import threading
import time
import subprocess
import json
import pika
import sys
import yaml
import uuid
import base64

with open("quditto_v2.yaml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

#Indicate the number of network links to initiate the locks

def bits_to_base64(bits_str):
    # Convertir la cadena de bits (str) a bytes
    bits_as_bytes = int(bits_str, 2).to_bytes((len(bits_str) + 7) // 8, byteorder='big')
    
    # Codificar los bytes en base64
    base64_encoded = base64.b64encode(bits_as_bytes)
    
    # Convertir el resultado a una cadena
    return base64_encoded.decode('utf-8')

def count_all_connections(data):
    connections = []
    
    for node in data.get('nodes', []):
        node_name = node['node_name']
        for neighbour in node.get('neighbour_nodes', []):
            neighbour_name = neighbour['name']
            connection = f"{node_name}{neighbour_name}"
            connections.append(connection)
    return connections

unique_connections = count_all_connections(cfg)

num_grupos = len(unique_connections)
grupos_locks = {i: threading.Lock() for i in range(num_grupos)}

def emul_BB84(grupo_id, grupo_lock, key, d, origin, n, call_id, e_d, percentage):
    print(f"Preparing link {grupo_id}...")

    script_name = "BB84_hilo.py"
    #script_name = "bb84_eve_percentage.py"

    print(f"Running BB84 on link: {grupo_id} with parameters: {key} {d}")

    command = ['python3', script_name, str(grupo_id), key, d]
    #command = ['python3', str(script_name), str(key), str(d), str(e_d), str(percentage)]

    #Entering the corresponding link's lock
    with grupo_lock:
        print(f"Running protocol on link {grupo_id}...")

        #Taking initial time
        inicio = time.perf_counter()

        #Running the BB84 simulation script with the given parameters
        result = subprocess.run(command, capture_output=True, text=True)
        print(f"Contenido de result.stdout: {result.stdout!r}")
        #Retrieving the simulation results
        try:
            salida = json.loads(result.stdout)
            clave_Alice = salida["alice_key"]
            clave_Bob = salida["bob_key"]
            tiempo_devuelto = salida["time"]
            print(clave_Alice == clave_Bob)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Link {grupo_id}: Error processing the results: {e}")
            return

        #Blocking the sending of results until the specified time has passed
        momento_actual = time.perf_counter()

        while momento_actual < inicio + tiempo_devuelto:
            momento_actual = time.perf_counter()
        
        timepo_real = momento_actual-inicio

        print(f"Link {grupo_id}: Key generated for Alice{clave_Alice} \n key generated for Bob{clave_Bob}\n delay: {tiempo_devuelto:.4f} sec")
        print(f"Actual time elapsed until key printing: {timepo_real:.4f} sec")

        #Sending results to both linked machines
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
        key_id = str(uuid.uuid4())

        clave_Alice = str(clave_Alice).replace("[", "").replace("]", "").replace(", ", "")
        clave_Alice = bits_to_base64(clave_Alice)
        message_A = {"key_ID":key_id, "key": clave_Alice, "call_id": call_id}
        json_A = json.dumps(message_A)

        clave_Bob = str(clave_Bob).replace("[", "").replace("]", "").replace(", ", "")
        clave_Bob = bits_to_base64(clave_Bob)
        message_B = {"node":origin, "key_ID":key_id, "key": clave_Bob}
        json_B = json.dumps(message_B)

        channel.basic_publish(
            exchange='direct_logs', routing_key=str(origin), body=json_A)
        channel.basic_publish(
            exchange='direct_logs', routing_key=str(n), body=json_B)
        connection.close()

# Search index of a specific link
def find_link_position(links, target_name):
    for index, item in enumerate(links):
        if item.get("link_name") == target_name:
            return index  # return link's position if found
    return -1 

#Request receiver funciton
def callback(ch, method, properties, body):
    
    print(f" [x] {method.routing_key}:{body}")

    body = json.loads(body)

    origin = body["origin"]
    n = body["node"]
    position = None

    for idx, connection in enumerate(unique_connections):
        if connection == origin + n:  # Locate the connection's position on the list
            position = idx
            break

    grupo_id = position

    key = body["key"]
    call_id = body["call_id"]
    

    #If the link requested is valid, begin simulation on a thread
    if 0 <= int(grupo_id) < num_grupos:
        nodes = cfg["nodes"]
        d = None
        for node in nodes:
            if node["node_name"] == origin:
                for neighbour in node["neighbour_nodes"]:
                    if neighbour.get("name") == n and "link_length" in neighbour:
                        d = neighbour["link_length"]
                        e_d = neighbour["eavesdropper_parameters"]["eavesdropper_distance"]
                        percentage = neighbour["eavesdropper_parameters"]["percentage_intercepted_qubits"]
                        break
        d=str(d)
        hilo = threading.Thread(target=emul_BB84, args=(grupo_id, grupos_locks[grupo_id], key, d, origin, n, call_id, e_d, percentage))
        hilo.start()

    else:
        print(f"Select a valid link...")

    time.sleep(1)
    

def lanzar_hilos():
    #Establish connection with localhost
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    #create message exchanger
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    #Create the simulation request queue
    result = channel.queue_declare(queue='', exclusive=True, arguments={'x-message-ttl': 60000,'x-expires': 1800000})
    queue_name = result.method.queue
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key="c")
    #Begin taking requests
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":

    lanzar_hilos()
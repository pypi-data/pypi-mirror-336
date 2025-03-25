import netsquid as ns
import numpy as np
import netsquid.components.instructions as instr
from netsquid.nodes import Node, Network, DirectConnection
from netsquid.components import QuantumChannel, QuantumProgram, ClassicalChannel, FibreDelayModel, FibreLossModel
from netsquid.protocols import NodeProtocol, Signals
from netsquid.components.qprocessor import QuantumProcessor, PhysicalInstruction
import sys
from netsquid.util.datacollector import DataCollector
import json

#Reads the parameters of the link ID, the final key length, 
# and the fiber connection distance.

if len(sys.argv) == 4:
    enlace = sys.argv[1]
    enlace = int(enlace)
    key = sys.argv[2]
    key = int(key)
    d = sys.argv[3]
    d = int(d)

else:
    sys.exit(1)


class EncodeQubitProgram(QuantumProgram):
    """
    Program to encode a bit according to a secret key and a basis.
    """

    default_num_qubits = 1

    def __init__(self, base, bit):
        super().__init__()
        self.base = base
        self.bit = bit

    def program(self):
        q1, = self.get_qubit_indices(1)
        self.apply(instr.INSTR_INIT, q1)
        if self.bit == 1:
            self.apply(instr.INSTR_X, q1)
        if self.base == 1:
            self.apply(instr.INSTR_H, q1)
        yield self.run()


class KeyReceiverProtocol(NodeProtocol):
    """
    Protocol for the receiver of the key.
    """

    def __init__(self, node, key_size=10, port_names=("qubitIO", "classicIO")):
        super().__init__(node)
        self.node = node
        self.q_port = port_names[0]
        self.c_port = port_names[1]
        self.key_size = key_size
        self.key = None

    def run(self):
        # Select random bases
        bases = np.random.randint(2, size=self.key_size)
        #print(bases)
        results = []
        for i in range(self.key_size):
            # Await a qubit from Alice
            yield self.await_port_input(self.node.ports[self.q_port])

            # Measure in random basis
            if bases[i] == 0:
                res = self.node.qmemory.execute_instruction(instr.INSTR_MEASURE, output_key="M")
            else:
                res = self.node.qmemory.execute_instruction(instr.INSTR_MEASURE_X, output_key="M")
            yield self.await_program(self.node.qmemory)
            results.append(res[0]['M'][0])
            self.node.qmemory.reset()
            

            # Send ACK to Alice to trigger next qubit send (except in last transmit)
            if i < self.key_size - 1:
                self.node.ports[self.c_port].tx_output('ACK')
        #print(results)

        # All qubits arrived, send bases
        self.node.ports[self.c_port].tx_output(bases)

        # Await matched indices from Alice and process key
        yield self.await_port_input(self.node.ports[self.c_port])
        matched_indices = self.node.ports[self.c_port].rx_input().items
        final_key = []
        #print(matched_indices)
        for i in matched_indices:
            final_key.append(results[i])
        self.key = final_key
        self.send_signal(signal_label=Signals.SUCCESS, result=final_key)

        final_key=str(final_key)

        with open(f'key_Bob{enlace}.txt', 'w') as archivo:
            archivo.write(final_key)


class KeySenderProtocol(NodeProtocol):
    """
    Protocol for the sender of the key.
    """

    def __init__(self, node, key_size=10, port_names=("qubitIO", "classicIO")):
        super().__init__(node)
        self.node = node
        self.q_port = port_names[0]
        self.c_port = port_names[1]
        self.key_size = key_size
        self.key = None

    def run(self):
        secret_key = np.random.randint(2, size=self.key_size)
        bases = list(np.random.randint(2, size=self.key_size))
        #print(bases)

        # Transmit encoded qubits to Bob
        for i, bit in enumerate(secret_key):
            self.node.qmemory.execute_program(EncodeQubitProgram(bases[i], bit))
            yield self.await_program(self.node.qmemory)

            q = self.node.qmemory.pop(0)
            self.node.ports[self.q_port].tx_output(q)
            if i < self.key_size - 1:
                yield self.await_port_input(self.node.ports[self.c_port])

        # Await response from Bob
        yield self.await_port_input(self.node.ports[self.c_port])
        bob_bases = self.node.ports[self.c_port].rx_input().items[0]
        matched_indices = []
        for i in range(self.key_size):
            if bob_bases[i] == bases[i]:
                matched_indices.append(i)

        self.node.ports[self.c_port].tx_output(matched_indices)
        final_key = []
        for i in matched_indices:
            final_key.append(secret_key[i])
        self.key = final_key
        self.send_signal(signal_label=Signals.SUCCESS, result=final_key)
        #print(final_key)

        final_key=str(final_key)

        with open(f'key_Alice{enlace}.txt', 'w') as archivo:
            archivo.write(final_key)


def create_processor():
    """Factory to create a quantum processor for each end node.

    Has three memory positions and the physical instructions necessary
    for teleportation.
    """
    physical_instructions = [
        PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
        PhysicalInstruction(instr.INSTR_H, duration=68, parallel=True),
        PhysicalInstruction(instr.INSTR_X, duration=68, parallel=True),
        PhysicalInstruction(instr.INSTR_X, duration=68, parallel=True),
        PhysicalInstruction(instr.INSTR_MEASURE, duration=1000, parallel=False),
        PhysicalInstruction(instr.INSTR_MEASURE_X, duration=1000, parallel=False)
    ]
    processor = QuantumProcessor("quantum_processor",
                                 phys_instructions=physical_instructions)
    return processor


def generate_network(link_len):
    """
    Generate the network. For BB84, we need a quantum and classical channel.
    """

    network = Network("BB84 Network")
    alice = Node("alice", qmemory=create_processor())
    bob = Node("bob", qmemory=create_processor())

    network.add_nodes([alice, bob])
    p_ab, p_ba = network.add_connection(alice,
                                        bob,
                                        label="q_chan",
                                        channel_to=QuantumChannel(name='AqB', length = link_len, 
                                                                  models={"delay_model": FibreDelayModel(), 
                                                                          "loss_model": FibreLossModel(p_loss_init=0,p_loss_length=0.12)}),
                                        channel_from=QuantumChannel(name='BqA', length = link_len, 
                                                                    models={"delay_model": FibreDelayModel(), 
                                                                            "loss_model": FibreLossModel(p_loss_init=0,p_loss_length=0.12)}),
                                        port_name_node1="qubitIO",
                                        port_name_node2="qubitIO")
    # Map the qubit input port from the above channel to the memory index 0 on Bob"s
    # side
    alice.ports[p_ab].forward_input(alice.qmemory.ports["qin0"])
    bob.ports[p_ba].forward_input(bob.qmemory.ports["qin0"])
    network.add_connection(alice,
                           bob,
                           label="c_chan",
                           channel_to=ClassicalChannel('AcB', length = link_len, 
                                                       models={"delay_model": FibreDelayModel(c=200000)}),
                           channel_from=ClassicalChannel('BcA', length = link_len, 
                                                         models={"delay_model": FibreDelayModel(c=200000)}),
                           port_name_node1="classicIO",
                           port_name_node2="classicIO")
    return network

def get_key(evexpr):
    event = evexpr.triggered_events[-1]
    return {"value": event.source.uid}

dc = DataCollector(get_key)


if __name__ == '__main__': 

    #Check the buffer for any leftover bits from previous protocol operations
    try:

        with open(f'buff_Alice{enlace}.txt','r') as archivo:
            buff_txt_Alice = archivo.read()

    except FileNotFoundError:
        buff_txt_Alice = []
    
    buff_txt_Alice=list(buff_txt_Alice)

    tot_key=[]
    buff=[]
    for j in buff_txt_Alice:
            if j == '0' or j == '1':
                j=int(j)
                buff.append(j)
    
    tot_key=buff

    try:

        with open(f'buff_Bob{enlace}.txt','r') as archivo:
            buff_txt_Bob = archivo.read()

    except FileNotFoundError:
        buff_txt_Bob = []
    
    buff_txt_Bob=list(buff_txt_Bob)

    tot_key_Bob=[]
    buff_Bob=[]
    for j in buff_txt_Bob:
            if j == '0' or j == '1':
                j=int(j)
                buff_Bob.append(j)
    
    tot_key_Bob=buff_Bob

    keep = True
    l=key
    if len(tot_key) > key:
        keep=False
        #If the buffer has enough bits to account for the key length, skip the protocol
    
    Time = 0

    while(keep==True):
        if l==0:
            l=1

        n = generate_network(link_len=d)
        
        node_a = n.get_node("alice")
        node_b = n.get_node("bob")

        p1 = KeySenderProtocol(node_a, key_size=l*2)
        p2 = KeyReceiverProtocol(node_b, key_size=l*2)

        p1.start()
        p2.start()
        
        stats = ns.sim_run()
        
        simulated_time = stats.timeline_status().split()[2]
        Time = Time + float(simulated_time)/1000000000

        with open(f'key_Alice{enlace}.txt','r') as archivo:
            key_txt=archivo.read()

        key_txt=list(key_txt)

        final_key_main=[]

        for j in key_txt:
            if j == '0' or j == '1':
                j=int(j)
                final_key_main.append(j)

        tot_key=tot_key + final_key_main

        with open(f'key_Bob{enlace}.txt','r') as archivo:
                key_txt_Bob=archivo.read()

        key_txt_Bob=list(key_txt_Bob)

        final_key_main_Bob=[]
        for j in key_txt_Bob:
                if j == '0' or j == '1':
                    j=int(j)
                    tot_key_Bob.append(j)

        tot_key_Bob=tot_key_Bob + final_key_main_Bob

        if len(tot_key) >= key:
            keep = False

        #Generate three times as many qubits as bits on the key are left
        l=(key-len(tot_key))*3
        ns.sim_reset()
    
    final_key_Alice = tot_key[:key]
    buff = tot_key[key:]

    final_key_Bob = tot_key_Bob[:key]
    buff_Bob = tot_key[key:]

    buff=str(buff)
    buff_Bob=str(buff_Bob)

    with open(f'buff_Alice{enlace}.txt','w') as archivo:
        archivo.write(buff)

    with open(f'buff_Bob{enlace}.txt','w') as archivo:
        archivo.write(buff_Bob)

    #Return the final key and its generation time to the controller

    resultado = {"alice_key": final_key_Alice, "bob_key": final_key_Bob, "time": Time}

    print(json.dumps(resultado))

    ns.sim_reset()
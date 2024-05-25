from typing import List
from neuron import Neuron
from neuron_type import NeuronType



input_neurons: List[Neuron] = []


def get_distance_to_north(): 
    return .3
input_neurons.append(Neuron('DTN', NeuronType.INPUT, input_func=get_distance_to_north))

def get_distance_to_east():
    return .4
input_neurons.append(Neuron('DTE', NeuronType.INPUT, input_func=get_distance_to_east))

def get_distance_to_south():
    return .7
input_neurons.append(Neuron('DTS', NeuronType.INPUT, input_func=get_distance_to_south))

def get_distance_to_west():
    return .6
input_neurons.append(Neuron('DTW', NeuronType.INPUT, input_func=get_distance_to_west))

def get_age():
    return .2
input_neurons.append(Neuron('AGE', NeuronType.INPUT, input_func=get_age))



output_neurons: List[Neuron] = []


def move_forward():
    return print('moved forward')
output_neurons.append(Neuron('MFW', NeuronType.OUTPUT, output_func_a=move_forward))

def move_up():
    return print('moved up')
def move_down():
    return print('moved down')
output_neurons.append(Neuron('MUD', NeuronType.OUTPUT, output_func_a=move_up, output_func_b=move_down))

def move_right():
    return print('moved right')
def move_left():
    return print('moved left')
output_neurons.append(Neuron('MRL', NeuronType.OUTPUT, output_func_a=move_right, output_func_b=move_left))

def move_north():
    return print('moved north')
def move_south():
    return print('moved south')
output_neurons.append(Neuron('MNS', NeuronType.OUTPUT, output_func_a=move_north, output_func_b=move_south))

def move_east():
    return print('moved east')
def move_west():
    return print('moved west')
output_neurons.append(Neuron('MEW', NeuronType.OUTPUT, output_func_a=move_east, output_func_b=move_west))


MAX_INTERNAL_NEURONS = 2

internal_neurons: List[Neuron] = [Neuron(f'I{i+1}', NeuronType.INTERNAL) for i in range(MAX_INTERNAL_NEURONS)]




Neuron.connect_neurons(input_neurons[4], internal_neurons[0], 1.1)
Neuron.connect_neurons(input_neurons[0], output_neurons[1], -2)
Neuron.connect_neurons(internal_neurons[0], output_neurons[1], .1)

Neuron.connect_neurons(input_neurons[4], output_neurons[1], -1.3)








neurons = input_neurons + output_neurons + internal_neurons

neurons = Neuron.sort(neurons)
neurons = Neuron.filter(neurons)

final_action = None
final_action_chance = float('-inf')

for i, n in enumerate(neurons):
    print(final_action, final_action_chance)
    if n.type == NeuronType.OUTPUT:
        neuron_action, action_chance = n.execute()
        if action_chance > final_action_chance and neuron_action is not None:
            final_action = neuron_action
            final_action_chance = action_chance
    else:
        n.execute()

print(final_action, final_action_chance)

# print(input_neurons)
# print(output_neurons)
# print(internal_neurons)

exit()
g = Genome(4)
b = Brain(g, sensory_neurons, output_neurons, internal_neurons)

# print(g)

b.create_brain()


print('===== INPUTS =====')
for n in internal_neurons + output_neurons:
    if n.input_neurons:
        print(n.type.name, n.name, n.input_neurons)
print('==================')

print('===== OUTPUTS =====')
for n in sensory_neurons + internal_neurons:
    if n.output_neurons:
        print(n.type.name, n.name, n.output_neurons)
print('==================')


def traverse_connection(neuron: SensoryNeuron | InternalNeuron | ActionNeuron, depth: int = 0) -> None:
    if neuron.type == NeuronType.SENSORY:
        print(neuron, depth)
    

    depth += 1
    for next_neuron in neuron.input_neurons:
        traverse_connection(next_neuron, depth)

traverse_connection(output_neurons[0])




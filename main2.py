from brain import Brain
from genome import Genome
from neuron import SensoryNeuron, InternalNeuron, ActionNeuron
from neuron_type import NeuronType


MAX_INTERNAL_NEURONS = 2


# ----------- InputSensorNeurons ----------- 
sensory_neurons: list[SensoryNeuron] = []


def get_distance_to_north():
    return .3
sensory_neurons.append(SensoryNeuron('dtn', get_distance_to_north))

def get_distance_to_east():
    return .4
sensory_neurons.append(SensoryNeuron('dte', get_distance_to_east))

def get_distance_to_south():
    return .7
sensory_neurons.append(SensoryNeuron('dts', get_distance_to_south))

def get_distance_to_west():
    return .6
sensory_neurons.append(SensoryNeuron('dtw', get_distance_to_west))

def get_age():
    return .2
sensory_neurons.append(SensoryNeuron('age', get_age))



# ----------- OutputActionNeurons ----------- 
action_neurons: list[ActionNeuron] = []


def move_up():
    return print('moved up')
action_neurons.append(ActionNeuron('mup', move_up))

def move_down():
    return print('moved down')
action_neurons.append(ActionNeuron('mdo', move_down))

def move_right():
    return print('moved right')
action_neurons.append(ActionNeuron('mri', move_right))

def move_left():
    return print('moved left')
action_neurons.append(ActionNeuron('mle', move_left))



# ----------- InternalNeurons ----------- 
internal_neurons: list[InternalNeuron] = [InternalNeuron(f'I{i+1}') for i in range(MAX_INTERNAL_NEURONS)]

# print(sensory_neurons)
# print(action_neurons)
# print(internal_neurons)

g = Genome(4)
b = Brain(g, sensory_neurons, action_neurons, internal_neurons)

# print(g)

b.create_brain()


print('===== INPUTS =====')
for n in internal_neurons + action_neurons:
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

traverse_connection(action_neurons[0])




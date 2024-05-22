from neuron import Neuron



ns = Neuron.create_neurons(1, 4, 1)

Neuron.connect_neurons(ns['S1'], ns['I1'])
Neuron.connect_neurons(ns['I1'], ns['I2'])
Neuron.connect_neurons(ns['I2'], ns['I3'])
Neuron.connect_neurons(ns['I3'], ns['I4'])
Neuron.connect_neurons(ns['I2'], ns['I4'])
Neuron.connect_neurons(ns['I4'], ns['A1'])

ns = list(ns.values())

sorted_neurons = Neuron.sort(ns)

for i, n in enumerate(sorted_neurons):
    print(i + 1, n)
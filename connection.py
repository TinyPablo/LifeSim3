from enum import Enum

from gene import Gene


class ConnectionTipType(Enum):
    SENSORY = 0
    INTERNAL = 1

class ConnectionEndType(Enum):
    ACTION = 0
    INTERNAL = 1




# class Connection:
#     def __init__(self, ) -> None:
#         pass


#     @property
#     def self_connected(self) -> bool:
#         return \
#             self.conn_tip_neuron_id == self.conn_end_neuron_id and \
#             self.conn_tip_neuron_type == self.conn_end_neuron_type
    
#     def are_inputs_equal(self, other: Self) -> bool:
#         return \
#             self.conn_tip_neuron_type == other.conn_tip_neuron_type and \
#             self.conn_tip_neuron_id == other.conn_tip_neuron_id
    
#     def are_outputs_equal(self, other: Self) -> bool:
#         return \
#             self.conn_end_neuron_type == other.conn_end_neuron_type and \
#             self.conn_end_neuron_id == other.conn_end_neuron_id
    
#     def __eq__(self, other: Self) -> bool:
#         return self.are_inputs_equal(other) and self.are_outputs_equal(other)
   
#     @staticmethod
#     def are_reverse_connected(a: Self, b: Self):
#         return \
#             a.conn_tip_neuron_type == b.conn_end_neuron_type and \
#             a.conn_end_neuron_type == b.conn_tip_neuron_type and \
#             a.conn_tip_neuron_id == b.conn_end_neuron_id and \
#             a.conn_end_neuron_id == b.conn_tip_neuron_id


    
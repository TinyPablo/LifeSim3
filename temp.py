from scipy.spatial import KDTree
import numpy as np

from grid import Grid


# Example list of entities with their (x, y) coordinates
entities = [
    (10, 10), (20, 20), (30, 30), (40, 40), (50, 50),
    (70, 70), (80, 80), (90, 90), (100, 100), (110, 110)
]

# Create a KDTree from entity coordinates
kd_tree = KDTree(entities)

# Coordinates of the entity to find the nearest neighbor for
target_entity = (64, 64)

# Query the KDTree for the nearest neighbor
distance, index = kd_tree.query(target_entity)

# Get the nearest entity's coordinates
nearest_entity = entities[index]

print(f"Nearest entity to {target_entity} is at {nearest_entity} with distance {distance}")

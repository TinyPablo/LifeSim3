import os
import random
from grid import Grid
from entity import Entity
from genome import Genome
from simulation_settings import settings


if settings.SEED == -1:
    settings.SEED = random.getrandbits(32)
    random.seed(settings.SEED)
else:
    random.seed(settings.SEED)

print('seed:', settings.SEED)

grid = Grid(settings.GRID_WIDTH, settings.GRID_HEIGHT)

# e = Entity(Genome(4))
for x in range(settings.GRID_WIDTH * settings.GRID_HEIGHT - 1):

    grid.deploy_enemy_randomly(Entity(Genome(4)))



print(grid)
# print(e.transform)




grid.render()
# TODO: create move method
exit()
print(grid)
print(e.transform)
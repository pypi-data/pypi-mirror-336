import time
from ScrapMechanicLogicTools import block_list
from ScrapMechanicLogicTools import color_list
from ScrapMechanicLogicTools import sm_helpers as sm
from ScrapMechanicLogicTools import Prefabs
start = time.perf_counter()



blocks = block_list.Blocks()  # list of usable blocks
objects = block_list.Objects()  # list of usable objects
colors = color_list.Colors()  # list of Scrap Mechanic Colors

ID = sm.ID()  # init ID class
blueprint = sm.Blueprint(ID)  # init Blueprint class

# simple pulse generator


pg = Prefabs.PulseGenerator(blueprint, (0, 0, 0), 1, colors.Red, (0, 0, 90))  # make the pulse generator from prefabs.py

blueprint.export_blueprint()  # save blueprint file


print(time.perf_counter()-start)  # the run time for fun :)

from ScrapMechanicLogicTools import block_list
from ScrapMechanicLogicTools import color_list
from ScrapMechanicLogicTools import sm_helpers as sm


blocks = block_list.Blocks()  # list of usable blocks
objects = block_list.Objects()  # list of usable objects
colors = color_list.Colors()  # list of Scrap Mechanic Colors
class PulseGenerator:
    def __init__(self,blueprint,pos,time,color=None,rotation=(0,0,0)):
        self.base = sm.FillBlock(blueprint,blocks.Spaceship_Block,(0,0,0),(4,5,1),color,rotation)  # make a base
        time = int(time*40)
        self.sw_xor = sm.LogicGate(blueprint, "xor", (1, 3, 1), "up", "up", colors.Blue,rotation)  # sw_xor as output and flip-flop
        self.tick_and = sm.LogicGate(blueprint, "and", (1, 2, 1), "up", "up",color,rotation)  # and gate for 1 tick pulse
        self.tick_nor = sm.LogicGate(blueprint, "nor", (1, 1, 1), "up", "up",color,rotation)  # nor gate for 1 tick pulse
        self.timer = sm.Timer(blueprint, int(time/40), time%40, (2, 2, 1), "north", "up", colors.Black,rotation)  # timer to set the pulse length
        self.button = sm.Button(blueprint, (2, 1, 1), "up", "up", colors.Green,rotation)  # button to trigger the pulse

        # connections
        self.sw_xor.connect(self.sw_xor)  # self wire the xor
        self.button.connect(self.tick_nor)  # connect the button to tick_nor
        self.button.connect(self.tick_and)  # connect the button to tick_and
        self.tick_nor.connect(self.tick_and)  # connect tick_nor to the tick_and
        self.tick_and.connect(self.sw_xor)  # connect tick_and to the sw_xor
        self.tick_and.connect(self.timer)  # connect tick_and to the timer
        self.timer.connect(self.sw_xor)  # connect timer to the sw_xor
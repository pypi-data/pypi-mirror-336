#sm_helpers version 0.5.6


import json
import os
from ScrapMechanicLogicTools import block_list
from ScrapMechanicLogicTools import color_list

blocks = block_list.Blocks()  # list of usable blocks
objects = block_list.Objects()  # list of usable objects
colors = color_list.Colors()  # list of Scrap Mechanic Colors



def offset(pos,offset):
    return (offset[0]+pos[0],offset[1]+pos[1],offset[2]+pos[2])


def hex_rgb(color):
    r = int(color[:2],16)
    g = int(color[2:4],16)
    b = int(color[4:],16)
    return r,g,b


def rgb_hex(color):
    if color[0] > 255:
        red = 255
    elif color[0] < 0:
        red = 0
    else:
        red = color[0]

    if color[1] > 255:
        green = 255
    elif color[1] < 0:
        green = 0
    else:
        green = color[1]

    if color[2] > 255:
        blue = 255
    elif color[2] < 0:
        blue = 0
    else:
        blue = color[2]

    hex_red = hex(red).replace("0x","")
    if len(hex_red) == 1:
        hex_red = "0" + hex_red
    hex_green = hex(green).replace("0x","")
    if len(hex_green) == 1:
        hex_green = "0" + hex_green
    hex_blue = hex(blue).replace("0x","")
    if len(hex_blue) == 1:
        hex_blue = "0" + hex_blue
    return hex_red + hex_green + hex_blue

def fill_void(object,size,block, color = "000000" ,offSet = None):
    def fill_block(member):
        if hasattr(member, "timer_pos"):
            posx, posy, posz = member.timer_pos
            posx -= offx
            posy -= offy
            posz -= offz
            filled_blocks[posx][posy][posz] = member

        posx, posy, posz = member.pos
        posx -= offx
        posy -= offy
        posz -= offz
        filled_blocks[posx][posy][posz] = member

    def fill():
        isblock = False
        blocks_members = [attr for attr in dir(blocks) if not callable(getattr(blocks, attr)) and not attr.startswith("__")]
        for each in blocks_members:
            if block["uuid"] == blocks.__getattribute__(each)["uuid"]:
                isblock = True
                break


        for x in range(len(filled_blocks)):
            for y in range(len(filled_blocks[x])):
                for z in range(len(filled_blocks[x][y])):
                    if filled_blocks[x][y][z] is None:
                        if isblock:
                            object.fill_block(block, (x+offx,y+offy,z+offz), (1,1,1), color)
                        else:
                            object.place_object(block,(x+offx,y+offy,z+offz),"up","up", color)

    x,y,z = size

    filled_blocks = [[[None for _ in range(z)] for _ in range(y)] for _ in range(x)]

    if offSet is not None:
        offx, offy, offz = offSet
    elif hasattr(object, "pos"):
        offx,offy,offz = object.pos
    else:
        offx, offy, offz = 0,0,0

    members = [attr for attr in dir(object) if not callable(getattr(object, attr)) and not attr.startswith("__")]

    for each in members:
        member = object.__getattribute__(each)
        if type(member) == type([]):
            for each in member:
                if hasattr(each, "pos"):
                    fill_block(each)

        elif hasattr(member,"pos"):
            fill_block(member)

    #show_fill_block()
    fill()

def border(blueprint,posx,posy,offx,offy):
    offx-=1
    offy-=1
    posx+=1

    for y in range(posy):
        blueprint.place_object(objects.Small_Pipe_Tee,(offx,y + offy,0),"up","up","000000")
        blueprint.place_object(objects.Duct_End,(offx,y + offy,0),"south","right","000000")
        blueprint.place_object(objects.Duct_End,(offx,y + offy,0),"north","left","000000")
        blueprint.place_object(objects.Duct_End,(offx,y + offy,0),"south","left","000000")

        blueprint.place_object(objects.Small_Pipe_Tee,(offx+posx,y + offy,0),"up","down","000000")
        blueprint.place_object(objects.Duct_End,(offx+posx,y + offy,0),"west","down","000000")
        blueprint.place_object(objects.Duct_End,(offx+posx,y + offy,0),"south","right","000000")
        blueprint.place_object(objects.Duct_End,(offx+posx,y + offy,0),"south","left","000000")

    for x in range(posx-1):
        blueprint.place_object(objects.Small_Pipe_Tee,(1+x+offx,offy-1,0),"up","left","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy-1,0),"west","down","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy-1,0),"east","left","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy-1,0),"west","left","000000")

        blueprint.place_object(objects.Small_Pipe_Tee,(1+x+offx,offy+posy,0),"up","right","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy+posy,0),"west","up","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy+posy,0),"east","left","000000")
        blueprint.place_object(objects.Duct_End,(1+x+offx,offy+posy,0),"west","left","000000")
    offy-=1
    blueprint.place_object(objects.Small_Pipe_Bend, (offx, offy, 0), "west", "left", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "west", "right", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "south", "left", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "west", "down", "000000")
    blueprint.place_object(objects.Duct_End, (offx, offy, 0), "south", "up", "000000")
    blueprint.place_object(objects.Small_Pipe_Bend, (offx, posy+offy+1, 0), "west", "right", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "west", "right", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "north", "left", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "west", "up", "000000")
    blueprint.place_object(objects.Duct_End, (offx, posy+offy+1, 0), "north", "right", "000000")
    blueprint.place_object(objects.Small_Pipe_Bend, (posx+offx, offy, 0), "east", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "south", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "east", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "south", "down", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, offy, 0), "east", "up", "000000")
    blueprint.place_object(objects.Small_Pipe_Bend, (posx+offx, posy+offy+1, 0), "east", "right", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "east", "down", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "north", "up", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "east", "left", "000000")
    blueprint.place_object(objects.Duct_End, (posx+offx, posy+offy+1, 0), "north", "right", "000000")


def rotate(rotation, pos, facing, rotated):
    def get_rotation(a):
        if a < 0:
            a *= -1
            a %= 360
            a = 360 - a
        else:
            a %= 360

        if a < 90 or a == 360:
            return 0
        if a < 180:
            return 1
        if a < 270:
            return 2
        if a < 360:
            return 3

    def get_index(index,a):
        index += get_rotation(a)
        if index > 3:
            index-=4
        return index
    def cos(a):
        if a < 90 or a == 360:
            return 1
        if a < 180:
            return 0
        if a < 270:
            return -1
        if a < 360:
            return 0

    def sin(a):
        if a < 90 or a == 360:
            return 0
        if a < 180:
            return 1
        if a < 270:
            return 0
        if a < 360:
            return -1

    def rotate_x(a, pos, facing, rotated):
        rotated_index = rotate.index(rotated)
        if facing in xfacing:
            facing_index = xfacing.index(facing)
            facing = xfacing[get_index(facing_index, a)]
            rotated = rotate[get_index(rotated_index, a)]
        else:
            if facing == "north":
                rotated = rotate[get_index(rotated_index,a)]
            else:
                rotated = rotate[get_index(rotated_index, -a)]

        return (cos(a)*pos[0] + sin(a)*pos[2],pos[1],sin(a)*pos[0] + cos(a)*pos[2]), facing, rotated

    def rotate_y(a, pos, facing, rotated):
        rotated_index = rotate.index(rotated)
        if facing in yfacing:
            facing_index = yfacing.index(facing)
            facing = yfacing[get_index(facing_index, a)]
            #rotated = rotate[get_index(rotated_index, a)]
        else:
            if facing == "east":
                rotated = rotate[get_index(rotated_index,a)]
            else:
                rotated = rotate[get_index(rotated_index, -a)]
        return (pos[0], cos(a)*pos[1] + -sin(a)*pos[2], sin(a)*pos[1] + cos(a)*pos[2]), facing, rotated

    def rotate_z(a, pos, facing, rotated):
        if facing in zfacing:
            facing_index = zfacing.index(facing)
            facing = zfacing[get_index(facing_index, a)]
        else:
            rotated_index = rotate.index(rotated)
            if facing == "up":
                rotated = rotate[get_index(rotated_index,a)]
            else:
                rotated = rotate[get_index(rotated_index, -a)]
        return (cos(a)*pos[0] + sin(a)*pos[1], sin(a)*pos[0] + cos(a)*pos[1], pos[2]), facing, rotated


    facing = facing
    rotated = rotated

    xfacing = ["up", "east", "down", "west"]
    zfacing = ["north", "east", "south", "west"]
    yfacing = ["north", "up", "south", "down"]

    rotate = ["up","right","down","left"]

    px, py, pz = pos
    rx, ry, rz = rotation

    rx = rx % 360
    ry = ry % 360
    rz = rz % 360
    #print(pos, facing, rotated)
    pos,facing,rotated = rotate_x(rx, pos, facing, rotated)
    #print(pos, facing, rotated)
    pos,facing,rotated = rotate_y(ry, pos, facing, rotated)
    #print(pos, facing, rotated)
    pos,facing,rotated = rotate_z(rz, pos, facing, rotated)
    #print(pos,facing,rotated)
    #print("////////////////////////////////////")
    return pos, facing, rotated

def location(args):
    x,y,z = args[0]
    facing = args[1]
    rotated = args[2]

    if facing == "west":
        if rotated == "down":
            return (x + 1,y,z + 1),(-3,2)
        elif rotated == "right":
            return (x + 1,y + 1,z + 1),(-2,-3)
        elif rotated == "left":
            return (x + 1,y,z),(2,3)
        elif rotated == "up":
            return (x + 1,y + 1,z),(3,-2)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "up":
        if rotated == "down":
            return (x + 1,y + 1,z),(-2,-1)
        elif rotated == "right":
            return (x,y + 1,z),(1,-2)
        elif rotated == "left":
            return (x + 1,y,z),(-1,2)
        elif rotated == "up":
            return (x,y,z),(2,1)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "down":
        if rotated == "left":
            return (x + 1,y + 1,z + 1),(-1,-2)
        elif rotated == "up":
            return (x + 1,y,z + 1),(2,-1)
        elif rotated == "down":
            return (x,y + 1,z + 1),(-2,1)
        elif rotated == "right":
            return (x,y,z + 1),(1,2)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "south":
        if rotated == "down":
            return (x + 1,y + 1,z + 1),(-3,-1)
        elif rotated == "right":
            return (x,y + 1,z + 1),(1,-3)
        elif rotated == "left":
            return (x + 1,y + 1,z),(-1,3)
        elif rotated == "up":
            return (x,y + 1,z),(3,1)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "north":
        if rotated == "down":
            return (x + 1,y,z + 1),(-1,-3)
        elif rotated == "right":
            return (x,y,z),(1,3)
        elif rotated == "left":
            return (x,y,z + 1),(-3,1)
        elif rotated == "up":
            return (x + 1,y,z),(3,-1)
        else:
            print("not a valid rotation")
            exit(1)
    elif facing == "east":
        if rotated == "down":
            return (x,y + 1,z + 1),(-3,-2)
        elif rotated == "left":
            return (x,y + 1,z),(-2,3)
        elif rotated == "right":
            return (x,y,z + 1),(2,-3)
        elif rotated == "up":
            return (x,y,z),(3,2)
        else:
            print("not a valid rotation")
            exit(1)
    else:
        print("not a valid rotation")
        exit(1)

def wedge_color_match(color):
    red,green,blue = hex_rgb(color)
    red -= 25
    green -= 32
    blue -= 32
    return rgb_hex((red,green,blue))


def connect_logic(logic1,logic2):
    for i in range(len(logic1)):
        logic1[i].connect(logic2[i])


class LightObject:
    def __init__(self,blueprint,block,ID,positon,facing,rotated,color=None,lightColor=None,coneAngle=0,activity=False,rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))
        self.block = block
        self.color = color
        self.ID = ID
        self.lightColor = lightColor
        self.coneAngle = coneAngle
        self.activity = activity

        self.connections = []

        if self.color == None:
            self.color = block["color"]

        if self.lightColor == None:
            self.lightColor = block["color"]

        if self.coneAngle == 0:
            self.coneAngle = 0
        if self.activity == False:
            self.activity = False

        blueprint.parts.append(self)

    def connect(self,device):
        if type(device) == type([]):
            for i in device:
                if type(device) == int:
                    self.connections.append({"id": i})
                else:
                    self.connections.append({"id": i.ID})
        elif type(device) == int:
            self.connections.append({"id": device})
        elif device is not None:
            self.connections.append({"id": device.ID})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections
        return {
            "color":self.color,
            "controller":{
                "color":self.lightColor,
                "coneAngle":self.coneAngle,
                "active":self.activity,
                "controllers":self.connections,
                "id":self.ID,
                "joints":None,
                "luminance":0},
            "pos":{
                "x":self.pos[0],
                "y":self.pos[1],
                "z":self.pos[2]},
            "shapeId":self.block["uuid"],
            "xaxis":self.rot[0],
            "zaxis":self.rot[1]}

class PlaceObject:
    def __init__(self,blueprint,block,positon,facing,rotated,color=None,rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))
        self.block = block
        self.color = color

        blueprint.parts.append(self)


    def blueprint(self):
        if self.color == None:
            self.color = self.block["color"]

        return {
            "color":self.color,
            "pos":{
                "x":self.pos[0],
                "y":self.pos[1],
                "z":self.pos[2]},
            "shapeId":self.block["uuid"],
            "xaxis":self.rot[0],
            "zaxis":self.rot[1]}

class FillBlock:
    def __init__(self,blueprint, block, pos, size, color=None, rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, pos, "north", "right"))
        if color == None:
            self.color = block["color"]
        else:
            self.color = color
        self.block = block
        self.size = size

        blueprint.parts.append(self)

    def blueprint(self):
        print(self.pos,self.size,self.rot)
        return {
            "bounds": {
                "x": self.size[0],
                "y": self.size[1],
                "z": self.size[2]},
            "color": self.color,
            "pos": {
                "x": self.pos[0],
                "y": self.pos[1],
                "z": self.pos[2]},
            "shapeId": self.block["uuid"],
            "xaxis": self.rot[0],
            "zaxis": self.rot[1]}
class LogicGate:
    def __init__(self,blueprint,mode,positon,facing,rotated,color=None,rotation=(0,0,0),ID = None):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))

        if mode == "and":
            mode = 0
        elif mode == "or":
            mode = 1
        elif mode == "xor":
            mode = 2
        elif mode == "nand":
            mode = 3
        elif mode == "nor":
            mode = 4
        elif mode == "xnor":
            mode = 5
        else:
            mode = 0

        if color == None:
            color = "df7f01"

        self.facing = facing
        self.rotated = rotated
        self.mode = mode
        self.color = color
        if ID is not None:
            if ID is int:
                self.ID = id
            else:
                print("ID must be int ")
                exit(1)
        else:
            self.ID = blueprint.Logic_ID.get_next()
        self.connections = []
        blueprint.parts.append(self)

    def connect(self,device):
        if type(device) == type([]):
            for i in device:
                if type(device) == int:
                    self.connections.append({"id": i})
                else:
                    self.connections.append({"id": i.ID})
        elif type(device) == int:
            self.connections.append({"id": device})
        elif device is not None:
            self.connections.append({"id": device.ID})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color": self.color,
            "controller": {
                "active": False,
                "controllers": connections,
                "id": self.ID,
                "mode": self.mode},
            "pos": {
                "x": self.pos[0],
                "y": self.pos[1],
                "z": self.pos[2]},
            "shapeId": "9f0f56e8-2c31-4d83-996c-d00a9b296c3f",
            "xaxis": self.rot[0],
            "zaxis": self.rot[1]}

class Timer:
    def get_timer_pos(self,facing,pos):
        if facing == "east":
            return pos[0]+1,pos[1],pos[2]
        if facing == "west":
            return pos[0]-1,pos[1],pos[2]
        if facing == "north":
            return pos[0],pos[1]+1,pos[2]
        if facing == "south":
            return pos[0]+1,pos[1]-1,pos[2]
        if facing == "up":
            return pos[0],pos[1],pos[2]+1
        if facing == "down":
            return pos[0]+1,pos[1],pos[2]-1
        print("error in get_timer_pos()")
        exit(1)

    def __init__(self,blueprint,seconds,ticks,positon,facing,rotated,color=None,rotation=(0,0,0)):
        if 0 <= seconds <= 59:
            if 0 <= ticks <= 40:
                self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))

                if color == None:
                    color = "df7f01"


                self.timer_pos = self.get_timer_pos(facing,self.pos)

                self.facing = facing
                self.rotated = rotated
                self.color = color
                self.ID = blueprint.Logic_ID.get_next()
                self.seconds = seconds
                self.ticks = ticks
                self.connections = []

                blueprint.parts.append(self)

                return
        print("timer error")
        print(ID,seconds,ticks,positon,facing,rotated,color,rotation)
        exit(1)

    def connect(self,device):
        if type(device) == type([]):
            for i in device:
                self.connections.append({"id": i.ID})
        else:
            self.connections.append({"id": device.ID})


    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color": self.color,
            "controller": {
                "active": False,
                "controllers": connections,
                "id": self.ID,
                "joints": None,
                "seconds": self.seconds,
                "ticks": self.ticks},

            "pos": {
                "x": self.pos[0],
                "y": self.pos[1],
                "z": self.pos[2]},
            "shapeId": "8f7fd0e7-c46e-4944-a414-7ce2437bb30f",
            "xaxis": self.rot[0],
            "zaxis": self.rot[1]}

class Switch:
    def __init__(self,blueprint,positon,facing,rotated,color=None,rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))
        if color == None:
            color = "df7f01"



        self.facing = facing
        self.rotated = rotated
        self.color = color
        self.ID = blueprint.Logic_ID.get_next()
        self.connections = []

        blueprint.parts.append(self)

    def connect(self,device):
        if type(device) == type([]):
            for i in device:
                self.connections.append({"id": i.ID})
        else:
            self.connections.append({"id": device.ID})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color":self.color,
            "controller":{
                "active":False,
                "controllers":connections,
                "id":self.ID,
                "joints":None},
            "pos":{
                "x":self.pos[0],
                "y":self.pos[1],
                "z":self.pos[2]},
            "shapeId":"7cf717d7-d167-4f2d-a6e7-6b2c70aa3986",
            "xaxis":self.rot[0],
            "zaxis":self.rot[1]}

class Button:
    def __init__(self,blueprint,positon,facing,rotated,color=None,rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))
        if color == None:
            color = "df7f01"



        self.facing = facing
        self.rotated = rotated
        self.color = color
        self.ID = blueprint.Logic_ID.get_next()
        self.connections = []

        blueprint.parts.append(self)

    def connect(self, device):
        if type(device) == type([]):
            for i in device:
                self.connections.append({"id": i.ID})
        else:
            self.connections.append({"id": device.ID})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color":self.color,
            "controller":{
                "controllers":connections,
                "id":self.ID,
                "joints":None},
            "pos":{
                "x":self.pos[0],
                "y":self.pos[1],
                "z":self.pos[2]},
            "shapeId":"1e8d93a4-506b-470d-9ada-9c0a321e2db5",
            "xaxis":self.rot[0],
            "zaxis":self.rot[1]}

class Chair:
    def __init__(self,blueprint,positon,facing,rotated,color=None,rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))
        if color == None:
            color = "df7f01"



        self.facing = facing
        self.rotated = rotated
        self.color = color
        self.ID = blueprint.Logic_ID.get_next()
        self.connections = []

        blueprint.parts.append(self)

    def connect(self, device):
        if type(device) == type([]):
            for i in device:
                self.connections.append({"id": i.ID})
        else:
            self.connections.append({"id": device.ID})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color":self.color,
            "controller":{
                "controllers":connections,
                "id":self.ID,
                "joints":None},
            "pos":{
                "x":self.pos[0],
                "y":self.pos[1],
                "z":self.pos[2]},
            "shapeId":"4c93de5a-72ab-40d0-a081-c41e3aa87e86",
            "xaxis":self.rot[0],
            "zaxis":self.rot[1]}

class Seat:
    def __init__(self,blueprint,seat,positon,facing,rotated,color=None,rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))
        if color == None:
            color = "df7f01"



        self.facing = facing
        self.seat = seat
        self.rotated = rotated
        self.color = color
        self.ID = blueprint.Logic_ID.get_next()
        self.connections = []

        blueprint.parts.append(self)

    def connect(self, device):
        if type(device) == type([]):
            for i in device:
                self.connections.append({"id": i.ID})
        else:
            self.connections.append({"id": device.ID})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color":self.color,
            "controller":{
                "controllers":connections,
                "id":self.ID,
                "joints":None,
                "steering":None},
            "pos":{
                "x":self.pos[0],
                "y":self.pos[1],
                "z":self.pos[2]},
            "shapeId":self.seat["uuid"],
            "xaxis":self.rot[0],
            "zaxis":self.rot[1]}

class horn:
    def __init__(self,blueprint,positon,facing,rotated,color=None,rotation=(0,0,0)):
        self.pos, self.rot = location(rotate(rotation, positon, facing, rotated))
        if color == None:
            color = "df7f01"



        self.facing = facing
        self.rotated = rotated
        self.color = color
        self.ID = blueprint.Logic_ID.get_next()
        self.connections = []

        blueprint.parts.append(self)

    def connect(self, device):
        if type(device) == type([]):
            for i in device:
                self.connections.append({"id": i.ID})
        else:
            self.connections.append({"id": device.ID})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color":self.color,
            "controller":{
                "containers": None,
                "controllers":connections,
                "data":"gExVQQAAAAEFBQDwAgIAAAAEgHNsaWRlclBvcwgF",
                "id":self.ID,
                "joints":None},
            "pos":{
                "x":self.pos[0],
                "y":self.pos[1],
                "z":self.pos[2]},
            "shapeId":"818f4e15-ff51-4fed-b874-723a25d62e1c",
            "xaxis":self.rot[0],
            "zaxis":self.rot[1]}

class Blueprint:
    def __init__(self,Logic_ID):

        if not os.path.isfile("config.txt"):
            print("Config file not found!")
            print("Creating new config file...")
            print("Please enter the paths and blueprint in to the config file.")
            with open("config.txt", "w") as config:
                config.write("path/to/SteamLibrary/steamapps/common/Scrap Mechanic\n")
                config.write("path/to/blueprint/folder\n")
                config.write("blueprint-folder-name")
            exit(1)

        with open("config.txt", "r") as config:
            self.game_path = config.readline()[:-1]
            self.path = config.readline()[:-1] + "/"
            self.blueprint = config.readline()

        if self.path == "path/to/blueprint/folder/":
            print("Please check the config file. The example path is still in use!")
            exit(1)

        if self.path == "blueprint-folder-name":
            print("Please check the config file. The example blueprint is still in use!")
            exit(1)

        if not os.path.isdir(self.path):
            print("Sorry the path to the blueprint folder did not work")
            print("Please check the config file")
            exit(1)

        if not os.path.isdir(self.path + self.blueprint):
            print("Sorry the blueprint was not found in the blueprint folder")
            print("Please check the config file")
            exit(1)

        self.version = 4
        self.bodies = []
        self.childs = []
        self.parts = []
        self.Logic_ID = Logic_ID
        self.dependencies = []


    def export_blueprint(self):
        for blueprint in self.parts:
            self.childs.append(blueprint.blueprint())
        blueprint = {}
        blueprint["bodies"] = self.bodies
        blueprint["bodies"].append({
            "childs":self.childs})
        blueprint["version"] = self.version
        with open(f"{self.path+self.blueprint}/blueprint.json","w") as bp:
            bp.write(json.dumps(blueprint))
        print(self.path+self.blueprint)
        print("export complete")

    def add_dependency(self, dependency):
        for each in dependency:
            print(each)

    def connect_ID(blueprint,IDs1,IDs2):
        for i in range(len(IDs1)):
            IDs1[i].connect(IDs2[i])

    def connect_IDS(blueprint,ID,IDs):
        for i in range(len(IDs)):
            ID.connect(IDs[i])



    def addIds(self,ID1,IDs):
        for index in range(len(self.childs)):
            each = self.childs[index]
            if "controller" in each.keys():
                if "id" in each["controller"].keys():
                    if each["controller"]["id"] == ID1:
                        if each["controller"]["controllers"] == None:
                            self.childs[index]["controller"]["controllers"] = []
                        for ID2 in IDs:
                            control = {}
                            control["id"] = ID2
                            self.childs[index]["controller"]["controllers"].append(control)

    def linkIDs(self,ID1,IDs):
        for index in range(len(self.childs)):
            each = self.childs[index]
            if "controller" in each.keys():
                if "id" in each["controller"].keys():
                    for ID2 in IDs:
                        if each["controller"]["id"] == ID2:
                            if each["controller"]["controllers"] == None:
                                self.childs[index]["controller"]["controllers"] = []
                                control = {}
                                control["id"] = ID1
                                self.childs[index]["controller"]["controllers"].append(control)


    def fast_logic_gate(self,ID,Mode,positon,facing,rotated,color=None,rotation=(0,0,0)):
        pos,facing,rotated = rotate(rotation,positon,facing,rotated)
        pos,rot = location(pos,facing,rotated)
        if Mode == "and":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggA"
        elif Mode == "or":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggB"
        elif Mode == "xor":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggC"
        elif Mode == "nand":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggD"
        elif Mode == "nor":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggE"
        elif Mode == "xnor":
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggF"
        else:
            mode = "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggA"

        if color == None:
            color = "df7f01"
        self.childs.append({
            "color":color,
            "controller":{
                "containers":None,
                "controllers":None,
                "data":mode,
                "id":ID,
                "joints":None},
            "pos":{
                "x":pos[0],
                "y":pos[1],
                "z":pos[2]},
            "shapeId":"8f98db04-72eb-4a3a-88a1-f4f3e8d818ee",
            "xaxis":rot[0],
            "zaxis":rot[1]})

    def merge(self,blueprint):
        self.childs = self.childs + blueprint.childs

    def load(self):
        with open(f"{self.path+self.blueprint}/blueprint.json","r") as bp:
            blueprint = json.loads(bp.read())

        self.bodies = []
        self.childs = blueprint["bodies"][0]["childs"]
        self.version = blueprint["version"]

class Joints:
    def __init__(self):
        self.joints = []

    def addJoint(self,joint):
        self.joints.append(joint)

class ID:
    def __init__(self):
        self.used_IDs = []
        self.current_ID = 0

    def cheak_ID(self,ID):
        for ID_range in self.used_IDs:
            if ID_range[0] <= ID <= ID_range[1]:
                return True
        return False

    def add_ID(self,ID):
        if self.cheak_ID(ID):
            return False
        self.used_IDs.append((ID,ID))
        self.clean()
        return True

    def get_next(self):
        while not self.add_ID(self.current_ID):
            self.current_ID += 1
        self.clean()
        return self.current_ID

    def set_ID(self,ID):
        if self.add_ID(ID):
            return ID
        else:
            return None

    def set_range(self,range):
        self.used_IDs.append(range)

    def clean(self):
        length = len(self.used_IDs)
        new_range = [self.used_IDs[0][0],self.used_IDs[0][1]]
        new_used_IDs = []
        for index in range(length):
            if index + 1 < length:
                if self.used_IDs[index + 1][0] == new_range[1] + 1:
                    new_range[1] = self.used_IDs[index + 1][1]
                else:
                    new_used_IDs.append(tuple(new_range))
                    new_range = [self.used_IDs[index + 1][0],self.used_IDs[index + 1][1]]
            else:
                new_used_IDs.append(tuple(new_range))
        self.used_IDs = new_used_IDs

    def claim_range(self,amount):
        next = 0
        for range in self.used_IDs:
            s,e = range
            if next <= s <= next + amount or next <= e <= next + amount:
                next = e + 1

        self.used_IDs.append((next,next + amount))
        print(next)
        return (next)

class AsciiBlock:
    def __init__(self, blueprint, id, char, positon, facing, rotated, color=None, rotation=(0,0,0)):
        pos, facing, rotated = rotate(rotation, positon, facing, rotated)
        pos, rot = location(pos, facing, rotated)

        if color == None:
            color = "df7f01"



        self.facing = facing
        self.rotated = rotated
        self.char = char
        self.color = color
        if type(id) == int:
            self.ID = id
        else:
            self.ID = id.get_next()
        self.connections = []
        blueprint.parts.append(self)

        blueprint.add_dependency({"contentId":"b7443f95-67b7-4f1e-82f4-9bef0c62c4b3","name":"The Modpack Continuation","shapeIds":["a459eb96-7f0a-42e6-a841-44f9c0561a55"],"steamFileId":2448492759})

    def blueprint(self):
        if self.connections == []:
            connections = None
        else:
            connections = self.connections

        return {
            "color": self.color,
            "controller": {
                "containers": None,
                "controllers": None,
                "data": self.char,
                "id": self.ID,
                "joints": None},
            "pos": {
                "x": self.pos[0],
                "y": self.pos[1],
                "z": self.pos[2]},
            "shapeId": "a459eb96-7f0a-42e6-a841-44f9c0561a55",
            "xaxis": self.rot[0],
            "zaxis": self.rot[1]}

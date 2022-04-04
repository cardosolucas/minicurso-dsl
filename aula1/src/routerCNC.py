from textx import metamodel_from_str

def cname(o):
    if type(o) is str:
        return o
    return o.__class__.__name__

grammar = """
Model: commands*=Command;
Command: G20 | G21 | G0 | G1 | G2 | G3 | G40 | G41 | G42;
G20: 'G20';
G21: 'G21';
G40: 'G40';
G0: 'G0' position=Point;
G1: 'G1' position=Point;
G2: 'G2' position=PointRot;
G3: 'G3' position=PointRot;
G41: 'G41' position=PointCom;
G42: 'G42' position=PointCom;
Point: x=INT ',' y=INT;
PointRot: x=INT ',' y=INT ',' rot=INT;
PointCom: z=INT;
"""

class Point(object):
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y
    
    def __str__(self):
        return "{},{}".format(self.x, self.y)

class PointRot(object):
    def __init__(self, parent, x, y, rot):
        self.parent = parent
        self.x = x
        self.y = y
        self.rot = rot

    def __str__(self):
        return "{},{},{}".format(self.x, self.y, self.rot)

class PointCom(object):
    def __init__(self, parent, z):
        self.parent = parent
        self.z = z

    def __str__(self):
        return "{}".format(self.z)

mm = metamodel_from_str(grammar, classes=[Point, PointRot, PointCom])

model_str = """
G20
G0 5,10
G1 10,10
G2 20,30,20
G41 30
"""

model = mm.model_from_str(model_str)

for command in model.commands:
    cname_s = cname(command)
    if cname_s == 'G20' or cname_s == 'G21' or cname_s == 'G40':
        print("Executando {}...".format(cname_s))
    else:
        print("Executando {} args={}".format(cname_s, command.position))
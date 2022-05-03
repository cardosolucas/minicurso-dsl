import sys
from dsl import Pipeline, Task
from textx import metamodel_from_str, get_children_of_type

class Symbol(object):
    def __init__(self, parent, symb):
        self.parent = parent
        self.symb = symb

class Parameter(object):
    def __init__(self, parent, name, arg):
        self.parent = parent
        self.name = name9
        self.arg = arg

def cname(o):
    return o.__class__.__name__

f = open('grammar.tx', 'r')
grammar = f.read()
f.close()

f = open(sys.argv[1], 'r')
model_str = f.read()
f.close()

mm = metamodel_from_str(grammar, classes=[Parameter])

model = mm.model_from_str(model_str)

pipe = Pipeline(sys.argv[1])

#default value
workers = 2

for command in model.commands:
    if cname(command) == 'Task':
        name = command.name
        nbpath = command.nbpath
        nbout = command.nbout
        params = {}
        if command.pars != []:
            for param in command.pars:
                params[param.name] = param.arg
        pipe.add_task(Task(name, nbpath, nbout, params))

    if cname(command) == 'Workers':
        if command.workers > 0:
            workers = command.workers

    if cname(command) == 'Pipeline':
        pipe.add_dag(command.symb)
        pipe.run_pipeline(workers)
    





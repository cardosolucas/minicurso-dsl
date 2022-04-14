import papermill as pm 
import networkx as nx 
from joblib import Parallel, delayed

class DagBuildError(Exception):
    pass

def execute_step(task):
    pm.execute_notebook(task.nb_path, task.nb_out_path, task.parameters)

def parse_dag_str(dag_str):
    #task_1 -> task_21 | task_22 -> task_3
    aux_pipe = dag_str.split()
    #['task_1', '->', 'task_21',  '|', 'task_22']
    aux_pipe = list(filter(('|').__ne__, aux_pipe))
    #['task_1', '->', 'task_21', 'task_22']
    index = 0
    parsed_dag = []
    while index < len(aux_pipe):
        level = []
        try:
            while aux_pipe[index] != '->':
                level.append(aux_pipe[index])
                index += 1
        except IndexError:
            pass
        parsed_dag.append(tuple(level))
        index += 1
    return parsed_dag

def dag_list_to_graph(parsed_dag):
    graph = []
    ref = 0
    while True:
        try:
            t1 = parsed_dag[ref]
            t2 = parsed_dag[ref + 1]
            for step_t1 in t1:
                for step_t2 in t2:
                    graph.append((step_t1, step_t2))
            ref += 1
        except IndexError:
            break
    return graph


class Task(object):
    def __init__(self, task_name, nb_path, nb_out_path, parameters):
        self.task_name = task_name
        self.nb_path = nb_path
        self.nb_out_path = nb_out_path
        self.parameters = parameters

class Pipeline(object):
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.pipeline_dict = {}
        self.pipeline_graph = None

    def add_task(self, task_obj):
        self.pipeline_dict[task_obj.task_name] = task_obj

    def get_task_by_name(self, task_name):
        return self.pipeline_dict[task_name]

    def add_dag(self, dag_str):
        try:
            parsed_dag = parse_dag_str(dag_str)
            out = dag_list_to_graph(parsed_dag)
            dag = nx.DiGraph()
            dag.add_edges_from(out)
        except:
            raise DagBuildError("Error while parsing DAG")
        
        if not nx.is_directed_acyclic_graph(dag):
            raise DagBuildError("Parsed graph is not a DAG")

        self.pipeline_graph = dag

    def run_level(self, level, n_jobs):
        task_list = [self.get_task_by_name(l) for l in level]
        Parallel(n_jobs = n_jobs)(delayed(execute_step)(t) for t in task_list)

    def run_pipeline(self, n_jobs):
        in_degrees = dict(self.pipeline_graph.in_degree)
        init_list = []
        for node in in_degrees:
            if in_degrees[node] == 0:
                init_list.append(node)

        topological_list = list(nx.topological_sort(
                                nx.line_graph(self.pipeline_graph)
                                ))
        
        while init_list != []:
            self.run_level(init_list, n_jobs)
            next_list = []
            for conn in topological_list:
                if conn[0] in init_list:
                    next_list.append(conn[1])
            next_list = list(set(next_list))
            init_list = next_list
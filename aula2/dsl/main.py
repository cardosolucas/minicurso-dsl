from dsl import Pipeline, Task

pipe = Pipeline('pipeline_1')

pipe.add_task(Task('note1', 'notebooks/note1.ipynb', 'notebooks/note1_out.ipynb', {}))
pipe.add_task(Task('note2', 'notebooks/note2.ipynb', 'notebooks/note2_out.ipynb', {}))
pipe.add_task(Task('note3', 'notebooks/note3.ipynb', 'notebooks/note3_out.ipynb', {}))
pipe.add_task(Task('note4', 'notebooks/note4.ipynb', 'notebooks/note4_out.ipynb', {}))
pipe.add_task(Task('note5', 'notebooks/note5.ipynb', 'notebooks/note5_out.ipynb', {}))
pipe.add_task(Task('note6', 'notebooks/note6.ipynb', 'notebooks/note6_out.ipynb', {}))

pipe.add_dag('note1 -> note3 | note4 -> note2 | note5 -> note6')

pipe.run_pipeline(3)
# import kubeflow libs
from kfp import dsl

# list of packages to install
@dsl.component(base_image="python:3.11", packages_to_install=["numpy", "pandas"])
def rand_matrix(rows: int, cols: int, values: int
      , outfile: dsl.OutputPath("numpy")) -> str:
   import numpy as np
   import pickle

   print(f">>> outfile: {outfile}")

   mat = np.random.randint(-values, values, (rows, cols))
   # write out the matrix as bytes with pickle
   with open(outfile, "wb") as f:
      pickle.dump(mat, f)

   return outfile

@dsl.component(base_image="python:3.11", packages_to_install=["numpy", "pandas"])
def display_matrix(infile: dsl.InputPath("numpy")):
   import numpy as np
   import pickle

   print(f">>> infile: {infile}")

   with open(infile, "rb") as f:
      mat = pickle.load(f)

   print(">>>> numpy: ", mat)

@dsl.pipeline(name="my-first-pipeline", display_name="My first pipeline")
def my_first_pipeline(rows: int, cols: int, values: int):

   rand_matrix_step = rand_matrix(rows=rows, cols=cols, values=values)
   display_matrix(infile=rand_matrix_step.outputs['outfile'])


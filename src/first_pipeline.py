# import kubeflow libs
from kfp import dsl

# annotate function to be a componenet
# function will be converted into a container
# base_image is the image name
@dsl.component(base_image="python:3.12")
def power(base: int, ex: int) -> int:
   answer = 1
   for i in range(ex):
      answer = answer * base 
   return answer

# list of packages to install
@dsl.component(base_image="python:3.11", packages_to_install=["numpy", "pandas"])
def rand_matrix(rows: int, cols: int, values: int) -> str:
   import numpy as np
   import json

   mat = np.random.randint(-values, values, (rows, cols))
   # can only return primitive number, boolean, string
   # convert to JSON string
   return json.dumps(mat.tolist())

@dsl.pipeline(name="my-first-pipeline", display_name="My first pipeline")
def my_first_pipeline(p_base: int, p_ex: int):

   # Must use keyword arguments to invoke the component
   _result = power(base=p_base, ex=p_ex)

   _mat = rand_matrix(rows=p_base, cols=p_ex, values=_result.output)

   print(">>>> _result: ", _result)
   print(">>>> _mat: ", _mat)

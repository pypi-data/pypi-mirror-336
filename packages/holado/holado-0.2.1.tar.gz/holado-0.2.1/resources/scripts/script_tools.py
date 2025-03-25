import os
import sys


def insert_holado_helper():
    # Insert path to holado_helper
    # holado_path = os.getenv('HOLADO_PATH')
    # if holado_path is None:
    #     raise Exception("Missing environment variable HOLADO_PATH with HolAdo installation path")
    holado_path = os.getenv('TESTING_SOLUTION_PATH')
    if holado_path is None:
        raise Exception("Missing environment variable TESTING_SOLUTION_PATH with HolAdo installation path")
    sys.path.insert(0, os.path.join(holado_path, "src", "holado_helper", "script") )
    


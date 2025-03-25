#################################################
# HolAdo (Holistic Automation do)
#
# (C) Copyright 2021-2025 by Eric Klumpp
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
#################################################

import logging

logger = logging.getLogger(__name__)


class Undefined(object):
    def __init__(self, undefined_value=0):
        self.__value = undefined_value

def is_undefined(obj):
    return isinstance(obj, Undefined)


# Define specific undefined objects

undefined_argument = Undefined(0)
undefined_value = Undefined(1)



# Define specific default values
# Note: Real value is defined by methods managing these values as argument.

default_value = Undefined(2)
default_context = Undefined(3)      # Example of real value: for ThreadsManager it means "current ScenarioContext" if a scenario context exists else "SessionContext".



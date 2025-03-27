# -*- coding: utf-8 -*-

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


from holado_test.scenario.step_tools import StepTools
from holado.common.context.session_context import SessionContext
from holado_test.behave.behave import *
import logging
from holado_test.behave.scenario.behave_step_tools import BehaveStepTools
from holado_value.common.tables.converters.value_table_converter import ValueTableConverter
from holado_python.standard_library.socket.blocking_socket import TCPBlockingSocketClient
from holado_python.standard_library.socket.echo_server import EchoTCPBlockingSocketServer
from holado_python.standard_library.socket.message_socket import MessageTCPSocketClient
from holado_core.common.handlers.wait import WaitFuncResultVerifying, WaitEndChange
from holado_core.common.exceptions.functional_exception import FunctionalException
from holado_python.standard_library.ssl.ssl import SslManager

logger = logging.getLogger(__name__)


def __get_scenario_context():
    return SessionContext.instance().get_scenario_context()

def __get_text_interpreter():
    return __get_scenario_context().get_text_interpreter()

def __get_variable_manager():
    return __get_scenario_context().get_variable_manager()



@Given(r"(?P<var_name>{Variable}) = certfile path for localhost")
def step_impl(context, var_name):
    """Return path to cert file for localhost stored in internal resources.
    Note: It is an autosigned certificate.
    """
    var_name = StepTools.evaluate_variable_name(var_name)
    
    cert_paths = SslManager.get_localhost_certificate()
    
    __get_variable_manager().register_variable(var_name, cert_paths[0])


@Given(r"(?P<var_name>{Variable}) = keyfile path for localhost")
def step_impl(context, var_name):
    """Return path to key file for localhost stored in internal resources.
    Note: It is an autosigned certificate.
    """
    var_name = StepTools.evaluate_variable_name(var_name)
    
    cert_paths = SslManager.get_localhost_certificate()
    
    __get_variable_manager().register_variable(var_name, cert_paths[1])




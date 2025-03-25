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



def configure(initialize_logging=True, log_level=None):
    from holado_logging.common.logging.log_config import LogConfig
    if log_level is None:
        import logging
        log_level = logging.INFO
        
    LogConfig.configure(initialize_logging=initialize_logging, log_level=log_level)
    
def dependencies():
    return None

def register():
    from holado.common.context.session_context import SessionContext
    from holado_logging.common.logging.log_manager import LogManager
    
    log_manager = LogManager()
    log_manager.initialize(log_on_console=True)
    
    SessionContext.instance().services.register_service_instance("log_manager", log_manager, SessionContext.instance())


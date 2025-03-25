
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
import ssl
from holado_core.common.exceptions.functional_exception import FunctionalException
from holado_core.common.tools.tools import Tools
from holado_json.ipc.json import set_object_attributes_with_json_dict
from holado_core.common.exceptions.technical_exception import TechnicalException
import os
import copy
from ssl import Purpose

logger = logging.getLogger(__name__)


class SslManager(object):
    """
    Helper for ssl module.
    
    It is implemented internally with standard library ssl.
    """
    
    @classmethod
    def new_ssl_context(cls, server_side=False, flat_kwargs=None):
        res = None
        
        if flat_kwargs is None:
            flat_kwargs = {}
        kwargs = copy.copy(flat_kwargs)
        
        try:
            activate_ssl = kwargs.pop('activate', True)
            if activate_ssl:
                purpose = Purpose.CLIENT_AUTH if server_side else Purpose.SERVER_AUTH
                res = ssl.create_default_context(purpose=purpose)
                
                if Tools.has_sub_kwargs(kwargs, 'context.'):
                    context_kwargs = Tools.pop_sub_kwargs(kwargs, 'context.')
                    
                    ciphers = context_kwargs.pop('ciphers', None)
                    if ciphers is not None:
                        res.set_ciphers(ciphers)
                    if Tools.has_sub_kwargs(context_kwargs, 'load_cert_chain.'):
                        load_cert_chain_kwargs = Tools.pop_sub_kwargs(context_kwargs, 'load_cert_chain.')
                        res.load_cert_chain(**load_cert_chain_kwargs)
                    if Tools.has_sub_kwargs(context_kwargs, 'load_verify_locations.'):
                        load_verify_locations_kwargs = Tools.pop_sub_kwargs(context_kwargs, 'load_verify_locations.')
                        res.load_verify_locations(**load_verify_locations_kwargs)
                    
                    # Set context attributes with remaining kwargs
                    if len(context_kwargs) > 0:
                        set_object_attributes_with_json_dict(res, context_kwargs)
        except Exception as exc:
            msg = f"Failed to create SSL context with parameters {flat_kwargs}: {exc}"
            logger.error(msg)
            raise TechnicalException(msg) from exc
        
        # Verify all kwargs were applied
        if len(kwargs) > 0:
            raise TechnicalException(f"Unmanaged ssl parameters: {kwargs}")
        
        return res
    
    @classmethod
    def get_localhost_certificate(cls):
        here = os.path.abspath(os.path.dirname(__file__))
        certfile_path = os.path.join(here, 'resources', 'certificates', 'localhost.crt')
        keyfile_path = os.path.join(here, 'resources', 'certificates', 'localhost.key')
        return (certfile_path, keyfile_path)


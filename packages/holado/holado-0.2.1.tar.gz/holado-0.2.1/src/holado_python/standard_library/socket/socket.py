
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
import socket
from _socket import SHUT_RDWR
from holado.common.handlers.object import DeleteableObject
import abc
from holado_core.common.exceptions.functional_exception import FunctionalException
from holado_core.common.tools.tools import Tools
from holado_python.standard_library.ssl.ssl import SslManager

logger = logging.getLogger(__name__)


class Socket(DeleteableObject):
    """
    Base class for socket objects.
    
    It is implemented internally with standard library socket.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        if name is None and create_ipv4_socket_kwargs is not None:
            if not set(create_ipv4_socket_kwargs.keys()).issuperset({'host', 'port'}):
                raise FunctionalException(f"Parameters 'host' and 'port' must be defined")
            name = f"{create_ipv4_socket_kwargs['host']}:{create_ipv4_socket_kwargs['port']}"
        
        super().__init__(name)
        self.__socket = None
        
        if create_ipv4_socket_kwargs is not None:
            self.create_ipv4_socket(**create_ipv4_socket_kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _delete_object(self):
        self.close()
    
    @property    
    def internal_socket(self) -> socket.socket:
        return self.__socket
    
    def _set_internal_socket(self, socket):
        self.__socket = socket
    
    @abc.abstractmethod
    def create_ipv4_socket(self, host, port, **kwargs):
        raise NotImplementedError()
    
    def close(self):
        if self.__socket is not None:
            try:
                self.__socket.shutdown(SHUT_RDWR)
            except OSError as exc:
                if 'Errno 107' in str(exc):
                    logger.info(f"Got following error on socket shutdown (known to appear sometimes at shutdown): {exc}")
                else:
                    raise exc
            self.__socket.close()
            self.__socket = None
    
    def read(self, bufsize=1024, **kwargs):
        res = self.internal_socket.recv(bufsize, **kwargs)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"[{self.name}] Received [{res}] (type: {type(res)})")
        return res
    
    def write(self, data_bytes, loop_until_all_is_sent=True, **kwargs):
        if loop_until_all_is_sent:
            # Note: no return is done, since sendall return None or raise an exception on error
            self.internal_socket.sendall(data_bytes, **kwargs)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"[{self.name}] Sent all [{data_bytes}] (type: {type(data_bytes)})")
        else:
            res = self.internal_socket.send(data_bytes, **kwargs)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"[{self.name}] Sent {res}/{len(data_bytes)} bytes of [{data_bytes}] (type: {type(data_bytes)})")
            return res
    
    def _new_ssl_context_if_required(self, server_side=False, **socket_kwargs):
        """Return a SSLContext if required, and the remaining socket kwargs.
        """
        res = None
        if Tools.has_sub_kwargs(socket_kwargs, 'ssl.'):
            ssl_kwargs = Tools.pop_sub_kwargs(socket_kwargs, 'ssl.')
            res = SslManager.new_ssl_context(server_side=server_side, flat_kwargs=ssl_kwargs)
        return res, socket_kwargs


class SocketClient(Socket):
    """
    Base class for socket clients.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
    



class SocketServer(Socket):
    """
    Base class for socket servers.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
    
    def accept(self):
        conn, addr = self.internal_socket.accept()
        res = Socket(name=f"[{self.name}] Connection with {addr}")
        res._set_internal_socket(conn)
        return res, addr
    
    @abc.abstractmethod
    def start(self, read_bufsize=1024, *, read_kwargs=None, write_kwargs=None):
        """Start server.
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _process_data(self, data):
        raise NotImplementedError()





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
from holado_python.standard_library.socket.socket import SocketClient, SocketServer
import abc
from holado_multitask.multithreading.loopfunctionthreaded import LoopFunctionThreaded

logger = logging.getLogger(__name__)


##########################################################################
## Clients
##########################################################################


class BlockingSocketClient(SocketClient):
    """
    Base class for blocking socket client.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
    

class TCPBlockingSocketClient(BlockingSocketClient):
    """
    TCP socket client.
    """
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
    
    def create_ipv4_socket(self, host, port, **kwargs):
        ssl_context, kwargs = self._new_ssl_context_if_required(**kwargs)
        
        sock = socket.create_connection((host, port), **kwargs)
        
        if ssl_context:
            sock = ssl_context.wrap_socket(sock, server_hostname=host, do_handshake_on_connect=False)
            # sock = ssl_context.wrap_socket(sock, server_hostname=host)
        self._set_internal_socket(sock)




##########################################################################
## Servers
##########################################################################


class BlockingSocketServer(SocketServer):
    """
    Base class for socket servers.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
        
        self.__start_thread = None
    
    def start(self, read_bufsize=1024, *, read_kwargs=None, write_kwargs=None):
        """Start server to wait a connection, and then listen data, process data, and send result.
        Note: current implementation is simple and supports only one connection at a time.
        """
        kwargs = {'read_bufsize':read_bufsize, 'read_kwargs':read_kwargs, 'write_kwargs':write_kwargs}
        self.__start_thread = LoopFunctionThreaded(self.wait_and_process_connection, kwargs=kwargs, register_thread=True, delay_before_run_sec=None)
        self.__start_thread.start()
    
    def stop(self):
        if self.__start_thread is not None:
            self.__start_thread.interrupt()
            self.__start_thread.join()
            self.__start_thread = None
    
    def wait_and_process_connection(self, read_bufsize=1024, *, read_kwargs=None, write_kwargs=None):
        """Wait a connection, and then listen data, process data, and send result.
        Note: current implementation is simple and supports only one connection at a time.
        """
        read_kwargs = read_kwargs if read_kwargs is not None else {}
        write_kwargs = write_kwargs if write_kwargs is not None else {}
        
        conn, _ = self.accept()
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"[{self.name}] New connection: {conn}")
        with conn:
            while True:
                data = conn.read(read_bufsize, **read_kwargs)
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"[{self.name}] Received: {data}")
                    
                if not data:
                    break
                result = self._process_data(data)
                
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"[{self.name}] Sending: {result}")
                conn.write(result, **write_kwargs)
    
    @abc.abstractmethod
    def _process_data(self, data):
        raise NotImplementedError()



class TCPBlockingSocketServer(BlockingSocketServer):
    """
    TCP socket server
    """
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
    
    def create_ipv4_socket(self, host, port, **kwargs):
        ssl_context, kwargs = self._new_ssl_context_if_required(server_side=True, **kwargs)
        
        sock = socket.create_server((host, port), **kwargs)
        
        if ssl_context:
            # sock = ssl_context.wrap_socket(sock, do_handshake_on_connect=False, server_side=True)
            sock = ssl_context.wrap_socket(sock, server_side=True)
        self._set_internal_socket(sock)


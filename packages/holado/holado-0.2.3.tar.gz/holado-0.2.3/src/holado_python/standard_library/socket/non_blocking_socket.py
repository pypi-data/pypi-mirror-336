
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
from holado_python.standard_library.socket.socket import SocketClient
import abc
from holado_multitask.multithreading.loopfunctionthreaded import LoopFunctionThreaded
import selectors
import types
import threading

logger = logging.getLogger(__name__)


##########################################################################
## Clients
##########################################################################


class NonBlockingSocketClient(SocketClient):
    """
    Base class for blocking socket client.
    """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        self.__selector = selectors.DefaultSelector()
        
        self.__data_lock = threading.Lock()
        self.__data = types.SimpleNamespace(
            in_bytes=b"",
            out_bytes=b"",
        )
        
        # Note: __selector and __data must be defined before, since Socket.__init__ can execute create_ipv4_socket
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
        
        self.__start_thread = None

    def _delete_object(self):
        self.stop()
        if self.internal_socket:
            self.__selector.unregister(self.internal_socket)
        
        super()._delete_object()
    
    def _register_socket(self, sock):
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.__selector.register(sock, events, data=self.__data)
    
    @property
    def _data_lock(self):
        return self.__data_lock
    
    @property
    def _data(self):
        return self.__data
    
    def start(self, *, read_bufsize=1024, read_kwargs=None, write_kwargs=None):
        """Start client event loop.
        """
        kwargs = {'read_bufsize':read_bufsize, 'read_kwargs':read_kwargs, 'write_kwargs':write_kwargs}
        self.__start_thread = LoopFunctionThreaded(self._wait_and_process_events, kwargs=kwargs, register_thread=True, delay_before_run_sec=None)
        self.__start_thread.start()
    
    def stop(self):
        if self.__start_thread is not None:
            self.__start_thread.interrupt()
            self.__start_thread.join()
            self.__start_thread = None
    
    def _wait_and_process_events(self, *, read_bufsize=1024, read_kwargs=None, write_kwargs=None):
        events = self.__selector.select(timeout=None)
        for key, mask in events:
            self._service_connection(key, mask, read_bufsize=read_bufsize, read_kwargs=read_kwargs, write_kwargs=write_kwargs)

    def _service_connection(self, key, mask, *, read_bufsize=1024, read_kwargs=None, write_kwargs=None):
        read_kwargs = read_kwargs if read_kwargs is not None else {}
        write_kwargs = write_kwargs if write_kwargs is not None else {}
        
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(read_bufsize, **read_kwargs)
            if recv_data:
                with self.__data_lock:      # data is self.__data
                    data.in_bytes += recv_data
        if mask & selectors.EVENT_WRITE:
            with self.__data_lock:      # data is self.__data
                if data.out_bytes:
                    sent = sock.send(data.out_bytes)
                    data.out_bytes = data.out_bytes[sent:]
    
    @property
    def received_data_size(self):
        with self.__data_lock:
            res = len(self.__data.in_bytes)
        return res
    
    def read(self, bufsize=1024):
        with self.__data_lock:
            if self.__data.in_bytes:
                res = self.__data.in_bytes[:bufsize]
                self.__data.in_bytes = self.__data.in_bytes[bufsize:]
            else:
                res = b''
        return res
    
    def write(self, data_bytes):
        with self.__data_lock:
            self.__data.out_bytes += data_bytes


class TCPNonBlockingSocketClient(NonBlockingSocketClient):
    """
    TCP socket client.
    """
    
    def __init__(self, *, name=None, create_ipv4_socket_kwargs=None):
        super().__init__(name=name, create_ipv4_socket_kwargs=create_ipv4_socket_kwargs)
    
    def create_ipv4_socket(self, host, port, **kwargs):
        ssl_context, kwargs = self._new_ssl_context_if_required(**kwargs)
        
        sock = socket.create_connection((host, port), **kwargs)
        sock.setblocking(False)
        
        if ssl_context:
            sock = ssl_context.wrap_socket(sock, server_hostname=host, do_handshake_on_connect=False)
        self._set_internal_socket(sock)
        
        # Register socket
        self._register_socket(sock)








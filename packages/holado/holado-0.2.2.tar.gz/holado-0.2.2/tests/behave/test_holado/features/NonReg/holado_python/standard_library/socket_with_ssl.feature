@testing_solution
@python
@socket
@ssl
Feature: Test python socket steps with ssl

    @blocking_socket
    Scenario: Server and client with blocking connections

        ### PRECONDITIONS - BEGIN
        Given begin preconditions
        
        # Get files of a self-signed certificate
        Given CERTFILE_PATH = certfile path for localhost
        Given KEYFILE_PATH = keyfile path for localhost
        
        # Use echo server with a blocking connection
        Given PORT = first available anonymous port
        Given SERVER = new echo TCP socket server
            | Name                                   | Value         |
            | 'host'                                 | 'localhost'   |
            | 'port'                                 | PORT          |
            | 'ssl.activate'                         | True          |
            | 'ssl.context.ciphers'                  | 'SHA256'      |
            | 'ssl.context.load_cert_chain.certfile' | CERTFILE_PATH |
            | 'ssl.context.load_cert_chain.keyfile'  | KEYFILE_PATH  |
        
        # Create a TCP client with a blocking connection
        Given CLIENT = new TCP socket client
            | Name                                       | Value         |
            | 'host'                                     | 'localhost'   |
            | 'port'                                     | PORT          |
            | 'ssl.activate'                             | True          |
            | 'ssl.context.check_hostname'               | True          |
            | 'ssl.context.load_verify_locations.cafile' | CERTFILE_PATH |
        
        Given end preconditions
        ### PRECONDITIONS - END
        
        # Start echo server
        When start (socket server: SERVER)
        
        # Write data and verify result is identical
        When write b'\x01\x02' (socket: CLIENT)
        When DATA = read (socket: CLIENT)
        Then DATA == b'\x01\x02'
        
        When write b'\x11\x21' (socket: CLIENT)
        When DATA = read (socket: CLIENT)
        Then DATA == b'\x11\x21'
        
        # Stop server
        #When stop (socket server: SERVER)


    @non_blocking_socket
    Scenario: Server and client with non blocking connection

        ### PRECONDITIONS - BEGIN
        Given begin preconditions
        
        # Get files of a self-signed certificate
        Given CERTFILE_PATH = certfile path for localhost
        Given KEYFILE_PATH = keyfile path for localhost
        
        # Use echo server with a blocking connection
        Given PORT = first available anonymous port
        Given SERVER = new echo TCP socket server
            | Name                                   | Value         |
            | 'host'                                 | 'localhost'   |
            | 'port'                                 | PORT          |
            | 'ssl.activate'                         | True          |
            | 'ssl.context.ciphers'                  | 'SHA256'      |
            | 'ssl.context.load_cert_chain.certfile' | CERTFILE_PATH |
            | 'ssl.context.load_cert_chain.keyfile'  | KEYFILE_PATH  |
        
        # Create a TCP client with a blocking connection
        Given CLIENT = new TCP socket client
            | Name                                       | Value         |
            | 'host'                                     | 'localhost'   |
            | 'port'                                     | PORT          |
            | 'blocking'                                 | False         |
            | 'ssl.activate'                             | True          |
            | 'ssl.context.check_hostname'               | True          |
            | 'ssl.context.load_verify_locations.cafile' | CERTFILE_PATH |
        
        Given end preconditions
        ### PRECONDITIONS - END
        
        # Start echo server & client
        When start (socket server: SERVER)
        When start (socket client: CLIENT)
        
        # Write data and verify result is identical
        When write b'\x01\x02' (socket: CLIENT)
        When wait socket CLIENT stops to receive data (window: 0.1 s)
        When DATA = read (socket: CLIENT)
        Then DATA == b'\x01\x02'
        
        When write b'\x11\x21' (socket: CLIENT)
        When wait socket CLIENT stops to receive data (window: 0.1 s)
        When DATA = read (socket: CLIENT)
        Then DATA == b'\x11\x21'
        
        # Stop server & client
        #When stop (socket server: SERVER)
        When stop (socket client: CLIENT)



    @message_socket
    Scenario: Echo server and message client (with underlying non blocking connection)

        ### PRECONDITIONS - BEGIN
        Given begin preconditions
        
        # Get files of a self-signed certificate
        Given CERTFILE_PATH = certfile path for localhost
        Given KEYFILE_PATH = keyfile path for localhost
        
        # Use echo server with a blocking connection
        Given PORT = first available anonymous port
        Given SERVER = new echo TCP socket server
            | Name                                   | Value         |
            | 'host'                                 | 'localhost'   |
            | 'port'                                 | PORT          |
            | 'ssl.activate'                         | True          |
            | 'ssl.context.ciphers'                  | 'SHA256'      |
            | 'ssl.context.load_cert_chain.certfile' | CERTFILE_PATH |
            | 'ssl.context.load_cert_chain.keyfile'  | KEYFILE_PATH  |
        
        # Create a message client
        Given CLIENT = new message TCP socket client
            | Name                                       | Value         |
            | 'host'                                     | 'localhost'   |
            | 'port'                                     | PORT          |
            | 'separator'                                | b'\n'         |
            | 'ssl.activate'                             | True          |
            | 'ssl.context.check_hostname'               | True          |
            | 'ssl.context.load_verify_locations.cafile' | CERTFILE_PATH |
        
        Given end preconditions
        ### PRECONDITIONS - END
        
        # Start echo server & message client
        When start (socket server: SERVER)
        When start (socket client: CLIENT)
        
        # Write data and verify result is identical
        When write message b'\x01\x02' (socket: CLIENT)
        When write message b'\x11\x21' (socket: CLIENT)
        
        # Verify received messages
        When wait socket CLIENT stops to receive messages (window: 0.1 s)
        When MESSAGES = received messages (socket: CLIENT)
        Then MESSAGES is list
            | b'\x01\x02' |
            | b'\x11\x21' |
        
        When MESSAGES_2 = received messages (socket: CLIENT)
        Then MESSAGES_2 == MESSAGES
        
        # Verify pop messages functionality
        When MSG_1 = read message (socket: CLIENT)
        Then MSG_1 == b'\x01\x02'
        When MESSAGES_3 = received messages (socket: CLIENT)
        Then MESSAGES_3 is list
            | b'\x11\x21' |

        When MSG_2 = read message (socket: CLIENT)
        Then MSG_2 == b'\x11\x21'
        When MESSAGES_4 = received messages (socket: CLIENT)
        Then MESSAGES_4 is empty list
        
        # Stop server & client
        #When stop (socket server: SERVER)
        When stop (socket client: CLIENT)




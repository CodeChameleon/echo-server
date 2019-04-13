import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    sock.connect(server_address)
    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = []

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(msg.encode('utf-8'))

        while True:
            chunk = sock.recv(16)
            received_message.append(chunk.decode('utf8'))
            print('received "{0}"'.format(received_message[-1]), file=log_buffer)
            if len(chunk) < 16:
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        print('closing socket', file=log_buffer)
        sock.close()

    return ''.join(received_message)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)

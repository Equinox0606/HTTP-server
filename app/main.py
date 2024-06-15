import socket
import threading
import os
import sys
import gzip
import io

def parse_request(request):
    lines = request.split(b"\r\n")
    request_line = lines[0]
    headers = {line.split(b": ")[0].decode().lower(): line.split(b": ")[1].decode() for line in lines[1:] if b": " in line}
    verb, path, version = request_line.split(b" ")
    body = b"\r\n".join(lines[len(headers)+2:]).decode()
    return verb.decode(), path.decode(), headers, body

def gzip_compress(data):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(data.encode())
    return buf.getvalue()

def handle_get(path_segments, headers):
    if len(path_segments) == 1 and path_segments[0] == '':
        return "HTTP/1.1 200 OK\r\n\r\n".encode()

    if len(path_segments) == 2 and path_segments[0] == 'echo':
        body = path_segments[1]
        accept_encoding = headers.get('accept-encoding', '').lower().split(',')
        accept_encoding = [enc.strip() for enc in accept_encoding]
        if 'gzip' in accept_encoding:
            compressed_body = gzip_compress(body)
            content_length = len(compressed_body)
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Encoding: gzip\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {content_length}\r\n"
                f"\r\n"
            ).encode() + compressed_body
        else:
            content_length = len(body)
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {content_length}\r\n"
                f"\r\n"
                f"{body}"
            ).encode()
        return response

    if len(path_segments) == 1 and path_segments[0] == 'user-agent':
        user_agent = headers.get('user-agent', 'unknown')
        body = user_agent
        content_length = len(body)
        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/plain\r\n"
            f"Content-Length: {content_length}\r\n"
            f"\r\n"
            f"{body}"
        ).encode()
        return response

    if len(path_segments) == 2 and path_segments[0] == 'files':
        filename = path_segments[1]
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_contents = f.read()
                content_length = len(file_contents)
                return f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {content_length}\r\n\r\n".encode() + file_contents
        else:
            return "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    return "HTTP/1.1 404 Not Found\r\n\r\n".encode()

def handle_post(path_segments, headers, body, directory):
    if len(path_segments) == 2 and path_segments[0] == 'files':
        filename = path_segments[1]
        file_path = os.path.join(directory, filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        print(f"Received body: {body}")

        with open(file_path, 'wb') as f:
            f.write(body.encode())

        return "HTTP/1.1 201 Created\r\n\r\n".encode()

    return "HTTP/1.1 404 Not Found\r\n\r\n".encode()

def get_response(request, directory):
    verb, path, headers, body = parse_request(request)
    path_segments = path.strip('/').split('/')

    if verb == "GET":
        return handle_get(path_segments, headers)
    
    elif verb == "POST":
        return handle_post(path_segments, headers, body, directory)
    
    return "HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode()

def handle_request(connection, address, directory):
    try:
        print(f"Handling request from {address}")
        request = connection.recv(1024)
        print(f"Received request: {request.decode()}")
        response = get_response(request, directory)
        connection.sendall(response)
        print("Response sent successfully")
    except Exception as e:
        print(f"Error handling request from {address}: {e}")
    finally:
        connection.close()
        print(f"Connection with {address} closed")

def main(directory):
    print("Logs from your program will appear here!")
    print("Starting server...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 4221))
    server_socket.listen()

    def client_thread(connection, address, directory):
        handle_request(connection, address, directory)

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=client_thread, args=(conn, addr, directory)).start()
    except KeyboardInterrupt:
        print("Server is shutting down")
    except Exception as e:
        print(f"Server encountered an error: {e}")
    finally:
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    default_directory = os.getcwd()  # Default to current working directory
    directory = default_directory

    if len(sys.argv) == 3 and sys.argv[1] == '--directory':
        directory = sys.argv[2]
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory")
            sys.exit(1)

    main(directory)

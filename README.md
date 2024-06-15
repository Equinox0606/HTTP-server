# Simple HTTP Server with Compression

This project is a simple HTTP server implemented in Python. The primary motivation behind this project was to learn how to create an HTTP server from scratch, handle various HTTP methods, and implement response compression using gzip.

## Features

- **Basic HTTP Methods**: Supports GET and POST requests.
- **File Handling**: Ability to serve files and handle file uploads.
- **Header Parsing**: Parses and handles HTTP headers correctly, including case-insensitivity.
- **Response Compression**: Supports gzip compression based on the `Accept-Encoding` header.
- **Concurrent Connections**: Handles multiple client connections concurrently using threading.

## Learning Outcomes

- **HTTP Protocol**: Gained a deep understanding of the HTTP protocol, including request/response structure and header handling.
- **Socket Programming**: Learned how to use Python's `socket` module to create a server that listens for client connections.
- **Data Compression**: Implemented gzip compression for HTTP responses, learning about the gzip format and its integration in HTTP communication.
- **Threading**: Implemented concurrent request handling using Python's `threading` module to manage multiple client connections simultaneously.
- **Error Handling**: Improved error handling techniques to manage various edge cases and ensure the server remains robust.

## How to Run

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/your-username/simple-http-server.git
    cd simple-http-server
    ```

2. **Run the Server**:
    ```sh
    python server.py --directory /path/to/serve/files
    ```

3. **Make Requests**:
    - **GET Request**:
        ```sh
        curl -v http://localhost:4221/echo/foo
        ```
    - **POST Request**:
        ```sh
        curl -v -X POST http://localhost:4221/files/yourfile -H "Content-Length: 13" -d 'Hello, world!'
        ```

4. **Test Gzip Compression**:
    ```sh
    curl -v http://localhost:4221/echo/foo -H "Accept-Encoding: gzip"
    ```

## Project Structure

- `app/main.py`: The main server script containing all the logic for handling requests, parsing headers, managing threads, and compressing responses.
- `README.md`: This file.

## Future Enhancements

- **Additional Methods**: Add support for more HTTP methods such as PUT and DELETE.
- **Advanced Features**: Implement more advanced HTTP features like HTTPS, session management, and cookie handling.
- **Performance Optimization**: Optimize the server for better performance and scalability.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

Feel free to explore, contribute, and provide feedback!

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

def run(server_class=ThreadingHTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
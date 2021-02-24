from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import click
import os

@click.command()
@click.option('--port',
              default=8888,
              help='Listening Port')
def run(port, server_class=ThreadingHTTPServer, handler_class=SimpleHTTPRequestHandler):
    target_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.chdir(target_dir)

    server_address = ('', port)
    print("Server started at localhost:" + str(port))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
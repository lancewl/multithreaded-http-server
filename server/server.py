from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import click

@click.command()
@click.option('--port',
              default=8888,
              help='Listening Port')
def run(port, server_class=ThreadingHTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
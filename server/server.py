from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from http import HTTPStatus
import urllib.parse
import html
import sys
import io
import os
import click
import json


class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Override the original file listing method

        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = {}
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r[displayname] = {}
            r[displayname]["link"] = urllib.parse.quote(linkname, errors='surrogatepass')
        
        enc = sys.getfilesystemencoding()
        encoded = json.dumps(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        return f

@click.command()
@click.option('--port',
              default=8888,
              help='Listening Port')
def run(port, server_class=ThreadingHTTPServer, handler_class=MyHttpRequestHandler):
    target_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.chdir(target_dir)

    server_address = ('', port)
    print("Server started at localhost:" + str(port))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
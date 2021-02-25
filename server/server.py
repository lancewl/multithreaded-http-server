from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from http import HTTPStatus
import urllib.parse
import sys
import io
import os
import hashlib
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
            md5 = ""
            nametype = ""
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
                nametype = "dir"
            if os.path.islink(fullname):
                displayname = name + "@"
                nametype = "link"
                # Note: a link to a directory displays with @ and links with /
            if os.path.isfile(fullname):
                md5 = hashlib.md5(open(linkname,'rb').read()).hexdigest()
                nametype = "file"
            r[displayname] = {}
            r[displayname]["link"] = urllib.parse.quote(linkname, errors='surrogatepass')
            r[displayname]["md5"] = md5
            r[displayname]["type"] = nametype
        
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
@click.option('--dir',
              default="data",
              help='Serving directory relative to current directory')
def run(port, dir, server_class=ThreadingHTTPServer, handler_class=MyHttpRequestHandler):
    target_dir = os.path.join(os.path.dirname(__file__), dir)
    os.chdir(target_dir)

    server_address = ('', port)
    print("Server started at localhost:" + str(port))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
from __future__ import division, with_statement

from contextlib import closing
import json
import os
import sys
import time
import tarfile
from urllib.request import urlopen
import http.server
import socketserver
from threading import Thread
import subprocess
import webbrowser


PORT = 9841
if getattr(sys, 'frozen', False):
    static_dir = os.path.dirname(sys.executable)
else:
    static_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.abspath(static_dir)

def makedirs(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def get_platform():
    name = sys.platform
    if name.startswith('darwin'):
        name = 'darwin64'
    elif name.startswith('linux'):
        import platform
        if platform.architecture()[0] == '64bit':
            name = 'linux64'
        else:
            name = 'linux32'
    return name

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, 'OK')
        self.send_header('Allow', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_GET(self):

        if self.path == '/status':
            content = json.dumps(self.server.install.status).encode()
            self.send_response(200, 'OK')
        else:
            path = os.path.join(static_dir, 'index.html' if self.path == '/' else self.path[1:])
            if os.path.exists(path):
                with open(path, 'rb') as fd:
                    content = fd.read()
                self.send_response(200, 'OK')
                content_type = {
                    'html': 'text/html',
                    'png': 'image/png',
                    'svg': 'image/svg+xml',
                    'txt': 'text/plain',
                }.get(path.split('.')[-1], 'txt')
                self.send_header('Content-Type', content_type)
            else:
                self.send_response(404, 'not found')
                content = b'404 not found'
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        pass

class Install(Thread):

    release_url = "http://downloads.openmedialibrary.com/release.json"
    status = {
        'step': 'Downloading...'
    }

    def __init__(self, target, httpd):
        target = os.path.normpath(os.path.join(os.path.abspath(target)))
        self.target = target
        self.httpd = httpd
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        webbrowser.open('http://127.0.0.1:%s'%PORT)
        target = self.target
        makedirs(target)
        os.chdir(target)
        self.status["step"] = 'Downloading...'
        release = self.get_release()
        self.status["release"] = release
        self.status["progress"] = 0
        platform = get_platform()
        if 'platform_win32' not in release['modules']:
            release['modules']['platform_win32'] = {
                'name': 'platform_win32-20160201-3-3d473b8.tar.bz2',
                'version': '20160201-3-3d473b8.tar.bz2',
                'platform': 'win32',
            }
        for module in sorted(release['modules']):
            if release['modules'][module].get('platform', platform) == platform:
                package_tar = release['modules'][module]['name']
                url = self.release_url.replace('release.json', package_tar)
                self.download(url, package_tar)
        self.status["step"] = 'Installing...'
        for module in sorted(release['modules']):
            if release['modules'][module].get('platform', platform) == platform:
                package_tar = release['modules'][module]['name']
                tar = tarfile.open(package_tar)
                tar.extractall()
                tar.close()
                os.unlink(package_tar)
        makedirs('data')
        with open('data/release.json', 'w') as fd:
            json.dump(release, fd, indent=2)
        self.status = {"relaunch": True}
        open_oml(target)
        time.sleep(5)
        self.httpd.shutdown()

    def download(self, url, filename):
        dirname = os.path.dirname(filename)
        if dirname:
            makedirs(dirname)
        with open(filename, 'wb') as f:
            with closing(urlopen(url)) as u:
                size = int(u.headers.get('content-length', 0))
                self.status["size"] = size
                available = 0
                data = u.read(4096)
                while data:
                    if size:
                        available += len(data)
                    f.write(data)
                    data = u.read(4096)

    def get_release(self):
        with closing(urlopen(self.release_url)) as u:
            data = json.loads(u.read().decode())
        return data

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class InstallServer(Thread):
    def __init__(self, target):
        self.target = target
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        httpd = Server(("127.0.0.1", PORT), Handler)
        install = Install(self.target, httpd)
        httpd.install = install
        httpd.serve_forever()

def open_oml(base):
    python = os.path.join(base, 'platform_win32', 'pythonw.exe')
    pid = os.path.join(base, 'data', 'openmedialibrary.pid')
    oml = os.path.join(base, 'openmedialibrary')
    subprocess.Popen([python, 'oml', 'server', pid], cwd=oml, start_new_session=True)

def run(target):
    return InstallServer(target)

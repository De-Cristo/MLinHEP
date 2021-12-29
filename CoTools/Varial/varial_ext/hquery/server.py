from cherrypy.lib.static import serve_file
import cherrypy
import string
import socket
import random
import time
import os
join = os.path.join
_ssldir = join(os.environ['HOME'], '.hQuery')
_sslcrt = join(_ssldir, 'hQuery.crt')
_sslkey = join(_ssldir, 'hQuery.key')

redirect = """\
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="1;url=index.html">
        <script type="text/javascript">
            window.location.href = "index.html"
        </script>
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically,
        follow this <a href='index.html'>link to index.html</a>
    </body>
</html>
"""
session_token = ''.join(
    random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(20))
session_token = session_token[:10] + 'hQuery' + session_token[10:]

def load_html(args):
    path = '/'.join(args)
    real_path = 'sections/' + path
    if os.path.isdir(real_path):
        real_path = join(real_path, 'index.html')
        path = join(path, 'index.html')

    if not (path.endswith('index.html') and os.path.isfile(real_path)):
        raise cherrypy.NotFound()

    with open(real_path) as f:
        return path, f.read()


class WebService(object):
    exposed = True

    def __init__(self, engine, no_session):
        self.engine = engine
        self.path = os.path.abspath(os.getcwd()) + '/sections'
        self.use_session = not no_session

    def GET(self, *args, **kws):
        if self.use_session and 'auth' not in cherrypy.session:
            if kws.get('s', '') == session_token:
                cherrypy.session['auth'] = True
            else:
                raise cherrypy.HTTPError(
                    '403 Forbidden',
                    'hQuery token unavaialbe or incorrect. Please restart the '
                    'server to get an URL with a fresh token.'
                )

        if not args:
            return redirect
        elif any(args[-1].endswith(t) for t in (
            '.png', '.json', '.rt', 'rootjs.html'
        )):
            return serve_file(join(self.path, *args))
        elif args[-1].endswith('index.html'):
            return self.engine.get(*load_html(args))
        else:
            raise cherrypy.NotFound()

    def POST(self, *args, **kws):
        self.engine.post(args, kws)
        return self.engine.get(*load_html(args))

    def PUT(self, *args, **kws):
        pass  # using html forms only

    def DELETE(self, *args, **kws):
        pass  # using html forms only


def _create_ssl_keys():
    from OpenSSL import crypto

    if os.path.exists(_sslcrt) and os.path.exists(_sslkey):
        return
    else:
        if not os.path.exists(_ssldir):
            os.mkdir(_ssldir)
            os.system('chmod 700 %s' % _ssldir)

    # generate keypair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    crt = crypto.X509()
    crt.set_serial_number(int(time.time()))
    crt.gmtime_adj_notBefore(0)
    crt.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)  # valid for ten years
    crt.set_issuer(crt.get_subject())
    crt.set_pubkey(key)
    crt.sign(key, 'sha1')

    # write to disk
    with open(_sslcrt, 'wt') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, crt))
    with open(_sslkey, 'wt') as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    os.system('chmod 600 %s' % _sslkey)
    os.system('chmod 644 %s' % _sslcrt)


def find_port(port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def test_port(num):
        try:
            soc.bind(('', num))
            return True
        except socket.error:
            return False

    while not test_port(port):
        port += 1
    soc.listen(1)
    soc.close()
    return port


conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/html')],

        'tools.sessions.on': True,
        'tools.sessions.storage_type': 'file',
        'tools.sessions.storage_path': os.path.abspath(os.getcwd()),
        'tools.sessions.timeout': 24*60,
    },
    'global': {
        'server.ssl_module': 'pyopenssl',
        'server.ssl_certificate': _sslcrt,
        'server.ssl_private_key': _sslkey,
        'server.socket_host': '0.0.0.0',
        'server.socket_port': find_port(8080),
        'log.screen': False,
        'log.error_file': 'hQuery.server.error.log',
        'log.access_file': 'hQuery.server.access.log',
    }
}


def start(engine, no_session):
    # check / create keys
    _create_ssl_keys()

    # print browser-links
    url = 'https://{}:{}/?s={}'.format(
        '{}',
        conf['global']['server.socket_port'],
        '' if no_session else session_token
    )
    print '='*80
    print 'hQuery is ready at:'
    print url.format(socket.gethostname())
    print url.format('localhost')
    print '='*80

    # start serving
    cherrypy.quickstart(WebService(engine, no_session), '/', conf)

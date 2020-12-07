from http.client import HTTPSConnection, HTTPException
from urllib.parse import urlparse
from time import time
import json

class Response:
    def __init__(self, status, headers, content, conn):
        self.status = status
        self.headers = headers
        self.content = content
        self.conn = conn

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return self

    @property
    def text(self):
        return self.content.decode("UTF-8")

    def json(self):
        return json.loads(self.content)

class ConnectionManager:
    proxy_url: str
    timeout: float
    max_age: float

    def __init__(self, proxy_url=None, timeout=5, retries=1, max_age=3600):
        self.proxy_url = proxy_url
        self.timeout = timeout
        self.retries = retries
        self.max_age = max_age
        self._conn_map = {}
        self._proxy = proxy_url and urlparse(proxy_url)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.clear()

    def __del__(self):
        self.clear()

    def clear(self):
        for conn, _ in self._conn_map.values():
            self.close(conn)

    def close(self, conn):
        conn.close()
        for k, v in self._conn_map.items():
            if v == conn:
                del self._conn_map[k]
                break

    def _create_conn(self, host, port):
        kw = dict(timeout=self.timeout)

        if self._proxy:
            conn = HTTPSConnection(self._proxy.hostname, self._proxy.port, **kw)
            conn.set_tunnel(host, port)
        else:
            conn = HTTPSConnection(host, port, **kw)
        
        conn.connect()
        return (conn, time())

    def get_conn(self, host: str, port: int=443, force: bool=False) \
        -> HTTPSConnection:
        host_key = "%s:%d" % (host.lower(), port)
        conn = created = None

        if not force and (c := self._conn_map.get(host_key)):
            conn, created = c
        
        if not conn or time()-created >= self.max_age:
            if conn: conn.close()
            conn, created = self._create_conn(host, port)
            self._conn_map[host_key] = (conn, created)
        
        return conn
    
    def request(self,
            method: str,
            url: str,
            data: bytes = None,
            headers: dict = {},
            _retries=0) -> Response:
        parsed = urlparse(url)
        conn = None

        if isinstance(data, str):
            data = data.encode("UTF-8")

        print(data)
        
        try:
            conn = self.get_conn(parsed.hostname)
            conn.putrequest(method, url, True, True)
            conn.putheader("Host", parsed.hostname)
            if data:
                conn.putheader("Content-Length", len(data))
            for k, v in headers.items():
                conn.putheader(k, v)
            conn.endheaders()
            if data:
                conn.send(data)
            resp = conn.getresponse()
            content = resp.read()
            return Response(resp.status, resp.headers, content, conn)
        
        except HTTPException:
            if conn:
                self.close(conn)
            _retries += 1
            if _retries-1 < self.retries:
                return self.request(method, url, data, headers, _retries)
            else:
                raise
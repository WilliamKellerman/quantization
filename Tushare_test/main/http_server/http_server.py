from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from main.quantization.quant_volume import QuantVolume

data = {'result': 'this is a test'}
host = ('localhost', 8888)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if '/' == self.path:
            quant = QuantVolume()
            quant.calc()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == '__main__':
    server = HTTPServer(host, RequestHandler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

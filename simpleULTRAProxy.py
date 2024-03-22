# A proxy just for the SPOKE API
from socketserver import ForkingTCPServer
import http.server 
import urllib.request

PORT = 9097

URL_REQUIREMENT=['https://www.dropbox.com','https://zenodo.org','https://raw.githubusercontent.com','reltrans.s3.us-east-2.amazonaws.com']

class MyProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url=self.path[1:] # remove trailing /

        good_url=False
        for s in URL_REQUIREMENT:
            if url.find(s) != -1:
                good_url=True
        if not good_url:
            self.send_response(403)
            print(f"Rejecting URL because it does not have the the required string")
        else:
            self.send_response(200)
            self.end_headers()
            self.copyfile(urllib.request.urlopen(url), self.wfile)

httpd = ForkingTCPServer(('', PORT), MyProxy)
print (f"Now serving at {PORT}")
httpd.serve_forever()


                      
                 

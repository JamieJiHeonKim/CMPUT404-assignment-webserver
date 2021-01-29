#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        typeOfRequest = self.data.decode('utf-8').split(' ')[0]
        file_name = self.data.decode('utf-8').split(" ")[1]
        url = os.path.abspath(__file__)
        homeDir = os.path.dirname(url)

        # if the request type is GET, direct to index.html
        if typeOfRequest == "GET":

            # handles redirect and proper direcroty
            if ".." not in file_name.split("/") and os.path.exists(homeDir + "/www" + file_name):
                if file_name == "/deep":
                    self.page_301()
                    return
                if file_name[-1] == "/":
                    url = homeDir + "/www" + file_name + "index.html"
                else:
                    url = homeDir + "/www" + file_name
            else:
                self.page_404()

            # handles html and css
            if os.path.isdir("/www" + file_name):
                url = file_name + "index.html"
            content_type = url.split(".")[-1]
            if content_type == "css":
                content_type = "css"
                self.page_200(url, content_type)
            else:
                self.page_200(url, content_type)

        # handles different requests
        else:
            self.page_405()

    def page_200(self, file_path, content_type):
        # prevent broken pipe
        with open(file_path, "r") as lines:
            content = lines.read()
        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/" + content_type + "\n\n", "utf-8"))
        self.request.sendall(bytearray(content + "\n\n", "utf-8"))


        #for line in path.readlines():
        #    self.request.sendall(str.encode(""+line+"", "utf-8"))
        #    line = path.read(1024)
        #path.close()



    def page_301(self):
        body = ("<html><h>301 Moved Permanently</h></html>")
        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\n", "utf-8"))
        self.request.sendall(bytearray("Location: http://127.0.0.1:8080/deep/\n\n" + body + "\n", "utf-8"))

    def page_404(self):
        body = ("<html><h>404 Not Found</h></html>")
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\n\n" + body, "utf-8"))

    def page_405(self):
        body = ("<html><h><405 Method Not Allowed</h></html>")
        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\n\n" + body, "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

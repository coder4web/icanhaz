#!/usr/bin/env python
#
# Copyright 2012 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from flask import Flask, request
import re
import shlex
import socket
import subprocess

app = Flask(__name__)
app.debug=True


@app.route("/")
def icanhazafunction():
    if 'icanhazptr' in request.host:
        # The request is for *.icanhazptr.com
        try:
            output = socket.gethostbyaddr(request.remote_addr)
            result = output[0]
        except:
            result = request.remote_addr
    elif 'icanhaztrace' in request.host:
        # The request is for *.icanhaztraceroute.com
        valid_ip = False
        try:
            socket.inet_pton(socket.AF_INET, request.remote_addr)
            valid_ip = True
        except socket.error:
            pass
        try:
            socket.inet_pton(socket.AF_INET6, request.remote_addr)
            valid_ip = True
        except socket.error:
            pass
        if valid_ip:
            tracecmd = shlex.split("traceroute -q 1 -w 1 %s" %
                request.remote_addr)
            result = subprocess.Popen(tracecmd,
                stdout=subprocess.PIPE).communicate()[0].strip()
        else:
            result = request.remote_addr
    else:
        # The request is for *.icanhazip.com or something we don't recognize
        result = request.remote_addr
    return "%s\n" % result

if __name__ == "__main__":
    app.run()

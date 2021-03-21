#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys, os, datetime, re, urllib, shutil
import socket
import socketserver
import threading

from helpers import *
from statics import _statics
import mimeLib

if _statics['debug']:
    print('!!! Debug mode !!!')

def initdirs():
    md = lambda s: os.makedirs(s, exist_ok=True)
    def cf(s):
        f = open(s, 'ab')
        f.write(b'')
        f.close()
    md('./database/')
    cf('./database/records.csv')
    cf('./database/members.csv')

initdirs()

can_get_apikey = True   # Only allow apikey to be get once, i.e. when front-end starts up

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        path = recover(self.path)
        v = urlvar(path)
        if len(path) >= 2:
            if path[0:2] == '/~':
                if v['action'] == 'get_apikey':
                    global can_get_apikey
                    if can_get_apikey or _statics['debug']:
                        self.send_response(200)
                        self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                        self.end_headers()
                        self.wfile.write(_statics['apikey'].encode('utf-8'))
                        can_get_apikey = False
                    else:
                        self.send_response(403)
                        self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                        self.end_headers()
                        self.wfile.write(b'Forbidden')
                    return
                if v['apikey'] != _statics['apikey']:
                    self.send_response(403)
                    self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                    self.end_headers()
                    self.wfile.write(b'Forbidden')
                    return
                if v['action'] == 'shutdown':
                    exit(0)
                    return
                if v['action'] == 'get_file':
                    self.send_response(200)
                    self.send_header('Content-Type', mimeLib.getmime(path))
                    self.end_headers()
                    filename = v['file']
                    with open(filename, 'rb') as f:
                        while True:
                            data = f.read(_statics['buffer_size'])
                            if data:
                                self.wfile.write(data)
                            else:
                                break
                    return
                elif v['action'] == 'write_record':
                    self.send_response(200)
                    self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                    self.end_headers()
                    record = v['record']
                    with open('./database/records.csv', 'a', encoding='utf-8') as f:
                        f.write(record + '\n')
                    self.wfile.write(b'OK')
                    return
                elif v['action'] == 'get_record':
                    item_barcode = v['code']
                    f = open('./database/records.csv', 'r', encoding='utf-8')
                    while True:
                        line = f.readline()
                        if line:
                            if line == '\n':
                                continue
                            barcode, item, unit, price = line.split('\n')[0].split(',')
                            if item_barcode == barcode:
                                self.send_response(200)
                                self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                                self.end_headers()
                                self.wfile.write(line.encode('utf-8'))
                                break
                        else:
                            self.send_response(404)
                            self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                            self.end_headers()
                            self.wfile.write(b'Not Found')
                            break
                elif v['action'] == 'write_member':
                    self.send_response(200)
                    self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                    self.end_headers()
                    member = v['member']
                    member_id_new, member_name_new, member_credits_new = member.split(',')
                    f = open('./database/members.csv', 'r', encoding='utf-8')
                    g = open('./database/members.csv~', 'w', encoding='utf-8')
                    found_member = False
                    while True:
                        line = f.readline()
                        if line:
                            if line == '\n':
                                continue
                            member_id, member_name, member_credits = line.split('\n')[0].split(',')
                            if member_id == member_id_new:
                                found_member = True
                                # Credits are calculated at client side
                                # member_credits = str(int(member_credits) + int(member_credits_new))
                                member_credits = member_credits_new
                            g.write(','.join([member_id, member_name, member_credits]) + '\n')
                        else:
                            f.close()
                            break
                    if not found_member:
                        g.write(','.join([member_id_new, member_name_new, member_credits_new]) + '\n')
                    g.close()
                    os.remove('./database/members.csv')
                    os.rename('./database/members.csv~', './database/members.csv')
                    self.wfile.write(b'OK')
                elif v['action'] == 'get_member':
                    get_member_id = v['id']
                    f = open('./database/members.csv', 'r', encoding='utf-8')
                    while True:
                        line = f.readline()
                        if line:
                            if line == '\n':
                                continue
                            member_id, member_name, member_credits = line.split('\n')[0].split(',')
                            if member_id == get_member_id:
                                self.send_response(200)
                                self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                                self.end_headers()
                                self.wfile.write(line.encode('utf-8'))
                                break
                        else:
                            self.send_response(404)
                            self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                            self.end_headers()
                            self.wfile.write(b'Not Found')
                            break
            else:
                # local file
                path = path[1:]
                if os.path.exists(path) and path in _statics['allowed_paths']:
                    self.send_response(200)
                    self.send_header('Content-Type', mimeLib.getmime(path))
                    # self.send_header('Cache-Control', 'public, max-age=86400')
                    self.end_headers()
                    with open(path, 'rb') as f:
                        while True:
                            data = f.read(_statics['buffer_size'])
                            if data:
                                self.wfile.write(data)
                            else:
                                break
                    return
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', mimeLib.getmime('*.html'))
                    self.end_headers()
                    self.wfile.write(b'Not Found')
                    return
    def do_POST(self):
        if self.path == '/':
            self.path = '/index.html'
        path = recover(self.path)
        v = urlvar(path)
        if len(path) >= 2:
            if path[0:2] == '/~':
                if v['apikey'] != _statics['apikey']:
                    self.send_response(403)
                    self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                    self.end_headers()
                    self.wfile.write(b'Forbidden')
                    return
                if v['action'] == 'import_database':
                    self.send_response(200)
                    self.send_header('Content-Type', mimeLib.getmime('*.txt'))
                    self.end_headers()
                    length = int(self.headers['Content-Length'])
                    f = open('./database/records.csv', 'ab')
                    f.write(self.rfile.read(length))
                    f.close()
                    self.wfile.write(b'OK')
                    return

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """ Handle requests in a separate thread. """

if __name__ == '__main__':
    d = _statics['config']
    address, port = d['address'], int(d['port'])
    server = ThreadedHTTPServer((address, port), MyServer)
    print('Starting server on address %s, port %s...' % (address, port))
    if not _statics['debug']:
        os.system('firefox --kiosk http://127.0.0.1:8101/ &')

    try:
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        # print("Server loop running in thread:", server_thread.name)
        server.serve_forever()
    except KeyboardInterrupt:
        pass

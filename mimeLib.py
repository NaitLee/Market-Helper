#!/usr/bin/python3

import re
from helpers import wildcard2re, read_ini

mimedict = {}   # This is master one. Will be inited.

# built-in
mimesheetA = {
    '*.htm;*.html': 'text/html;charset=utf-8',
    '*.jpg;*.jpeg;*.jpe': 'image/jpeg',
    '*.gif': 'image/gif',
    '*.png': 'image/png',
    '*.bmp': 'image/bmp',
    '*.ico': 'image/x-icon',
    '*.mpeg;*.mpg;*.mpe': 'video/mpeg',
    '*.avi': 'video/x-msvideo',
    '*.txt': 'text/plain;charset=utf-8',
    '*.css': 'text/css;charset=utf-8',
    '*.js':  'text/javascript;charset=utf-8',
    '*.m3u;*.m3u8': 'application/vnd.apple.mpegurl',
    '*.ttf': 'font/ttf'
}

def setmime(data: dict):
    for i in data:
        for j in i.split(';'):
            mimedict[j] = data[i]

setmime(mimesheetA)

# from ini
mimesheetB = read_ini('mime.ini')
setmime(mimesheetB)

# get mime
def getmime(url: str):
    if url[-1] == '/':
        return 'text/html;charset=utf-8'
    else:
        item = url.split('/')[-1]
        for i in mimedict:
            if re.match(wildcard2re(i), item):
                return mimedict[i]
    return 'application/octet-stream'
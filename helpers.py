#!/usr/bin/python3

import urllib, os, random

FALSE_VALUES = ('', '0')
FALSE_VALUE = '0'
TRUE_VALUE = '1'

def if_(c):
    """ Helper function for boolean operations of macro system """
    return TRUE_VALUE if c else FALSE_VALUE

def if_not_(c):
    """ Helper function for boolean operations of macro system """
    return TRUE_VALUE if not c else FALSE_VALUE

def smartoscmd(posixcall, ntcall):
    return ntcall() if os.name == 'nt' else posixcall()

def ntpath(path: str):
    return path.replace('/', '\\')

def urlvar(path):
    a = path.split('?')
    d = []
    f = {}
    if len(a) > 1:
        b = a[1].split('&')
        for i in b:
            d.append(i.split('='))
    for i in d:
        if len(i) == 1:
            i.append('1')
        f[i[0]] = i[1]
    return f

def getsid():
    return ''.join(map(lambda i: str(random.randint(0, 9)), (['0'] * 32)))

def parse_ini(c: str):
    """ Parse an ini content, returns a dict """
    d = {}
    for i in c.split('\n'):
        if '=' not in i or len(i) == 0:
            continue
        j = i.split('=')
        d[j[0]] = j[1]
    return d

def read_ini(f: str):
    """ Read an .ini file, returns a dict """
    f = open(f, 'r', encoding='utf-8')
    c = f.read()
    f.close()
    return parse_ini(c)

def remove_extention(filename: str):
    return '.'.join(filename.split('.')[0:-1])

units = ['','K','M','G','T']
for c in range(97, 123):    # aa-zz
    units.append(chr(c)+chr(c))

def smartsize(b: int):
    """ Get a number with unit, 1024 = 1 K etc. """
    i = 0
    j = 0
    while j <= b:
        i += 1
        j = 1 << (i * 10)
    i -= 1
    n = b / (1 << (i * 10))
    return str(round(n, 1)) + ' ' + units[i]

def wildcard2re(e: str):
    return e.replace('*', '.*').replace('?', '.?')

def escaperegexp(e: str):
    g = '\\ / . * + ? | ( ) [ ] { }'.split(' ')
    for i in g:
        e = e.replace(i, '\\'+i)
    return e

def purify(s: str):
    """ uriencode input string, change \\ to / """
    return urllib.parse.quote(s).replace('%5C', '/').replace('%2F', '/')  # %5C \ %2F / -> /
def recover(s: str):
    """ uridecode input string """
    return urllib.parse.unquote(s)

def replacepairs(s: str, *args):
    for i in args:
        s = s.replace(i[0], i[1])
    return s

def trimiterable(i):
    """ Maps an iterable, trims strings inside """
    return list(map(lambda s: s.strip(), i))

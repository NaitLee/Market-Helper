#!/usr/bin/python3

# For Windows exe launcher, compile launcher.cpp with mingw

import os, sys

if len(sys.argv) <= 2:
    print('Usage: python3 make_launcher.py <app_name> <exe_name>')
    print('"app_name" is folder name which will be extracted to /tmp folder')
    print('"exe_name" is which file to execute')
    exit(1)

f = open('launcher_template.sh', 'r', encoding='utf-8')
template = f.read()
f.close()

f = open('.gitignore', 'r', encoding='utf-8')
gitignore = f.read().split('\n')
f.close()

files = list(filter(lambda s: s not in gitignore, os.listdir()))

os.system('tar -cz "%s" | base64 > tarball.b64' % '" "'.join(files))

f = open('tarball.b64', 'r', encoding='utf-8')
base64 = f.read()
f.close()

file_content = template.replace(r'%app_name%', sys.argv[1]).replace(r'%exe_name%', sys.argv[2]).replace(r'%base64_content%', base64)
f = open('launcher.sh', 'w', encoding='utf-8')
f.write(file_content)
f.close()

exit(0)

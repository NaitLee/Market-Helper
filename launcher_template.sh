#!/bin/bash
# https://unix.stackexchange.com/questions/46478/join-the-executable-and-all-its-libraries

TEMP_DIR=/tmp
APP_NAME=%app_name%
EXE_NAME=%exe_name%

mkdir ${TEMP_DIR}/${APP_NAME}

# Untar from base64 encoded tarball.
base64 -d <<EOF | tar -xz --overwrite -C ${TEMP_DIR}/${APP_NAME}/
%base64_content%
EOF

# Execute the binary.
LD_LIBRARY_PATH=${TEMP_DIR}/${APP_NAME}/lib/ ${TEMP_DIR}/${APP_NAME}/${EXE_NAME} $*

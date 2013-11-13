#!/usr/bin/env python3
import os
import sys

tox_env_name = 'py' + ''.join(str(x) for x in sys.version_info[:2])
tox_bin_name = 'tox'

print('running: tox -e' + tox_env_name, file=sys.stderr)

os.execvp(tox_bin_name, ['-e' + tox_env_name])

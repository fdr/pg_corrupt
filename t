#!/usr/bin/env python3
import subprocess
import sys

tox_env_name = 'py' + ''.join(str(x) for x in sys.version_info[:2])
tox_bin_name = 'tox'
args = ['-e', tox_env_name] + sys.argv[1:]

print('running: {0} {1}'.format(tox_bin_name, ' '.join(args)), file=sys.stderr)
retcode = subprocess.call([tox_bin_name] + args)
sys.exit(retcode)

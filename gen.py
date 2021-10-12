#!/usr/bin/env python2
from string import Template
import subprocess

result = subprocess.check_output('go help', shell=True)

completes = {}
def get_help():
    start = False

    for line in result.split('\n'):
        if 'The commands are:' in line:
            start = True
            continue
        elif 'Use "go help <command>"' in line:
            start = False
        if start:
            r = line.split()
            try:
                completes[r[0]] = set()
            except:pass

def get_cmd_help(cmd):
    start = False
    result = subprocess.check_output(['go', 'help', cmd])

    for line in result.split('\n'):
        if line.startswith('\t-'):
            r = line.split()
            try:
                completes[cmd].add(r[0])
            except:pass

get_help()
# get_cmd_help('build')
for k in completes:
    get_cmd_help(k)

config = {}

config['COMPLETION_CMDS'] = ' '.join(completes.keys())

flag_template = '''
  local _go_%s_flags="%s"
'''
k = 'build'
v = completes[k]
config['COMPLETION_BUILD_FLAGS'] = ' '.join(v)

with open('./go-completion.tmpl.sh', 'r') as _fd:
    template_content = _fd.read()

with open('./go-completion.bash', 'w') as _fd:
    r = Template(
        template_content).safe_substitute(config)
    _fd.write(r)

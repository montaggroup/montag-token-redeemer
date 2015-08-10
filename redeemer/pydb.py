import os
import sys
import subprocess
pydb_tool_path = os.path.join('..', 'montag', 'pydbtool.py')


def _call_pydb_tool(*args):
    interpreter = sys.executable
    venv_path = os.path.join(os.path.dirname(pydb_tool_path), 'venv')
    if os.path.exists(venv_path):
        interpreter = os.path.join(venv_path, 'bin', 'python')
    call_args = [interpreter, pydb_tool_path] + list(args)
    return subprocess.call(call_args)


def _check_exit_code(exit_code):
    if exit_code != 0:
        raise ValueError('pydbtool call exited with non zero code: {}'.format(exit_code))


def add_friend_to_pydb(friend_name, secet):
    exit_code = _call_pydb_tool('add_friend', friend_name)
    _check_exit_code(exit_code)
    exit_code = _call_pydb_tool('set_comm_data_tcp_aes', friend_name, '', '', secet)
    _check_exit_code(exit_code)



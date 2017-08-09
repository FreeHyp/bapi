import subprocess

def shell(command, simple_return=False):
    """ Execute a command on the host system """
    try:
        process = subprocess.check_output(command, shell=True)
        return process
    except subprocess.CalledProcessError as e:
        t = e.returncode, e.message

def log(level, message):
    print '[%s] %s' % (level, message)

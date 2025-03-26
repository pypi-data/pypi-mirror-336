import os
import glob
import re
from subprocess import Popen, PIPE

from tgqSim.utils.env import IS_WINDOWS

LINUX_HOME = '/usr/local/cuda'
WINDOWS_HOME = glob.glob('C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v*.*')


def find_nvcc():
    if IS_WINDOWS:
        proc = Popen(['where', 'nvcc.exe'], stdout=PIPE, stderr=PIPE)
    else:
        proc = Popen(['which', 'nvcc'], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    out = out.decode().strip()
    if len(out) > 0:
        if IS_WINDOWS:
            if out.find('\r\n') != -1:
                out = out.split('\r\n')[0]
            out = os.path.abspath(os.path.join(os.path.dirname(out), ".."))
            out = out.replace('\\', '/')
            out = str(out)
        return os.path.dirname(out)
    else:
        return None


def find_cuda_version(cuda_home):
    if cuda_home is None:
        return None
    if IS_WINDOWS:
        candidate_names = [os.path.basename(cuda_home)]
    else:
        # get CUDA lib folder
        cuda_lib_dirs = ['lib64', 'lib']
        for lib_dir in cuda_lib_dirs:
            cuda_lib_path = os.path.join(cuda_home, lib_dir)
            if os.path.exists(cuda_lib_path):
                break
        # get a list of candidates for the version number
        # which are files containing cudart
        candidate_names = list(glob.glob(os.path.join(cuda_lib_path, '*cudart*')))
        candidate_names = [os.path.basename(c) for c in candidate_names]

    # suppose version is MAJOR.MINOR.PATCH, all numbers
    version_regex = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+')
    candidates = [c.group() for c in map(version_regex.search, candidate_names) if c]
    if len(candidates) > 0:
        # normally only one will be retrieved, take the first result
        return candidates[0]
    # if no candidates were found, try MAJOR.MINOR
    version_regex = re.compile(r'[0-9]+\.[0-9]+')
    candidates = [c.group() for c in map(version_regex.search, candidate_names) if c]
    if len(candidates) > 0:
        return candidates[0]
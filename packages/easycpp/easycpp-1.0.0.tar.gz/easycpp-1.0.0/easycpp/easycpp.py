import os
import sys
import hashlib
import ctypes
import subprocess
import inspect

DEBUG = False

class Easycpp:
    pass

def debugon():
    global DEBUG
    DEBUG = True

def debugoff():
    global DEBUG
    DEBUG = False

def get_caller_args():
    frameinfo = inspect.stack()[3]
    sig = inspect.signature(frameinfo.frame.f_globals[frameinfo.function])  #  get the function signature
    args = {k: frameinfo.frame.f_locals[k] for k in sig.parameters}  #  get parameters
    return args

def get_functions(so_path):
    result = subprocess.run(['nm', '-D', '--defined-only', so_path], capture_output=True, text=True)
    symbols = result.stdout.split('\n')
    functions = [line for line in symbols if ' T ' in line]
    functions = [line.split()[-1] for line in functions]
    return functions

def is_dynamic_library(file_path):
    _, file_extension = os.path.splitext(file_path)
    dynamic_library_extensions = ['.dll', '.so', '.dylib']
    return file_extension.lower() in dynamic_library_extensions


def easycpp(code_or_so, so_dir="", func_signatures=None, compiler="g++ -O2 -shared -fPIC"):
    #if DEBUG:
    #    for frame in inspect.stack():
    #        print(frame.function, frame.filename)

    caller = inspect.stack()[1]
    if caller.filename == "<string>":
        # when using exec in precompile.py
        caller = inspect.stack()[2]

    prebuild = False
    if  caller.function == "precompile":
        prebuild = True
    if DEBUG: print(f"prebuild mode: {prebuild}")

    if not so_dir:
        # same dir to the .py who using easycpp
        if prebuild:
            caller_dir = os.path.dirname(os.path.abspath(get_caller_args()['py_file']))
        else:
            caller_dir = os.path.dirname(os.path.abspath(caller.filename))
        so_dir = caller_dir
    else:
        # if is a relative path, curdir must be same for precompile and run
        so_dir = os.path.abspath(os.path.expanduser(so_dir))

    if len(code_or_so) < 256 and is_dynamic_library(code_or_so):
        so_path = code_or_so
        if not os.path.exists(so_path):
            raise FileNotFoundError(f"the shared library file does not exist : {so_path}")
        if not os.path.dirname(so_path):
            so_path = f"./{so_path}"
    else:
        tohash = compiler + code_or_so
        code_hash = hashlib.md5(tohash.encode()).hexdigest()
        so_path = os.path.join(so_dir, f"easycpp_{code_hash}.so")

        if not os.path.exists(so_path):
            cpp_file = os.path.join(so_dir, f"easycpp_{code_hash}.cpp")
            with open(cpp_file, "w") as f:
                f.write(code_or_so)

            compile_cmd = f"{compiler} {cpp_file} -o {so_path}"
            result = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"compilation failed : {result.stderr}")

            if DEBUG: print(f"compiled successfully : {so_path}")

    if not prebuild:
        lib = ctypes.CDLL(so_path)
        r = Easycpp()
        r._lib = lib

        if func_signatures:
            functions = func_signatures.split(";")
        else:
            functions = get_functions(so_path)

        for func_name in functions:
            func_name = func_name.strip()
            if func_name:
                try:
                    func = getattr(lib, func_name)
                except AttributeError:
                    raise RuntimeError(f"the shared library does not export the function correctly : {func_name}")

                r.__dict__[func_name] = func
                if DEBUG: print(f"registered function : {func_name}:{func}")

        return r


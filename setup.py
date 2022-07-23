from Cython.Compiler import Options
Options.embed = "main"
from Cython.Build import cythonize

cythonize("spotify.py")
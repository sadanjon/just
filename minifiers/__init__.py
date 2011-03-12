import sys, os

__all__ = []

# get script's working directory
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

MINIFIERS_DIR = os.path.join(script_dir, 'minifiers')


for file in os.listdir(MINIFIERS_DIR):
    ext = os.path.splitext(file)
    if os.path.isfile(os.path.join(MINIFIERS_DIR, file)) and ext[1] == ".py" \
        and file != "__init__.py":
        __all__.append(ext[0])


import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Add everything in /api/ to the module search path.
__path__ = [os.path.dirname(__file__), os.path.join(os.path.dirname(__file__), "api")]

# New comment
def main():
    "Main function to run foamify"
    try:
        from foamify.src.system import System
        my_sys = System(sys.argv)
    except ImportError:
        print("Error: Could not import foamify.src.system.system")
        return 1


if __name__ == '__main__':
    main()

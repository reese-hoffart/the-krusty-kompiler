from .scanning import Scanner
from .utils import get_args, setup_tracebacks

DEBUG = True

def main():
    args = get_args()

    scanner = Scanner(args.PROGRAM)
    setup_tracebacks()
    scanner.scan_all()

if __name__ == "__main__":
    main()
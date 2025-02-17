if __name__ != "__main__":
    print("This is a module, not a standalone script.")
    exit(1)

from __main__ import app, auth, db

"""Generate a hashed password for use in Jupyter Notebook.

This command stores the generated password in your jupyter_notebook_config.json.

"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import argparse
from getpass import getpass
import sys

from traitlets.config.manager import BaseJSONConfigManager
from jupyter_core.paths import jupyter_config_dir

from . import passwd


def set_password(args):
    password = args.password
    while not password:
        password1 = getpass("" if args.quiet else "Provide password: ")
        password_repeat = getpass("" if args.quiet else "Repeat password:  ")
        if password1 != password_repeat:
            print("Passwords do not match, try again")
        elif not pasword1:
            print("Please provide a password")
        else:
            password = password1

    password_hash = passwd(password)
    cfg = BaseJSONConfigManager(config_dir=jupyter_config_dir())
    cfg.update('jupyter_notebook_config', {
        'NotebookApp': {
            'password': password_hash,
        }
    })
    if not args.quiet:
        print("password stored in config dir: %s" % jupyter_config_dir())


def main(argv):
    parser = argparse.ArgumentParser('notebook.auth', description=__doc__)
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    parser_password = subparsers.add_parser('password', help='sets a password for your notebook server')
    parser_password.add_argument("password", help="password to set, if not given, a password will be queried for (NOTE: this may not be safe)",
            nargs="?")
    parser_password.add_argument("--quiet", help="suppress messages", action="store_true")
    parser_password.set_defaults(function=set_password)
    args = parser.parse_args(argv[1:])
    try:
        args.function(args)
    except KeyboardInterrupt:
        print('') # newline
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)

import argparse
import logging
from pathlib import Path

import logging

from dotenv import load_dotenv

load_dotenv()


def suggest_filename():

    from lib import suggest_filename as dsa_suggest_filename

    script_parser = argparse.ArgumentParser(
        prog="suggest_name",
        description="",
    )

    script_parser.add_argument(
        "-f",
        "--file",
        action="store",
        metavar="file",
        help="file to rename and sort",
        required=True,
    )

    file = script_parser.parse_args().file

    path_to_file = Path(file).resolve()

    print(f"path_to_file: {path_to_file}")

    result = dsa_suggest_filename(str(path_to_file))

    print(f"result: {result}")


    # logging.debug(result)
    return ""

def suggest_filedirectory():

    from lib import suggest_filedirectory as dsa_suggest_filedirectory

    script_parser = argparse.ArgumentParser(
        prog="suggest_directory",
        description="",
    )

    script_parser.add_argument(
        "-f",
        "--file",
        action="store",
        metavar="file",
        help="file to rename and sort",
        required=True,
    )

    script_parser.add_argument(
        "-d",
        "--directory",
        action="append",
        metavar="directory",
        help="directories to sort the file into",
        required=True,
    )

    file = script_parser.parse_args().file
    directories = script_parser.parse_args().directory

    path_to_file = Path(file).resolve()
    print(f"path_to_file: {path_to_file}")

    result = dsa_suggest_filedirectory(str(path_to_file), directories)

    print(f"result: {result}")

    return ""


#     return result

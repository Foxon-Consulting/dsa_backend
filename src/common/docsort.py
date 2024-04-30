import logging

logging.getLogger().setLevel(logging.DEBUG)

from . import config


def _docsort(**kwargs):
    from dsa.entrypoint import main as dsa_main
    dsa_main()

    return "END"



def main():
    import argparse

    script_parser = argparse.ArgumentParser(
        prog="docsort",
        description="docsort script",
    )

    # script_parser.add_argument(
    #     "-a",
    #     "--argA",
    #     action="store",
    #     metavar="arg1",
    #     help="docsort argA",
    #     required=True,
    # )

    # script_parser.add_argument(
    #     "-b",
    #     "--argB",
    #     action="store",
    #     metavar="color",
    #     help="docsort color",
    #     required=True,
    # )

    result = _docsort(**vars(script_parser.parse_args()))

    # Example how to access config toml file
    # logging.debug(config)

    # Using **vars() to convert Namespace to dict
    logging.debug(result)

    return result


if __name__ == "__main__":
    main()

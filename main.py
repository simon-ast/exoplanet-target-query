import logging
import numpy as np
import sys

import modules.simbad_query as sq

# GLOBALS
logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        filename="simbad_query.log", level=logging.INFO,
        filemode="w", format='%(levelname)s:%(funcName)s: %(message)s'
    )
    logger.info("Started programme\n")

    # Read input filename from command line arguments
    try:
        input_file = sys.argv[1]
    except IndexError:
        input_file = "test_targets.txt"

    # Read input names from file
    input_names = read_targets(input_file)

    # Make the SIMBAD query object and find names in list
    simbad = sq.make_query()
    query_results = sq.query_names(simbad, input_names)

    query_results.write_csv("simbad_query_results.csv")

    logger.info("Completed")


def read_targets(filename: str) -> np.array:
    """
    Generate an array of test target-names from a fixed file. The file contains
    a selection of random planet names, and several iterations of the same
    planet to check for correct overlap

    :return: np.array of target names as strings
    """
    target_array = np.genfromtxt(
        filename, delimiter="\n", dtype=str
    )

    logger.info(f"From file {filename} querying the list\n{target_array}\n")
    return target_array


if __name__ == "__main__":
    main()

import astroquery.simbad as simbad
import numpy as np
import polars
import logging
import warnings


# GLOBALS
logger = logging.getLogger(__name__)


def make_query() -> simbad.Simbad:
    """
    Make a customised SIMBAD query only looking for 'MAIN_ID' and 'TYPED_ID'
    NOTE: This functionality of SIMBAD somewhat fails when the query results
    in an error. The result will not be a blank line to mark a failed query,
    but will be omitted in total. I will there implement a failsafe to make
    sure that failed queries are at least logged by their input value

    :return: SIMBAD query object
    """
    customised_simbad = simbad.Simbad()

    # Remove all fields but the default "MAIN_ID" field
    customised_simbad.remove_votable_fields("coordinates")

    # Add the input-ID for all objects
    customised_simbad.add_votable_fields('typed_id')

    logger.info(f"Queried fields are "
                f"{customised_simbad.get_votable_fields()}\n")
    return customised_simbad


def query_names(
        simbad_query: simbad.Simbad,
        name_list: np.array
) -> polars.DataFrame:
    """
    Make a data frame form the input object name list and SIMBAD query

    :param simbad_query:    SIMBAD query object
    :param name_list:       Array of names to query
    :return:
        Polars data frame of the query results and corresponding
        input values
    """
    logger.info(f"Querying {name_list.shape[0]} objects...")

    # Suppressing the "UserWarnings" from astroquery
    warnings.filterwarnings("ignore", category=UserWarning)

    # Produce a result dictionary from SIMBAD query. Keep in mind that
    # the SIMBAD table entries are masked array, so the underlying array
    # is accessed through .data.data
    simbad_table = simbad_query.query_objects(name_list)

    # Replace empty results from failed queries
    simbad_names = simbad_table["MAIN_ID"].data.data
    simbad_names[simbad_names == ""] = "N/A"

    results = {
        "SIMBAD": simbad_names,
        "INPUT": simbad_table["TYPED_ID"].data.data
    }

    # Construct Polars (new stuff!) data frame
    result_frame = polars.DataFrame(
        data=results, schema={"SIMBAD": str, "INPUT": str}
    )

    # Log number of failed queries
    failed_queries = result_frame.filter(polars.col("SIMBAD") == "N/A")
    if failed_queries.shape[0] != 0:
        logger.info(
            f"Failed to find {failed_queries.shape[0]} object(s):\n"
            f"{failed_queries['INPUT'].to_list()}\n"
        )
    else:
        logger.info("All queries successfull!\n")

    return result_frame


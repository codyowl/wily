"""
Print command.

Print information about the wily cache and what is in the index.
"""
from wily import logger, format_date, format_revision, MAX_MESSAGE_WIDTH
from wily.state import State
import tabulate
import wily.cache as cache
from wily.config import DEFAULT_GRID_STYLE


def index(config, include_message=False):
    """
    Show information about the cache and runtime.

    :param config: The wily configuration
    :type  config: :namedtuple:`wily.config.WilyConfig`

    :param include_message: Include revision messages
    :type  include_message: ``bool``
    """
    state = State(config=config)
    logger.debug("Running show command")
    logger.info("--------Configuration---------")
    logger.info(f"Path: {config.path}")
    logger.info(f"Archiver: {config.archiver}")
    logger.info(f"Operators: {config.operators}")
    logger.info("")
    logger.info("-----------History------------")

    data = []
    for archiver in state.archivers:
        for rev in state.index[archiver].revisions:
            if include_message:
                data.append(
                    (
                        format_revision(rev.revision),
                        rev.author_name,
                        rev.message[:MAX_MESSAGE_WIDTH],
                        format_date(rev.date),
                    )
                )
            else:
                data.append(
                    (
                        format_revision(rev.revision),
                        rev.author_name,
                        format_date(rev.date),
                    )
                )

    if include_message:
        headers = ("Revision", "Author", "Message", "Date")
    else:
        headers = ("Revision", "Author", "Date")
    print(
        tabulate.tabulate(
            headers=headers, tabular_data=data, tablefmt=DEFAULT_GRID_STYLE
        )
    )

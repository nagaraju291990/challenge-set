import logging
# for handler in logging.root.handlers[:]:
# 	logging.root.removeHandler(handler)
# log = logging.basicConfig(filename='comet.log', filemode='w', format='%(asctime)s %(levelname)s: %(lineno)d, %(funcName)s %(message)s', level=logging.INFO)
# logger = logging.getLogger()
def setup_logger(log_filename):
    # Clear any existing handlers on the root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up logging configuration
    logging.basicConfig(
        filename=log_filename,
        filemode='w',
        format='%(asctime)s %(levelname)s: %(lineno)d, %(funcName)s %(message)s',
        level=logging.INFO
    )

    return logging.getLogger()
#logger.disabled = True
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')
#logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
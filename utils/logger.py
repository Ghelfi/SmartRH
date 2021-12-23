import logging
import os
import datetime
import sys

logging_level_dict = {
    "WARN": logging.WARN,
    "ERROR": logging.ERROR,
    "INFO": logging.INFO,
    "CRITICAL": logging.CRITICAL,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET
}

def configure_logging(*args, **kwargs):
    log_name = kwargs.get('log_name', 'default_log')
    log_dir = kwargs.get('log_dir', './logs')
    log_level = kwargs.get('log_level', 'WARN')

    if type(log_level) is not str:
        raise TypeError('log_level parameter must be set as a str parameter')

    log_level = log_level.upper()
    accepted_log_levels = ['WARN', 'INFO', 'ERROR', 'CRITICAL', 'DEBUG', 'NOTSET']

    if log_level not in accepted_log_levels:
        raise ValueError('log_level parameter must be contained in {}'.format(accepted_log_levels))

    # Creating  the logdir if it does not exist
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    # Format of a log message.
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s %(lineno)s\t%(message)s') #:%(name)s

    log_file = '{}/{}-{}.log'.format(log_dir, log_name,datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S'))
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    root_log = logging.getLogger()
    root_log.addHandler(file_handler)

    # Configuring logging to stdout, for all INFO/WARNING/ERROR messages.
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    root_log.addHandler(console_handler)

    # Setting log level
    root_log.setLevel(logging_level_dict[log_level])


if __name__ == '__main__':

    logs_parameters = {
        'log_dir' : './logs',
        'log_level': 'INFO',
        'log_name': 'log_test'
    }

    configure_logging(**logs_parameters)
    my_logger = logging.getLogger()

    my_logger.error('Test Error Message')
    my_logger.warning('Test Warn Message')
    my_logger.info('Test Info Message')
    my_logger.debug('Test Debug Message')
    my_logger.critical('Test Critical Message')
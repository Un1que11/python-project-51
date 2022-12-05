import logging.config
import logging.handlers

CONFIG_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s | %(levelname)s] %(name)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'advanced': {
            'format': '%(asctime)s | [%(levelname)s] %(name)s [%(funcName)s:%(lineno)d]: %(message)s',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },

        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'filename': 'info.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8',
        },

        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'advanced',
            'filename': 'errors.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8',
        },
    },

    'loggers': {
        'page_loader.loader.loader': {
            'level': 'WARNING',
            'handlers': ['console', 'info_file_handler'],
            'propagate': False,
        },
    },

    'root': {
        'level': 'WARNING',
        'handlers': ['console', 'info_file_handler', 'error_file_handler'],
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(CONFIG_DICT)

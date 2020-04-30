import warnings
import logging
import logging.config


logging.config.dictConfig({
    "version": 1,

    "formatters": {
        "investment_local_horse_racing_crawler.logging.format": {
            "format": "%(asctime)s - %(levelname)-5s [%(name)s] %(message)s",
        },
    },

    "handlers": {
        "investment_local_horse_racing_crawler.logging.handler": {
            "class": "logging.StreamHandler",
            "formatter": "investment_local_horse_racing_crawler.logging.format",
            "level": logging.DEBUG,
        },
    },

    "loggers": {
        "investment_local_horse_racing_crawler": {
            "handlers": ["investment_local_horse_racing_crawler.logging.handler"],
            "level": logging.DEBUG,
            "propagate": 0,
        },
        "boto3": {
            "level": logging.INFO,
        },
        "botocore": {
            "level": logging.INFO,
        },
    },
})

warnings.simplefilter("ignore")


def get_logger(name):
    return logging.getLogger(name)

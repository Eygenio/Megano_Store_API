LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": (
                "%(log_color)s%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            ),
            "log_colors": {
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console_color": {
            "class": "logging.StreamHandler",
            "formatter": "color",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console_color"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console_color"],
            "level": "DEBUG",
            "propagate": False,
        },
        "app": {
            "handlers": ["console_color"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

import logging
import logging.config

# Configuración del logging con dictConfig()
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {  # Formato detallado para el archivo
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "simple": {  # Formato más simple para la consola
            "format": "%(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {  # Salida a la consola
            "class": "logging.StreamHandler",
            "level": "DEBUG",  # Asegurar que se capturan todos los niveles
            "formatter": "detailed",
        },
        "file": {  # Salida a un archivo de logs
            "class": "logging.FileHandler",
            "filename": "md_toc_files_plus.log",
            "mode": "a",  # Añadir en lugar de sobrescribir
            "level": "DEBUG",  # Capturar todos los niveles en el archivo
            "formatter": "detailed",
        },
    },
    "loggers": {
        "md_toc": {  # Logger específico para md_toc
            "level": "DEBUG",  # Asegurar que captura DEBUG y superiores
            "handlers": ["console", "file"],
            "propagate": False,
        }
    },
}

# Aplicar configuración
logging.config.dictConfig(LOGGING_CONFIG)

# Crear el logger principal del módulo md_toc
logger = logging.getLogger("md_toc_files_plus")
logger.debug("** [START] **")

# logger.debug('This message should go to the log file')
# logger.info('So should this')
# logger.warning('And this, too')
# logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
# logger.critical("Mensaje CRITICAL de prueba")
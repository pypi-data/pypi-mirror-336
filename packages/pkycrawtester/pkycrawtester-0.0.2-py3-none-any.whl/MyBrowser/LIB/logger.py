# -*- coding: utf-8 -*-
#=========================================================
# 제목 : 로깅설정 파일
#
#=========================================================
from logging.config import dictConfig

LOGGING_CONFIG = {
    'version': 1,
	 'disable_existing_loggers': True,
    'loggers': {
        'zz': {  # root logger
            'level': 'NOTSET',
            'handlers': ['console_handler', 'rotating_file_handler', 'error_file_handler', 'critical_mail_handler'],
        },
        'TEST': { 
            'level': 'DEBUG',
            'propagate': False,
            'handlers': ['console_handler', 'rotating_file_handler','error_file_handler' ], # 'rotating_file_handler',
        },
    },
    'handlers': {
        'console_handler': {
            'level': 'DEBUG',
            'formatter': 'consoleFormatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'rotating_file_handler': {
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'info.log',
            'mode': 'a',
				"encoding": "utf-8",
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'error_file_handler': {
            'level': 'WARNING',
            'formatter': 'error',
            'class': 'logging.FileHandler',
            'filename': 'error.log', # LOG/error.log
            'mode': 'a',
        },
        'critical_mail_handler': {
            'level': 'CRITICAL',
            'formatter': 'error',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost' : 'localhost',
            'fromaddr': 'monitoring@domain.com',
            'toaddrs': ['dev@domain.com', 'qa@domain.com'],
            'subject': 'Critical error with application name'
        }
    },
	'formatters': {
		'consoleFormatter': {
			'datefmt': '%H:%M:%S',
			'format': '%(message)s'
		},
		'info': {
			'datefmt': '%H:%M:%S',
			'format': '%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s'
		},
		'error': {
			'datefmt': '%Y-%m-%d %H:%M:%S',
			'format': '[%(asctime)s] %(name)s:%(lineno)s:%(levelname)s - %(message)s'
		},
		'shortFormatter': {
			'format': '%(name)s:%(lineno)s:%(levelname)s >>> %(message)s'
		},
		'fileFormatter': { # [2021-02-06 12:28:03] root:124:INFO -
			'datefmt': '%Y-%m-%d %H:%M:%S',
			'format': '[%(asctime)s] %(name)s:%(lineno)s:%(levelname)s - %(message)s'
			#'format': '%(asctime)-16s %(levelname)-8s %(filename)-s:%(lineno)-3s %(message)s'
		},
	},

}

dictConfig(LOGGING_CONFIG)

if __name__ == "__main__":
    
    import logging
    
    # Include in each module:
    log = logging.getLogger(__name__)
    log.debug("Logging is configured.")
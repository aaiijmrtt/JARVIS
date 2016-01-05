import logging, logging.config

details = 15
logging.config.dictConfig({
	'version': 1,
	'loggers': {
		'logger': {
			'handlers': ['DEBUGLog', 'DETAILLog', 'INFOLog'],
			'level': 'DEBUG'
		}
	},
	'handlers': {
		'DEBUGLog': {
			'class': 'logging.FileHandler',
			'formatter': 'LogFormat',
			'filename': 'jarvis.bug',
			'level': 'DEBUG'
		},
		'DETAILLog': {
			'class': 'logging.FileHandler',
			'formatter': 'LogFormat',
			'filename': 'jarvis.log',
			'level': details
		},
		'INFOLog': {
			'class': 'logging.StreamHandler',
			'formatter': 'LogFormat',
			'level': 'INFO'
		}
	},
	'formatters': {
		'LogFormat': {
			'format': '[%(asctime)s : %(module)s %(funcName)s : %(levelname)s] %(message)s'
		}
	}
})

logger = logging.getLogger('logger')
logger.info('CREATION')

import time, subprocess
import configurer, logger

def initialize():
	global online, process
	if online:
		logger.logger.warn('SPEAKER REINITIALIZATION')
		return
	process = subprocess.Popen(configurer.espeak, stdin = subprocess.PIPE, stdout = subprocess.PIPE, shell = True)
	online = True
	logger.logger.info('SPEAKER INITIALIZATION')

def speak(line):
	global online, process
	if not online:
		logger.logger.warn('UNINITIALIZED SPEAKER INPUT <' + line.strip() + '>')
		return
	logger.logger.info('SPEAKER INPUT <' + line.strip() + '>')
	process.stdin.write(line)
	time.sleep(0.1)

def terminate():
	global online, process
	if not online:
		logger.logger.warn('UNINITIALIZED SPEAKER TERMINATION')
		return
	process.terminate()
	online = False
	logger.logger.info('SPEAKER TERMINATION')

online = False
process = None
logger.logger.info('SPEAKER CREATION')

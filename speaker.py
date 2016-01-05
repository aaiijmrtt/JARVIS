import time, subprocess
import configurer, logger

def initialize():
	global online, process
	if online:
		logger.logger.warn('REINITIALIZATION')
		return
	process = subprocess.Popen(configurer.espeak, stdin = subprocess.PIPE, stdout = subprocess.PIPE, shell = True)
	online = True
	logger.logger.info('INITIALIZATION')

def speak(line):
	global online, process
	if not online:
		logger.logger.warn('UNINITIALIZED')
		logger.logger.warn('INPUT <' + line.strip() + '>')
		return
	logger.logger.info('INPUT <' + line.strip() + '>')
	process.stdin.write(line)
	time.sleep(0.1)

def terminate():
	global online, process
	if not online:
		logger.logger.warn('UNINITIALIZED')
		return
	process.terminate()
	online = False
	logger.logger.info('TERMINATION')

online = False
process = None
logger.logger.info('CREATION')

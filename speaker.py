import subprocess

class Speaker:
	def __init__(self, debug):
		self.debug = debug

	def initialize(self):
		self.engine = subprocess.Popen('../../Downloads/espeak-1.48.04-source/linux_32bit/espeak -s 130 -p 50 -k 1', stdin = subprocess.PIPE, shell = True)
		if self.debug:
			print '[DEBUG: INITIALIZED SPEAKER]'

	def speak(self, line):
		if self.debug:
			print '[DEBUG: SPEAKER INPUT', line.strip(), ']'
		self.engine.stdin.write(line)

	def terminate(self):
		self.engine.terminate()
		if self.debug:
			print '[DEBUG: TERMINATED SPEAKER]'

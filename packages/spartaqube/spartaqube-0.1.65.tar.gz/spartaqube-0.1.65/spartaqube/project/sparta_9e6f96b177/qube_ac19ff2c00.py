import time
from project.logger_config import logger
def sparta_d3985e0f9a():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_d3985e0f9a()
def sparta_ca5726841b(tempBool=True):
	A=next(TicToc)
	if tempBool:logger.debug('Elapsed time: %f seconds.\n'%A);return A
def sparta_cb1dc47aa3():sparta_ca5726841b(False)
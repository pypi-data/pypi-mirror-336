import os
from multiprocessing import Process
def sparta_c02689995d(func):
	def B(*A,**B):
		if os.fork()!=0:return
		func(*A,**B)
	def A(*C,**D):A=Process(target=lambda:B(*C,**D));A.start();A.join()
	return A
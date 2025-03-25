import os
from project.sparta_9e6f96b177.sparta_088dd79220.qube_6af15df9b4 import qube_6af15df9b4
from project.sparta_9e6f96b177.sparta_088dd79220.qube_9f28d74c04 import qube_9f28d74c04
from project.sparta_9e6f96b177.sparta_088dd79220.qube_4121807495 import qube_4121807495
from project.sparta_9e6f96b177.sparta_088dd79220.qube_484349890d import qube_484349890d
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_6af15df9b4()
		elif A.dbType==1:A.dbCon=qube_9f28d74c04()
		elif A.dbType==2:A.dbCon=qube_4121807495()
		elif A.dbType==4:A.dbCon=qube_484349890d()
		return A.dbCon
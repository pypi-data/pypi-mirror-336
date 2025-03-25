import os,sys,getpass,platform
from project.sparta_53ffb1e378.sparta_fb4fb1662f.qube_bb1f3cf253 import sparta_21537dcf3c,sparta_e4991d247e
def sparta_9bd33fd743(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_3172834b12():
	if sparta_e4991d247e():A='/app/APPDATA/local_db/db.sqlite3'
	else:C=sparta_21537dcf3c();B=os.path.join(C,'data');sparta_9bd33fd743(B);A=os.path.join(B,'db.sqlite3')
	return A
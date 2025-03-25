import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_04622df331():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_c5f545c17a(userId):A=sparta_04622df331();B=os.path.join(A,userId);return B
def sparta_8cfa02dbcc(notebookProjectId,userId):A=sparta_c5f545c17a(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_aa5bf49d93(notebookProjectId,userId):A=sparta_c5f545c17a(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_4a242b4f5a(notebookProjectId,userId,ipynbFileName):A=sparta_c5f545c17a(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_f4905ed09c(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_8cfa02dbcc(B,C);G=sparta_c5f545c17a(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_d285419157(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_f4905ed09c(A,B);C=f"{A}.zip";D=sparta_c5f545c17a(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}
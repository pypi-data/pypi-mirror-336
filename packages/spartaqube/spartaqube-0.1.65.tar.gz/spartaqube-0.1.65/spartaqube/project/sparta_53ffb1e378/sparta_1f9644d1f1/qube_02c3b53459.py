_H='execution_count'
_G='cell_type'
_F='code'
_E='outputs'
_D='source'
_C='cells'
_B='sqMetadata'
_A='metadata'
import os,re,uuid,json
from datetime import datetime
from nbconvert.filters import strip_ansi
from project.sparta_53ffb1e378.sparta_733d4ac517 import qube_7dc8b1ad86 as qube_7dc8b1ad86
from project.sparta_53ffb1e378.sparta_fb4fb1662f.qube_cddd9d1538 import sparta_14c28d1bf8,sparta_5a0e210d50
from project.logger_config import logger
def sparta_5ea7fe3ef7(file_path):return os.path.isfile(file_path)
def sparta_b5d5bfe2df():return qube_7dc8b1ad86.sparta_c37c8fc878(json.dumps({'date':str(datetime.now())}))
def sparta_e08ec09273():B='python';A='name';C={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':B,A:'python3'},'language_info':{'codemirror_mode':{A:'ipython','version':3},'file_extension':'.py','mimetype':'text/x-python',A:B,'nbconvert_exporter':B,'pygments_lexer':'ipython3'},_B:sparta_b5d5bfe2df()};return C
def sparta_fef7c2ba84():return{_G:_F,_D:[''],_A:{},_H:None,_E:[]}
def sparta_1ea60d512f():return[sparta_fef7c2ba84()]
def sparta_abad65e9dd():return{'nbformat':4,'nbformat_minor':0,_A:sparta_e08ec09273(),_C:[]}
def sparta_f16e51fa5c(first_cell_code=''):A=sparta_abad65e9dd();B=sparta_fef7c2ba84();B[_D]=[first_cell_code];A[_C]=[B];return A
def sparta_7dd4710e13(full_path):
	A=full_path
	if sparta_5ea7fe3ef7(A):return sparta_fa859a63f4(A)
	else:return sparta_f16e51fa5c()
def sparta_fa859a63f4(full_path):return sparta_b7acdb8559(full_path)
def sparta_2dd044ec98():A=sparta_abad65e9dd();B=json.loads(qube_7dc8b1ad86.sparta_9d8f675dfb(A[_A][_B]));A[_A][_B]=B;return A
def sparta_b7acdb8559(full_path):
	with open(full_path)as C:B=C.read()
	if len(B)==0:A=sparta_abad65e9dd()
	else:A=json.loads(B)
	A=sparta_8c1595d9f7(A);return A
def sparta_8c1595d9f7(ipynb_dict):
	A=ipynb_dict;C=list(A.keys())
	if _C in C:
		D=A[_C]
		for B in D:
			if _A in list(B.keys()):
				if _B in B[_A]:B[_A][_B]=qube_7dc8b1ad86.sparta_9d8f675dfb(B[_A][_B])
	try:A[_A][_B]=json.loads(qube_7dc8b1ad86.sparta_9d8f675dfb(A[_A][_B]))
	except:A[_A][_B]=json.loads(qube_7dc8b1ad86.sparta_9d8f675dfb(sparta_b5d5bfe2df()))
	return A
def sparta_a612941571(full_path):
	B=full_path;A=dict()
	with open(B)as C:A=C.read()
	if len(A)==0:A=sparta_2dd044ec98();A[_A][_B]=json.dumps(A[_A][_B])
	else:
		A=json.loads(A)
		if _A in list(A.keys()):
			if _B in list(A[_A].keys()):A=sparta_8c1595d9f7(A);A[_A][_B]=json.dumps(A[_A][_B])
	A['fullPath']=B;return A
def save_ipnyb_from_notebook_cells(notebook_cells_arr,full_path,dashboard_id='-1'):
	R='output_type';Q='markdown';L=full_path;K='tmp_idx';B=[]
	for A in notebook_cells_arr:
		A['bIsComputing']=False;S=A['bDelete'];F=A['cellType'];M=A[_F];T=A['positionIndex'];A[_D]=[M];G=A.get('ipynbOutput',[]);C=A.get('ipynbError',[]);logger.debug('ipynb_output_list');logger.debug(G);logger.debug(type(G));logger.debug('ipynb_error_list');logger.debug(C);logger.debug(type(C));logger.debug('this_cell_dict');logger.debug(A)
		if int(S)==0:
			if F==0:H=_F
			elif F==1:H=Q
			elif F==2:H=Q
			elif F==3:H='raw'
			D={_A:{_B:qube_7dc8b1ad86.sparta_c37c8fc878(json.dumps(A))},'id':uuid.uuid4().hex[:8],_G:H,_D:[M],_H:None,K:T,_E:[]}
			if len(G)>0:
				N=[]
				for E in G:O={};O[E['type']]=[E['output']];N.append({'data':O,R:'execute_result'})
				D[_E]=N
			elif len(C)>0:
				D[_E]=C
				try:
					J=[];U=re.compile('<ipython-input-\\d+-[0-9a-f]+>')
					for E in C:E[R]='error';J+=[re.sub(U,'<IPY-INPUT>',strip_ansi(A))for A in E['traceback']]
					if len(J)>0:D['tbErrors']='\n'.join(J)
				except Exception as V:logger.debug('Except prepare error output traceback with msg:');logger.debug(V)
			else:D[_E]=[]
			B.append(D)
	B=sorted(B,key=lambda d:d[K]);[A.pop(K,None)for A in B];I=sparta_7dd4710e13(L);P=I[_A][_B];P['identifier']={'dashboardId':dashboard_id};I[_A][_B]=qube_7dc8b1ad86.sparta_c37c8fc878(json.dumps(P));I[_C]=B
	with open(L,'w')as W:json.dump(I,W,indent=4)
	return{'res':1}
def sparta_662dcf5316(full_path):
	A=full_path;A=sparta_14c28d1bf8(A);C=dict()
	with open(A)as D:E=D.read();C=json.loads(E)
	F=C[_C];B=[]
	for G in F:B.append({_F:G[_D][0]})
	logger.debug('notebook_cells_list');logger.debug(B);return B
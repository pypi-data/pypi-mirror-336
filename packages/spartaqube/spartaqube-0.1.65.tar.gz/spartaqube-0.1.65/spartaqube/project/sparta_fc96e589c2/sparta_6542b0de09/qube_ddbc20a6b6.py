_A='menuBar'
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse,Http404
from urllib.parse import unquote
import project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 as qube_3b035725a9
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_43c7b997ad
from project.sparta_53ffb1e378.sparta_784a241164 import qube_8c9561c7c1 as qube_8c9561c7c1
from project.sparta_53ffb1e378.sparta_1f9644d1f1 import qube_02c3b53459 as qube_02c3b53459
from project.sparta_53ffb1e378.sparta_fb4fb1662f.qube_bb1f3cf253 import sparta_21537dcf3c
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_de8ab14b40(request):A=request;B=qube_3b035725a9.sparta_6d69866b9f(A);B[_A]=-1;C=qube_3b035725a9.sparta_c34211e67a(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_a539f0622c(request,kernel_manager_uuid):
	D=kernel_manager_uuid;C=True;B=request;E=False
	if D is None:E=C
	else:
		F=qube_8c9561c7c1.sparta_f24b301a6f(B.user,D)
		if F is None:E=C
	if E:return sparta_de8ab14b40(B)
	def H(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=C)
	K=sparta_21537dcf3c();G=os.path.join(K,'kernel');H(G);I=os.path.join(G,D);H(I);J=os.path.join(I,'main.ipynb')
	if not os.path.exists(J):
		L=qube_02c3b53459.sparta_f16e51fa5c()
		with open(J,'w')as M:M.write(json.dumps(L))
	A=qube_3b035725a9.sparta_6d69866b9f(B);A['default_project_path']=G;A[_A]=-1;N=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(N);A['kernel_name']=F.name;A['kernelManagerUUID']=F.kernel_manager_uuid;A['bCodeMirror']=C;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)
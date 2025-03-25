_K='bPublicUser'
_J='notebook_name'
_I='notebook_id'
_H='b_require_password'
_G='notebook_obj'
_F='default_project_path'
_E='bCodeMirror'
_D='menuBar'
_C='res'
_B=None
_A=True
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
from project.sparta_53ffb1e378.sparta_7bff2256ce import qube_a06b21bb50 as qube_a06b21bb50
from project.sparta_53ffb1e378.sparta_fb4fb1662f.qube_bb1f3cf253 import sparta_21537dcf3c
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_8405f5ab98(request):
	B=request;A=qube_3b035725a9.sparta_6d69866b9f(B);A[_D]=13;D=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(D);A[_E]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_21537dcf3c();C=os.path.join(F,'notebook');E(C);A[_F]=C;return render(B,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_d2eea56e58(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_a06b21bb50.sparta_2a3d3b5038(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_8405f5ab98(B)
	A=qube_3b035725a9.sparta_6d69866b9f(B);A[_D]=12;H=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_550ad6b1be(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_a06b21bb50.sparta_2a3d3b5038(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_8405f5ab98(B)
	A=qube_3b035725a9.sparta_6d69866b9f(B);A[_D]=12;H=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)
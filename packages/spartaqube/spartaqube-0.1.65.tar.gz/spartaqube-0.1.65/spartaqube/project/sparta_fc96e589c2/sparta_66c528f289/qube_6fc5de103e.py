_L='bPublicUser'
_K='developer_name'
_J='developer_id'
_I='b_require_password'
_H='developer_obj'
_G='default_project_path'
_F='bCodeMirror'
_E='menuBar'
_D='dist/project/homepage/homepage.html'
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
from django.conf import settings as conf_settings
import project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 as qube_3b035725a9
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_43c7b997ad
from project.sparta_53ffb1e378.sparta_edffdd25d8 import qube_54e9014617 as qube_54e9014617
from project.sparta_53ffb1e378.sparta_fb4fb1662f.qube_bb1f3cf253 import sparta_21537dcf3c
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_2a5aefc6e2(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_3b035725a9.sparta_6d69866b9f(B);return render(B,_D,A)
	qube_54e9014617.sparta_3778d0d03f();A=qube_3b035725a9.sparta_6d69866b9f(B);A[_E]=12;D=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(D);A[_F]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_21537dcf3c();C=os.path.join(F,'developer');E(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_51d2ac8579(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_3b035725a9.sparta_6d69866b9f(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_54e9014617.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_2a5aefc6e2(B)
	A=qube_3b035725a9.sparta_6d69866b9f(B);A[_E]=12;H=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_32e97cb379(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_3b035725a9.sparta_6d69866b9f(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_54e9014617.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_2a5aefc6e2(B)
	A=qube_3b035725a9.sparta_6d69866b9f(B);A[_E]=12;H=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_6a370f659b(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)
_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_53ffb1e378.sparta_1f9644d1f1 import qube_9b7bac7527 as qube_9b7bac7527
from project.sparta_53ffb1e378.sparta_1f9644d1f1 import qube_d2ad8d6e05 as qube_d2ad8d6e05
from project.sparta_53ffb1e378.sparta_2c2de249fd import qube_d35c863df6 as qube_d35c863df6
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_795c1e5190,sparta_b9a6882d05
@csrf_exempt
def sparta_6b7ef3cb6c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_6b7ef3cb6c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_d9938b5d98(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_d9938b5d98(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_eff0c77f89(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_eff0c77f89(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_98a2c75114(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_98a2c75114(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_18354437cc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_18354437cc(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_abfc42f59f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_abfc42f59f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_80f3f9668c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_80f3f9668c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_fb6549fcde(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_fb6549fcde(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_4d4f5c0d38(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_4d4f5c0d38(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_6b581f86e4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.sparta_6b581f86e4(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_177c9c320a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_9b7bac7527.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_7913370d54(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_9b7bac7527.sparta_7913370d54(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_04cedbcd4c(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_cb09acef28(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_795c1e5190
def sparta_e744b1e47d(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_cb09acef28(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_9b7bac7527.sparta_ef075f82ae(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_795c1e5190
def sparta_57b8ceb443(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_9b7bac7527.sparta_7d933e4950(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_2ae5d676b8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_2ae5d676b8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_755b63642f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_755b63642f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_af6b798cbc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_af6b798cbc(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_441859263a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_441859263a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_a4d2b6fa58(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_a4d2b6fa58(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_bcc0624db0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_bcc0624db0(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_18f8e3549a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_18f8e3549a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_1f5b377c7a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_1f5b377c7a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_fdab233eec(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_fdab233eec(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_8e1dbd65ab(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_8e1dbd65ab(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_68deac4099(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_68deac4099(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_88790d4c63(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_88790d4c63(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_bfa063c3e5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_bfa063c3e5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
@sparta_b9a6882d05
def sparta_f5309c3675(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2ad8d6e05.sparta_f5309c3675(C,A.user);E=json.dumps(D);return HttpResponse(E)
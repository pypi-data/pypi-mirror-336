_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='res'
_C='Content-Disposition'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_53ffb1e378.sparta_ba8a2af920 import qube_26dd731941 as qube_26dd731941
from project.sparta_53ffb1e378.sparta_ba8a2af920 import qube_7f9a5a24c8 as qube_7f9a5a24c8
from project.sparta_53ffb1e378.sparta_fb4fb1662f import qube_cddd9d1538 as qube_cddd9d1538
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_795c1e5190
@csrf_exempt
@sparta_795c1e5190
def sparta_9cc27d4495(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_26dd731941.sparta_a2f118a154(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_795c1e5190
def sparta_20221313bc(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_26dd731941.sparta_f57a107648(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_eec918f20f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_26dd731941.sparta_b2e90ebe40(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_ac661bf545(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_26dd731941.sparta_722fbe711f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_3d344c0488(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_7f9a5a24c8.sparta_003d513ed0(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_8510b66a8b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_26dd731941.sparta_8bcaabc343(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_6301b72772(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_26dd731941.sparta_989c74bf29(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_759fe7f803(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_26dd731941.sparta_362a2d26e3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_d53b75d2f4(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_26dd731941.sparta_d8beb84d1b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_77b7b08f4c(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_26dd731941.sparta_ef075f82ae(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_795c1e5190
def sparta_c64499c8ca(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_26dd731941.sparta_cbab33bde7(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_795c1e5190
def sparta_18c8e2a18b(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_26dd731941.sparta_7d933e4950(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A
import pkg_resources
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import re_path as url
from django.conf import settings
from project.sparta_9e6f96b177.sparta_3791b6ed45 import qube_40ef7044b9,qube_4ac261b6f3,qube_53a7386340,qube_4241c16aa6,qube_4fc6323356,qube_aff4b579f8,qube_ca52f53f6c,qube_8074ffa5f6,qube_ffa30651d3
from channels.auth import AuthMiddlewareStack
import channels
channels_ver=pkg_resources.get_distribution('channels').version
channels_major=int(channels_ver.split('.')[0])
def sparta_5d98ee3029(this_class):
	A=this_class
	if channels_major<=2:return A
	else:return A.as_asgi()
urlpatterns=[url('ws/statusWS',sparta_5d98ee3029(qube_40ef7044b9.StatusWS)),url('ws/notebookWS',sparta_5d98ee3029(qube_4ac261b6f3.NotebookWS)),url('ws/wssConnectorWS',sparta_5d98ee3029(qube_53a7386340.WssConnectorWS)),url('ws/pipInstallWS',sparta_5d98ee3029(qube_4241c16aa6.PipInstallWS)),url('ws/gitNotebookWS',sparta_5d98ee3029(qube_4fc6323356.GitNotebookWS)),url('ws/xtermGitWS',sparta_5d98ee3029(qube_aff4b579f8.XtermGitWS)),url('ws/hotReloadLivePreviewWS',sparta_5d98ee3029(qube_ca52f53f6c.HotReloadLivePreviewWS)),url('ws/apiWebserviceWS',sparta_5d98ee3029(qube_8074ffa5f6.ApiWebserviceWS)),url('ws/apiWebsocketWS',sparta_5d98ee3029(qube_ffa30651d3.ApiWebsocketWS))]
application=ProtocolTypeRouter({'websocket':AuthMiddlewareStack(URLRouter(urlpatterns))})
for thisUrlPattern in urlpatterns:
	try:
		if len(settings.DAPHNE_PREFIX)>0:thisUrlPattern.pattern._regex='^'+settings.DAPHNE_PREFIX+'/'+thisUrlPattern.pattern._regex
	except Exception as e:print(e)
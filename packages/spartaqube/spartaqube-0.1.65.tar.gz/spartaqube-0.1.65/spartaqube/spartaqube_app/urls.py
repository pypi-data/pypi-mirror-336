from django.contrib import admin
from django.urls import path
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from.url_base import get_url_patterns as get_url_patterns_base
from.url_spartaqube import get_url_patterns as get_url_patterns_spartaqube
handler404='project.sparta_fc96e589c2.sparta_c2058265d4.qube_c8a40cd8db.sparta_1c026938d5'
handler500='project.sparta_fc96e589c2.sparta_c2058265d4.qube_c8a40cd8db.sparta_9d605022cd'
handler403='project.sparta_fc96e589c2.sparta_c2058265d4.qube_c8a40cd8db.sparta_11bd1abc93'
handler400='project.sparta_fc96e589c2.sparta_c2058265d4.qube_c8a40cd8db.sparta_c9338e036c'
urlpatterns=get_url_patterns_base()+get_url_patterns_spartaqube()
if settings.B_TOOLBAR:urlpatterns+=[path('__debug__/',include(debug_toolbar.urls))]
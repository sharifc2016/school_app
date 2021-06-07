"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView

from main import settings
from student.views import StudentListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^task/', include('task.urls')),
    url(r'^attendance/',include('attendance.urls')),
    url(r'^sms/', include('template_messages.urls')),
    url(r'^level/', include('level.urls')),
    url(r'^subject/', include('subject.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^student/', include('student.urls')),
    url(r'', include('student.urls')),
    url(r'^login/', RedirectView.as_view(url='/accounts/login/', permanent=True), name='login'),
    url(r'^logout/', RedirectView.as_view(url='/accounts/logout/', permanent=True), name='logout'),
    url(r'^password-change/', RedirectView.as_view(url='/accounts/password/change/'), name='password_change'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

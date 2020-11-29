"""
Definition of urls for Instidropbox.
"""

from datetime import datetime
from django.conf.urls import url
from django.conf.urls.static import static
import django.contrib.auth.views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^sign_up$', app.views.sign_up, name='sign_up'),

    url(r'^mydashboard$', app.views.mydashboard, name='mydashboard'),
    url(r'^studentgrievances$', app.views.studentgrievances, name='studentgrievances'),
    url(r'^sendgrievance$', app.views.sendgrievance, name='sendgrievance'),
    url(r'^sendgrievance/(?P<id>\d+)$', app.views.viewfaculty, name='viewfaculty'),

    #need to write faculty panel urls here
    url(r'^f_viewgrievances$', app.views.f_viewgrievances, name='f_viewgrievances'),
    url(r'^deptgrievances$', app.views.deptgrievances, name='deptgrievances'),
    url(r'^editstudentreq/(?P<id>\d+)$', app.views.editstudentreq, name='editstudentreq'),
    url(r'^f_updatereq/(?P<id>\d+)$', app.views.updatereq, name='f_updatereq'),
    url(r'^delete/(?P<id>\d+)$', app.views.destroy),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^sign_up$', app.views.sign_up, name='sign_up'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


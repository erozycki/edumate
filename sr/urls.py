from django.conf.urls import url, include
from . import views


app_name = 'sr'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^register/$', views.register, name='register'),
    url(r'^decks/$', views.decks, name='decks'),
    url(r'^why-edumate/$', views.why_edumate, name='why-edumate'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact-success/$', views.contact_success, name='contact-success'),
    url(r'^browse-decks/$', views.browse_decks, name='browse-decks'),
    url(r'getting-started/$', views.getting_started, name='getting-started'),
]

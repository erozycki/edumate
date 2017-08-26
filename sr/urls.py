from django.conf.urls import url, include
from . import views


from django.views.static import serve
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
    url(r'^getting-started/$', views.getting_started, name='getting-started'),
    url(r'^.well-known/pki-validation/C06F6C31FEB8E0E0454C35722593BC00.txt$', views.ssl_validation),
    url(r'^.well-known/pki-validation/A74E04808631445013DE8BEC11187C75.txt$', views.ssl_validation),

    url(r'^decks/details/(?P<deck_name>.*)/$', views.deck_details, name='deck-details'),
    url(r'^decks/add-decks/(?P<deck_name>.*)/$', views.add_deck, name='add-deck'),
#    url(r'^.well-known/pki-validation/C06F6C31FEB8E0E0454C35722593BC00.txt$', serve, {),
]

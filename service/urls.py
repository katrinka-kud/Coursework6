from django.urls import path
from django.views.decorators.cache import cache_page

from service.apps import ServiceConfig
from service.views import ClientListView, HomeView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MailingSetupListView, MailingSetupDetailView, MailingSetupCreateView, MailingSetupUpdateView, \
    MailingSetupDeleteView, LogsListView

app_name = ServiceConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logs/', LogsListView.as_view(), name='logs_list'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/detail/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),
    path('mailingsetup/', MailingSetupListView.as_view(), name='mailingsetup_list'),
    path('mailingsetup/detail/<int:pk>/', MailingSetupDetailView.as_view(), name='mailingsetup_detail'),
    path('mailingsetup/create/', MailingSetupCreateView.as_view(), name='mailingsetup_create'),
    path('mailingsetup/<int:pk>/update', MailingSetupUpdateView.as_view(), name='mailingsetup_update'),
    path('mailingsetup/<int:pk>/delete', MailingSetupDeleteView.as_view(), name='mailingsetup_delete'),
]

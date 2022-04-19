from django.urls import path

from mailing_api.views import ClientView, SingleClientView, MailingView, SingleMailingView, MessageFromMailingStat

app_name = 'mailing_api'

urlpatterns = [
    path('clients/', ClientView.as_view()),
    path('clients/<int:pk>', SingleClientView.as_view()),
    path('mailing/', MailingView.as_view()),
    path('mailing/<int:pk>', SingleMailingView.as_view()),
    path('mailing/statistic/<int:pk>', MessageFromMailingStat.as_view()),
]

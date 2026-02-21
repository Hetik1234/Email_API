from django.urls import re_path
from .views import SendEmailView

urlpatterns = [
    # The /? at the end means "the slash is optional"
    re_path(r'^send/?$', SendEmailView.as_view(), name='send-email'),
]
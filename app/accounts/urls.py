from django.conf.urls import url, include
from .views import LoginView, SignupView
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', logout_then_login, name="logout-url"),
    url(r'^signup/', SignupView.as_view(), name="signup-url")
]

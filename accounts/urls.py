from unicodedata import name
from django.urls import path
from . import views

urlpatterns=[
    path('register',views.register,name="register"),
    path('profile_update/<slug:pk>',views.profile_update,name="profile_update"),
    path('login1',views.login1,name="login1"),
    path('logout',views.logout,name="logout"),
    path('token',views.token_sent,name="token_sent"),
    path('verify/<auth_tokens>',views.verify,name="verify"),
    path('onboarding',views.onboarding,name="onboarding"),
]

from .views import SignupView
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
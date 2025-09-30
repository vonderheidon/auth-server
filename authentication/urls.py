from django.urls import path
from .views import RegisterView, LoginView, ValidateTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('validate-token/', ValidateTokenView.as_view(), name='auth-validate-token'),
]
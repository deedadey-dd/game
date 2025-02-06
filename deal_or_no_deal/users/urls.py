from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.UserRegistrationView.as_view(), name='api_register'),
    path('login/', api_views.login_view, name='api_login'),
    path('password-reset/', api_views.RequestPasswordResetView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', api_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('token/', api_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]

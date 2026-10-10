from django.urls import path

from .views import LogoutAPI, RegisterAPI 

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('reg/', RegisterAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
]
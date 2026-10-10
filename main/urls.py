from django.urls import path
from .views import LoanListAPI, PaymentListAPI, LoanSumAPI

urlpatterns = [
    path('', LoanListAPI.as_view()),
    path('sum', LoanSumAPI.as_view()),
    path('<int:pk>', PaymentListAPI.as_view())
]
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated 
from django.db.models import Case, When, Q, Sum, F, Value, FloatField, BooleanField, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce

from .models import Loan, Payment
from .serializers import LoanListSerializer, PaymentListSerializer
# Create your views here.

class LoanListAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            serializer = LoanListSerializer(data=request.data, context={'user':request.user})
            if serializer.is_valid():
                res = serializer.save()
                return Response({'success':'created'}, status=status.HTTP_201_CREATED)
            raise Exception(str(serializer.errors))
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request):
        try:
            loans = Loan.objects.annotate(
                total=Coalesce(Sum('payments__amount'), Value(0.0), output_field=FloatField()),
            ).annotate(
                remaining=ExpressionWrapper(
                    F('payback') - F('total'),
                    output_field=FloatField()
                ),
                completed = Case(
                    When(
                        Q(total__gte=F('payback')),
                        then=Value(True)
                    ),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).filter(user=request.user).order_by('completed', 'due')
            serializer = LoanListSerializer(loans, many=True)
            return Response(serializer.data) 
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentListAPI(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, pk):
        try:
            loan = Loan.objects.get(pk=pk, user=request.user)
            serializer = PaymentListSerializer(data=request.data, context={'pk':loan, 'user':request.user})
            if serializer.is_valid():
                value = serializer.save()
                return Response({'success':"created"}, status=status.HTTP_201_CREATED)
            raise Exception(serializer.errors)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    def get(self, request, pk):
        try:
            data = Payment.objects.filter(loan_id=pk, user=request.user).order_by('-date')
            serializer = PaymentListSerializer(data, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoanSumAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        
        try:
            agg = Loan.objects.filter(user=request.user).aggregate(
                total_borrowed = Coalesce(Sum(
                    'amount'
                ), 0.0, output_field=DecimalField()),
                total_payback = Coalesce(Sum(
                    'payback'
                ),0.0,
                                         output_field=DecimalField())
            )
            agg2 = Payment.objects.filter(user=request.user).aggregate(
                total_paid = Coalesce(Sum(
                    'amount'
                ), 0.0, output_field=DecimalField()),
            )
            sum1 = {
                'total_borrowed': agg['total_borrowed'],
                'total_interest': agg['total_payback'] - agg['total_borrowed'],
                'total_paid': agg2['total_paid'],
                'total_remaining': agg['total_payback'] - agg2['total_paid']
            }
            return Response(sum1)
        except Exception as e:
            print(e)
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
            
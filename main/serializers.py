from rest_framework import  serializers
from .models import Loan, Payment

class LoanListSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(read_only=True)
    remaining = serializers.FloatField(read_only=True)
    completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Loan 
        fields = ['id', 'vendor', 'date', 'due', 'amount', 'payback', 'total', 'remaining', 'completed', 'description']

    def validate(self, data):
        vendor = data.get('vendor', getattr(self.instance, 'vendor', None))
        amount = data.get('amount', getattr(self.instance, 'amount', None))
        payback = data.get('payback', getattr(self.instance, 'payback', None))
        date = data.get('date', getattr(self.instance, 'date', None))
        due = data.get('due', getattr(self.instance, 'due', None))
        description = data.get('description', getattr(self.instance, 'description', None))

        if not vendor or vendor.strip() == '':
            raise serializers.ValidationError("vendor is required")
        if amount <= 0 or payback <= 0:
            raise serializers.ValidationError("amount and payback amount greater than 0 is required")
        if not date or not due:
            raise serializers.ValidationError("date borrowed and payback date is required")
        if date and due and due < date:
            raise serializers.ValidationError("Due date must be ahead of the date borrowed")

        return data 

    def create(self, validated_data):
        user = self.context['user']
        return Loan.objects.create(user=user, **validated_data) 


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields=['id','amount','date']

    def validate(self, data):
        amount = data.get('amount', getattr(self.instance, 'amount', 0))

        if amount <= 0:
            raise serializers.ValidationError('invalid amount')

        return data 

    def create(self, validated_data):
        pk = self.context['pk']
        user = self.context['user']
        return Payment.objects.create(loan=pk, user=user,  **validated_data)
        
            
        
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status, serializers


from rest_framework_simplejwt.tokens import RefreshToken 

from .serializers import RegisterSerializer 

# Create your views here.

class RegisterAPI(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({'access':str(refresh.access_token), 'refresh':str(refresh)}, status=status.HTTP_201_CREATED)
            raise serializers.ValidationError(serializer.errors)
        except serializers.ValidationError as f:
            message = ",".join([str(f.detail[m][0]) for m in f.detail.keys()])
            return Response({'error':message}, status=400)
        except Exception as e:
            return Response({'error':str(e)}, status=400)

class LogoutAPI(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
                return Response({'message':'logout successful'})
            return Response({'error':'incomplete request'}, status=400)
        except Exception as e:
            return Response({'error':str(e)})
            
    

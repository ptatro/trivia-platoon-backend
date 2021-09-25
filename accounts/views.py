from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer
from .models import CustomUser


class SignupView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
    authentication_classes = ()
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            email = serializer.validated_data["email"]

            CustomUser.objects.create_user(username=username, password=password, email=email)
          


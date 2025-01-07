 
from .models import MyUser 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
import jwt
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return the current user's details
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # Update the current user's details
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    # Get the ID token from the request data
    idTokens = request.data.get('idToken')

    if not idTokens:
        return Response({"error": "idToken is required"}, status=400)

    try:
        # Decode the token without verifying the signature
        decoded_token = jwt.decode(idTokens, options={"verify_signature": False})

        # Access the decoded data
        email = decoded_token.get('email')
        name = decoded_token.get('name')
        first_name = decoded_token.get('given_name')  # Assuming 'given_name' is the first name
 
        picture = decoded_token.get('picture')

        # Check if the user already exists
        user = MyUser.objects.filter(email=email).first()

        if user:
            # If the user exists, get or create the token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "User already exists. Token returned.",
            })
        
        # If the user doesn't exist, create a new one
        user = MyUser.objects.create_user(
            email=email,
            first_name=first_name,
            is_active=True  # Automatically verify the user
        )
       
        token = Token.objects.create(user=user)

        return Response({
            "token": token.key,
            "message": "User created successfully. Token returned.",
        })
    
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=400)
    except jwt.DecodeError:
        return Response({"error": "Error decoding the token"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)




 
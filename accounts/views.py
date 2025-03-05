from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth import login,logout
from rest_framework import status
from rest_framework.views import APIView
from app2.models import AboutUS
from accounts.serializers import  (UserLoginSerializer, 
                                  UserRegistrationSerializer,
                                  UserProfileSerializer,
                                  UserChangePasswordSerializer,
                                  SendPasswordResetEmailSerializer,
                                  UserPasswordResetSerializer,
                                  UserSerializer,
                                  OTPValidationSerializer,
                                  AboutUSSerializer,
                                  UserRewardSerializers
                                )
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from . models import User,UserOTP,UserReward
from rest_framework import generics


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }



  
def format_serializer_errors(serializer):
    error_detail = {}
    for field, errors in serializer.errors.items():
        error_detail[field] = [str(error) for error in errors]

    return error_detail

def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        'error': message,
        'success': 'false',
    }, status=status_code)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            if self.request.user.is_admin==True:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserRegistrationView(APIView):
  #renderer_classes = [UserRenderer]
  def post(self, request, format=None):
      try:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        UserReward.objects.create(user=user)
        token = get_tokens_for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token,
            'message': 'Register Successful!',
            'success': 'true',
        }, status=status.HTTP_201_CREATED)
      except Exception as e:
          return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
       

class UserLoginView(APIView):
#   renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    if User.objects.filter(email =email):
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            login(request, user)
            return Response({'user':UserSerializer(user).data,'token':token, 'message':'Login Successfully !', 'success':'true'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Password Invalid !','success':'false'}, status=status.HTTP_404_NOT_FOUND)
    else:
       return Response({'message':'User does not exists!', 'success':'false'}, status=status.HTTP_400_BAD_REQUEST)
      

class UserProfileView(APIView):
  # renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response({'user':UserSerializer(request.user).data,'message':'User get successfully', 'success':'true'}, status=status.HTTP_200_OK)



  def put(self, request, formate = None):
    profile = request.user
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'user':UserSerializer(request.user).data,'message':'Update  successfully !', 'success':'true'}, status=status.HTTP_200_OK)




class UserChangePasswordView(APIView):
  # renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    oldpassword = serializer.validated_data['oldPassword']
    password = serializer.validated_data['newPassword']
    password2 = serializer.validated_data['confirmPassword']
    user = request.user
    if user.check_password(oldpassword):
      if password != password2:
        return Response({'message':"Password doesn't match !",'success':'false'}, status = status.HTTP_400_BAD_REQUEST)
      user.set_password(password)
      user.save()
      return Response({'message':'Password Change Successfully !','success':'true'}, status=status.HTTP_200_OK)
    return Response({'message':"Old Password does not match !",'success':'false'}, status=status.HTTP_400_BAD_REQUEST)
    
   
  
class SendPasswordResetEmailView(APIView):
  # renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    try:
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'message': 'Verify your email!', 'success': 'true'}, status=status.HTTP_200_OK)

    except ValidationError as e:
        if 'non_field_errors' in e.detail:
            error_message = e.detail['non_field_errors'][0]
            return Response({'error': error_message, 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': str(e), 'success': 'false'}, status=status.HTTP_400_BAD_REQUEST)



class UserPasswordResetView(APIView):
  # renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Reset Successfully !','success':'true'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
  # renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    print(request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'message':'An OTP code has been sent to your email. Please check your email and use the code to reset your password', 'success':'true'}, status=status.HTTP_200_OK)

class OTPValidation(APIView):
    def post(self, request, format=None):
        serializer = OTPValidationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            response_data = {'message': 'OTP code validated successfully!', 'success': True, 'user_id': user.id}
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'OTP code validation failed!', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


from django.utils import timezone
class UserPasswordResetView(APIView):
    def post(self, request, format=None):
        user_id = request.data.get('user_id')  
        user = User.objects.get(id=user_id)
        password_reset_serializer = UserPasswordResetSerializer(data=request.data, context={'user': user})
        
        if password_reset_serializer.is_valid():
            new_password = password_reset_serializer.validated_data['newPassword']
            confirm_password = password_reset_serializer.validated_data['confirmPassword']

            if new_password != confirm_password:
                return Response({'message': 'New password and confirm password do not match.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            userotp = UserOTP.objects.get(user=user)
            if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
                return Response({'message': 'OTP code has expired.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            # Reset the password for the user
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successfully!', 'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to reset the password!', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

# logout User
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        print("Received refresh token:", refresh_token)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                print("Successfully logged out.")
                return Response({"detail": "Successfully logged out."})
            except Exception as e:
                print("Error during logout:", e)
                return Response({"detail": "Invalid token or token expired."}, status=400)
        else:
            print("Refresh token not provided.")
            return Response({"detail": "Refresh token not provided."}, status=400)
        
   

class AboutUsView(APIView):
    def get(self, request):
        try:
            aboutus = AboutUS.objects.first()
            serializer = AboutUSSerializer(aboutus)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
''' user rewards list views'''
class UserRewardViews(generics.ListAPIView):
    serializer_class = UserRewardSerializers
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        queryset = UserReward.objects.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data[0]) 
        
        
''' social login with facebook and google'''
import requests
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

class SocialRegisterLoginView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            email = data.get('email')

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                login_view_instance = UserLoginView()
                login_request = request._request
                login_request.data = {'email': existing_user.email, 'password': existing_user.name}
                return login_view_instance.post(login_request)   
            else:   
                user_data={
                    'email': data.get('email'),
                    'name': data.get('name'),
                    'image_url':data.get('photo'),
                    'password': data.get('name'),  
                    'password2':  data.get('name'), 
                }
                
                serializer = UserRegistrationSerializer(data=user_data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    
                    UserReward.objects.create(user=user)
                    
                    token = get_tokens_for_user(user)
                    
                    user_data = UserSerializer(user).data
                    
                    return Response({
                        'user': user_data,
                        'token': token,
                        'message': 'Register Successful!',
                        'success': True,
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({"errors":serializer.errors,"success":False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

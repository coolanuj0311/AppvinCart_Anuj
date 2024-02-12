from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounted.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from accounted.renderers import UserRenderer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer,TemplateHTMLRenderer]
  template_name = 'register.html'

  def get(self, request, format =None):
       reg = UserRegistrationSerializer()
       return Response({'reg': reg},template_name = self.template_name)
     
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the home page after successful login
            # return redirect('home')  # Assuming 'home' is the name of your home page URL
        else:
            # Authentication failed, handle accordingly
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')


class UserLoginView(APIView):
   
    renderer_classes =[UserRenderer, TemplateHTMLRenderer]
    template_name = 'login.html'
   
    def get(self, request, format=None):
        login_form = UserLoginSerializer()
        return Response({'login_form': login_form}, template_name=self.template_name)
   
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        #for redirection to page with this url
        if serializer.is_valid(raise_exception = True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            # using these it will authenticate and check if there any user with it or not
            user=authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token ,'msg':'Login Success'}, status = status.HTTP_201_CREATED)
                return redirect('home')
            else:
                return Response({'errors':{'non_field_errors': ['Email or Password is not valid']}}, status = status.HTTP_404_NOT_FOUND)
 
class UserProfileView(APIView):
  renderer_classes = [UserRenderer,TemplateHTMLRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response({"profile":serializer.data}, status = status.HTTP_200_OK, template_name='profile.html')
  


 

class UserChangePasswordView(APIView):
   
    renderer_classes = [UserRenderer, TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]  # Require authentication
    template_name = 'changepassword.html'
   
    def get(self, request, format=None):
        change_password_form = UserChangePasswordView()
        return Response({'login_form': change_password_form}, template_name=self.template_name)
   
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.shortcuts import render


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer,TemplateHTMLRenderer]
    
    def get(self, request, format=None):
        return render(request, 'email_reset_password.html')
        
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link sent. Please check your email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer,TemplateHTMLRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid():
            # Process the form data
            # For example, you can save the new password here
            return render(request, 'password_reset_form.html', {'uid': uid, 'token': token})
        else:
            # Handle invalid form data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

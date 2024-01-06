from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from .models import FileModel
from .serializers import FileModelSerializer,UserSerializer
from django.middleware.csrf import get_token
from django.conf import settings

from django.shortcuts import get_object_or_404
import itsdangerous


@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token':csrf_token})


@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(request.data)
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        #         csrf_token = get_token(request)
        #         {'csrf_token':csrf_token}

        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read-only permissions are allowed for any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Superuser can perform write operations.
        return request.user and request.user.is_superuser
    
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        password = serializer.data.get('password')

        # Set user password and save
        user.set_password(password)
        user.save()

        # Send verification email
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
        host_name = request.get_host()
        verification_link = f'http://{host_name}{verification_url}'

        send_mail(
            'Verify Your Email',
            f'Click the following link to verify your email: {verification_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'User created successfully. Verification email sent.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)

        return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@permission_classes([IsSuperuserOrReadOnly])
def upload_file(request):
    
    serializer = FileModelSerializer(data=request.data,context={'request': request})
    
    if not request.user.is_superuser:
        return Response({'message': 'Only Operational User has access to upload files'}, status=status.HTTP_403_FORBIDDEN)
    
    if serializer.is_valid():
        
        valid_extensions = ['pptx','docx','xlsx']
        check_extension = serializer.validated_data['file'].name.split('.')[-1].lower()
        # above code - splits file name and last word (extension) is returned
        # now, we have to check whether it is in valid_extension list or not
        
        if check_extension in valid_extensions:
            
            serializer.save()
            return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        
       
        return Response({'error': 'Invalid file type. Only pptx, docx, and xlsx are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

SECRET_KEY = b'My_$uP3r_S3cR3t_K3y_123'

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_file(request, file_id):
    file = get_object_or_404(FileModel, id=file_id)
    
    print(file.file.name)

    # Generate and store a secure token for the download link
    secure_token = generate_secure_token(file, request.user)

    # Append the secure token to the download link
    download_link = f'/download/{file_id}/?token={secure_token}'

    return Response({'download_link': download_link, 'message': 'success'})

# Function to generate a secure token
def generate_secure_token(file, user):
    serializer = itsdangerous.URLSafeSerializer(SECRET_KEY)
    file_id = file.id  # Assuming 'id' is the primary key field of FileModel
    user_id = user.id  # Assuming 'id' is the primary key field of User

    # Serialize only the necessary information
    data = {'file_id': file_id, 'user_id': user_id}

    return serializer.dumps(data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_uploaded_files(request):
    files = FileModel.objects.all()
    serializer = FileModelSerializer(files, many=True)
    return Response({'files': serializer.data})
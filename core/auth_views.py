from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username         = request.data.get('username', '').strip()
    email            = request.data.get('email', '').strip()
    password         = request.data.get('password', '')
    confirm_password = request.data.get('confirm_password', '')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=400)
    if password != confirm_password:
        return Response({'error': 'Passwords do not match.'}, status=400)
    if len(password) < 6:
        return Response({'error': 'Password must be at least 6 characters.'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken.'}, status=400)

    User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'Account created successfully!'}, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_view(request):
    username         = request.data.get('username', '').strip()
    new_password     = request.data.get('new_password', '')
    confirm_password = request.data.get('confirm_password', '')

    if not username:
        return Response({'error': 'Username is required.'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Username not found.'}, status=404)

    # Step 1 check — just verifying user exists
    if new_password == 'check_only_temp':
        return Response({'message': 'User found.'}, status=200)

    if new_password != confirm_password:
        return Response({'error': 'Passwords do not match.'}, status=400)
    if len(new_password) < 6:
        return Response({'error': 'Password must be at least 6 characters.'}, status=400)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password reset successfully!'}, status=200)
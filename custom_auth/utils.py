from rest_framework.exceptions import AuthenticationFailed
import jwt
from .serializers import CustomUserSerializer
from .models import CustomUser
from rockerboy_backend_app.settings import SECRET_KEY

def get_auth_token(request):
    token = request.META['HTTP_AUTHORIZATION']
    token_splitted = token.split(" ")

    if token_splitted[0] != "Bearer" or len(token_splitted) != 2:
        raise AuthenticationFailed("Error parsing authorization token")
    
    return token_splitted[1]


def get_user_from_request(request):
    token = get_auth_token(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token is either invalid or expired')
    
    get_username = payload['id']

    user = CustomUser.objects.get(username=get_username)
    serializer = CustomUserSerializer(user)

    return serializer.data
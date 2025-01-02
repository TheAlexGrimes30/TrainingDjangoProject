import jwt
from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from AuthApp.models import CustomUser
from FridgeProject import settings


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ['/login/', '/register/']
        if resolve(request.path_info).url_name in excluded_paths:
            return

        auth_header  = request.META.get('HTTP_AUTHORIZATION', None)

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            try:
                # Декодирование токена
                payload = jwt.decode(
                    token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.JWT_ALGORITHM]
                )

                user = CustomUser.objects.get(id=payload['user_id'])
                request.user = user

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=401)

        else:
            request.user = None

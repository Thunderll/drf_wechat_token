from django.contrib.auth import get_user_model
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView

from wechattoken.models import Token
from wechattoken.serializers import AuthTokenSerializer

User = get_user_model()


class ObtainAuthToken(APIView):
    """生成并返回Token

    请求和响应均为json类型.
    通过小程序post请求发送code, 经AuthTokenSerializer验证后返回
    openid和session_key.

    使用用户标识openid生成一个user实例, 方便视图对用户权限的管理.
    """
    serializer_class = AuthTokenSerializer
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        openid = serializer.validated_data['openid']
        session_key = serializer.validated_data['session_key']

        user, _ = User.objects.get_or_create(
            username=openid,
            defaults={'password': openid}
        )
        token, _ = Token.objects.update_or_create(
            user=user, openid=openid,
            defaults={'session_key': session_key, 'key': ''}
        )

        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()

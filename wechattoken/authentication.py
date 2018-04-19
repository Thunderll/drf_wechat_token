# -*- coding:utf-8 -*-
from rest_framework.authentication import TokenAuthentication
from wechattoken.models import Token


class WechatTokenAuthentication(TokenAuthentication):
    keyword = 'WToken'
    model = Token

# drf_wechat_token
djangorestframework框架的微信小程序认证后端

环境: python(3.6)<br>
&emsp;&emsp;&ensp;django(2.0+)<br>
&emsp;&emsp;&ensp;djangorestframework(3+)

依赖: requests

1. 将该文件夹放置在django项目目录中(或app目录), 在`INSTALL_APPS`中添加`wechattekon`
```python
#settings.py
INSTALL_APPS =[
    ...
    'wechattoken'
]
```

配置rest_framework认证后端
```python
#.settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    ...
    'wechattoken.authentication.WechatTokenAuthentication',
    )
}
```
在settings中添加`WECHAT_APPID`和`WECAHT_SECRET`分别对应开发者的appid和secret.

2.添加obtain_auth_token视图到URLconf中
```python
#urls.py
from wechattoken import views
urlpatterns += [
    path('api_token_auth/', views.obtain_auth_token)
]
```
<br>
小程序使用post请求将用户的code发送给该视图,obtai_auth_token会生成并返回一个token

```python
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

将token存储在本地,之后的请求只需要在请求头中携带Authorization即可

```python
Authorization: WToken 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

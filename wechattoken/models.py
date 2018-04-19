import hashlib, binascii
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Token(models.Model):
    openid = models.CharField(max_length=28, primary_key=True)
    key = models.CharField(max_length=40, verbose_name=_('Key'))
    session_key = models.CharField(max_length=24)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_('User')
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    class Meta:
        verbose_name_plural = verbose_name = _('Token')

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_token(self.openid, self.session_key)
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_token(key, salt):
        # 使用openid和session_key加密生成token
        dk = hashlib.pbkdf2_hmac('sha256', key.encode(), salt.encode(), 100000, 20)
        return binascii.hexlify(dk).decode()

    def __str__(self):
        return self.key

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    自定义用户模型
    """
    # 账号字段（继承自AbstractUser的username，唯一约束）
    username = models.CharField(max_length=150, unique=True, verbose_name="账号")

    # 姓名字段
    name = models.CharField(max_length=150, verbose_name="姓名")

    # 邮箱字段（唯一约束）
    email = models.EmailField(unique=True, verbose_name="邮箱")

    # 手机号字段
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="手机号")

    # 是否为管理员
    is_admin = models.BooleanField(default=False, verbose_name="是否为管理员")

    # 其他字段继承自AbstractUser，包括密码、权限等

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

# customtest/forms.py

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomTestForm(forms.Form):
    k = forms.IntegerField(
        label="测试次数",
        validators=[
            MinValueValidator(1, message="测试次数不能小于1"),
            MaxValueValidator(10, message="测试次数不能大于10"),
        ],
        error_messages={
            'required': '测试次数不能为空',
            'invalid': '测试次数必须是整数'
        },
    )
    x = forms.IntegerField(
        label="样本数量",
        validators=[
            MinValueValidator(1, message="样本数量不能小于1"),
            MaxValueValidator(1000, message="样本数量不能大于1000"),
        ],
        error_messages={
            'required': '样本数量不能为空',
            'invalid': '样本数量必须是整数'
        },
    )

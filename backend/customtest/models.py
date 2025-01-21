# customtest/models.py

from django.db import models


class ImageData(models.Model):
    DATASET_CHOICES = (
        ('train', 'Train'),
        ('test', 'Test'),
    )
    file = models.FileField(upload_to='image_files/')  # 存储图片的路径
    label = models.IntegerField(choices=((0, 'None'), (1, 'Diatom')), default=0)
    dataset = models.CharField(max_length=5, choices=DATASET_CHOICES)  # 标明数据集是训练集还是测试集
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {'Diatom' if self.label == 1 else 'None'} - {self.dataset}"

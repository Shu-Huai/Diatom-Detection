# import_imagedata.py
import os
import django
from django.core.management.base import BaseCommand
from django.conf import settings

# 设置 Django 的 settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 初始化 Django 设置
django.setup()

# 然后继续导入模型
from customtest.models import ImageData


class Command(BaseCommand):
    help = '导入 PNG 文件到数据库并设置标签'

    def handle(self, *args, **kwargs):
        # 清空现有数据
        print("正在清空现有的 ImageData 数据...")
        ImageData.objects.all().delete()  # 删除所有现有数据
        print("现有数据已清空。")

        train_path = os.path.join(settings.BASE_DIR, 'media/train_png')
        test_path = os.path.join(settings.BASE_DIR, 'media/test_png')

        # 导入训练集
        self.import_images_from_folder(train_path, 'train')

        # 导入测试集
        self.import_images_from_folder(test_path, 'test')

    def import_images_from_folder(self, folder_path, dataset_type):
        print(f"开始导入文件夹: {folder_path}")
        # 遍历目录下的子文件夹（diatom 和 none）
        for label_name in ['diatom', 'none']:
            label = 1 if label_name == 'diatom' else 0
            subfolder_path = os.path.join(folder_path, label_name)
            print(f"正在检查子文件夹: {subfolder_path}")  # 输出子文件夹路径
            if os.path.exists(subfolder_path):
                for file_name in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file_name)

                    if file_name.endswith('.png'):
                        print(f"找到 PNG 文件: {file_path}")  # 输出找到的文件路径
                        # 直接保存 PNG 文件路径
                        ImageData.objects.create(
                            file=file_path,  # 保存 .png 文件路径
                            label=label,
                            dataset=dataset_type
                        )
                        print(f"已导入: {file_path}")
                    else:
                        print(f"跳过非 PNG 文件: {file_name}")
            else:
                print(f"子文件夹不存在: {subfolder_path}")

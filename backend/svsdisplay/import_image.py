import os
import django
import sys

# 设置项目路径和 Django 环境变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # backend 是你的 Django 项目名

# 初始化 Django
django.setup()

from svsdisplay.models import DiatomSlice, DiatomPatch
print("BASE_DIR:", os.path.dirname(os.path.abspath(__file__)))
slice_dir = os.path.join(BASE_DIR, './media/diatom_slices')
patch_dir = os.path.join(BASE_DIR, './media/diatom_patches')
# 检查目录并导入图片
for filename in os.listdir(slice_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        DiatomSlice.objects.create(image=f'diatom_slices/{filename}')

for filename in os.listdir(patch_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        DiatomPatch.objects.create(image=f'diatom_patches/{filename}')

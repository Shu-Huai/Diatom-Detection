# users/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from .models import User

SECRET_KEY = "your_secret_key"


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"code": 1, "msg": "请求数据格式错误"})

        username = data.get("account")  # 修改为前端发送的字段名
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"code": 1, "msg": "用户名或密码不能为空"})

        # 使用 Django 的 authenticate 方法验证用户
        user = authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({"code": 0, "msg": "登录成功",
                                 "username": user.username,
                                 "name": user.name,
                                 "is_admin": user.is_admin})
        else:
            return JsonResponse({"code": 1, "msg": "用户名或密码错误"})
    return JsonResponse({"code": 404, "msg": "请求方法错误"}, status=404)


@csrf_exempt
def user_list(request):
    if request.method == "GET":
        # 分页
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("pageSize", 10))
        start = (page - 1) * page_size
        end = start + page_size

        # 筛选
        search_query = request.GET.get("query", "")
        search_field = request.GET.get("field", "username")

        users = User.objects.all()
        if search_query:
            filter_kwargs = {f"{search_field}__icontains": search_query}
            users = users.filter(**filter_kwargs)

        total = users.count()
        users = users[start:end]

        user_data = [
            {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,  # 假设 phone 存在于 last_name
                "is_admin": user.is_admin,
            }
            for user in users
        ]

        return JsonResponse({"data": user_data, "total": total})


@csrf_exempt
def update_user_view(request, user_id):
    if request.method == 'PUT':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "用户不存在"}, status=404)

        data = json.loads(request.body)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        # 如果有修改管理员权限
        if "is_admin" in data:
            user.is_admin = data["is_admin"]
        user.save()
        return JsonResponse({"code": 0, "msg": "用户信息更新成功"})
    return JsonResponse({"code": 404, "msg": "请求方法错误"}, status=404)


@csrf_exempt
def create_user_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            name = data.get("name")
            password = data.get("password")
            email = data.get("email")
            phone = data.get("phone")
            is_admin = data.get("is_admin", False)

            if User.objects.filter(username=username).exists():
                print("dddddddd")
                return JsonResponse({"code": 1, "msg": "用户名已存在"}, status=400)

            user = User.objects.create_user(
                username=username,
                name=name,
                password=password,
                email=email,
                phone=phone,
                is_admin=is_admin
            )
            return JsonResponse({"code": 0, "msg": "用户创建成功", "data": {"id": user.id}})
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"用户创建失败: {str(e)}"}, status=400)
    return JsonResponse({"code": 404, "msg": "请求方法错误"}, status=404)


@api_view(['DELETE'])
def delete_users(request):
    try:
        user_ids = request.data.get("user_ids", [])
        if not user_ids:
            return Response({"code": 1, "msg": "未提供用户 ID 列表"}, status=400)

        deleted_count = User.objects.filter(id__in=user_ids).delete()[0]
        return Response({
            "code": 0,
            "msg": f"成功删除 {deleted_count} 个用户",
        }, status=200)
    except Exception as e:
        return Response({"code": 2, "msg": "服务器错误"}, status=500)


@csrf_exempt
def change_password_view(request, user_id):
    if request.method == "POST":
        data = json.loads(request.body)
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "用户不存在"}, status=404)

        # 简化做法：假设前端已经判断过是否是管理员/本人
        # 仍可在后端添加进一步检查
        if not user.check_password(old_password):
            return JsonResponse({"code": 1, "msg": "旧密码不正确"}, status=205)

        user.set_password(new_password)
        user.save()
        return JsonResponse({"code": 0, "msg": "密码修改成功"})
    return JsonResponse({"code": 404, "msg": "请求方法错误"}, status=404)

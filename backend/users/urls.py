# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import login_view, user_list, update_user_view, create_user_view, delete_users, change_password_view

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path("", user_list),
    path('update/<int:user_id>/', update_user_view, name='update_user_view'),
    path('change_password/<int:user_id>/', change_password_view),
    path("create/", create_user_view),
    path('delete/', delete_users, name='delete_users'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

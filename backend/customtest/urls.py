# customtest/urls.py
from django.urls import path
from .views import custom_test_view, export_excel_view, data

app_name = 'customtest'

urlpatterns = [
    path('custom-test/', custom_test_view, name='custom_test'),
    path('export-excel/', export_excel_view, name='export_excel'),
    path('data/', data, name='data'),
]

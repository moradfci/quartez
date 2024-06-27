from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessOwnerViewSet, EmployeeViewSet, CompanyViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'businessowner', BusinessOwnerViewSet)
router.register(r'employee', EmployeeViewSet)
router.register(r'company', CompanyViewSet)
router.register(r'review', ReviewViewSet)


urlpatterns = [
    
    path('api/', include(router.urls)),
    
]

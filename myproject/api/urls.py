# api/urls.py

from django.urls import path,include
from knox import views as knox_views
from rest_framework import routers
from .apiviews import RegisterView, LoginView
from .userroles.test import AdminOnlyView, StaffOnlyView, AdminOrStaffView, UserOnlyView

router = routers.DefaultRouter(trailing_slash=True)
urlpatterns = [
    path('', include(router.urls)), 
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('api/staff-only/', StaffOnlyView.as_view(), name='staff-only'),
    path('api/admin-or-staff/', AdminOrStaffView.as_view(), name='admin-or-staff'),
    path('api/useronly/', UserOnlyView.as_view(), name='admin-or-staff'),
]

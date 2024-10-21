from django.urls import path
from .views import UserLogin, UserCreate, UserDetails, UserList, Logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('user/create/', UserCreate.as_view(), name='user-create'),
    path('user/<int:pk>/', UserDetails.as_view(), name='user-detail'),
    path('users/', UserList.as_view(), name='user-list'),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', Logout.as_view())
]
from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegistererView, verify_view, UserUpdateView, user_password_recovery, \
    UserListView, switch_status

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('user_recovery/', user_password_recovery, name='user_password_recovery'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistererView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('verify/<str:verify_key>', verify_view, name='verify'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('switch_status/<int:pk>/', switch_status, name='switch_status')
]

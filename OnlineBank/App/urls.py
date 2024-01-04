
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('block_user/<int:pk>/', views.Block_user, name='block_user'),
    path('delete_user/<int:pk>/', views.Delete_user, name='delete_user'),
    # path('otp', views.Otp, name='opt'),
    # path('pin/<int:pk>/', views.Pin, name='pin'),

    path('login/', views.Login, name="login"),
    path('create_new_user/', views.Create_new_user, name="create_new_user"),
    path('logout/', views.UserLogout, name="logout"),

    path('', views.Index, name='index'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('all_users/', views.All_users, name='all_users'),
    path('view_profile/', views.View_profile, name='view_profile'),
    path('view_user/<int:pk>/', views.View_user, name='view_user'),
    path('complete_user/<int:pk>/', views.Complete_user, name='complete_user'),

    path('transfer/', views.Transfer, name='transfer'),
    path('transfer_finish/', views.Transfer_finish, name='transfer_finish'),
    path('confirm/', views.Confirm, name='confirm'),
    path('history/<int:pk>/', views.History, name='history'),
    

    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name='nav_auth/reset_password.html'),
    #     name='reset_password'),

    path('reset_password/', views.password_reset_request, name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='nav_auth/reset_password_sent.html'), 
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='nav_auth/reset.html'), 
        name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='nav_auth/reset_password_complete.html'), 
        name='reset_password_complete'),

]


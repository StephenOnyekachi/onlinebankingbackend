
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('block_user/<int:pk>/', views.Block_user, name='block_user'),
    path('delete_user/<int:pk>/', views.Delete_user, name='delete_user'),

    path('login/', views.Login, name="login"),
    path('create_new_user/', views.Create_new_user, name="create_new_user"),
    path('logout/', views.UserLogout, name="logout"),

    path('', views.Index, name='index'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('all_users/', views.All_users, name='all_users'),
    path('view_profile/', views.View_profile, name='view_profile'),
    path('view_user/<int:pk>/', views.View_user, name='view_user'),
    path('complete_user/<int:pk>/', views.Complete_user, name='complete_user'),
    # path('deleteuser/<int:pk>/', views.Deleteuser, name='deleteuser'),

    path('transfer/', views.Transfer, name='transfer'),
    path('transfer_finish/', views.Transfer_finish, name='transfer_finish'),
    path('confirm/', views.Confirm, name='confirm'),
    path('history/', views.History, name='history'),


    path('transfer1/', views.Transfer1, name='transfer1'),
    path('pin/', views.Transfer_finish1, name='pin'),
    path('confirm1/', views.Confirm1, name='confirm1'),
    

    # Password Reset URLs

    # path('password_reset/', views.password_reset_request, name='password_reset/'),

    # path('password_reset/', 
    #     auth_views.PasswordResetView.as_view(), 
    #     name='password_reset'),

    path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='nav_auth/reset_password.html'), 
        name='password_reset'),

    path('password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='nav_auth/reset_password_sent.html'), 
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='nav_auth/reset.html'), 
        name='password_reset_confirm'),

    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='nav_auth/reset_password_complete.html'), 
        name='password_reset_complete'),

]


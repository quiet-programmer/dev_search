from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.profiles, name='profiles'),
    path('user_profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('user_account/', views.userAccount, name='user_account'),
    path('edit_account/', views.editAccount, name='edit_account'),
    path('add_skills/', views.addSkills, name='add_skills'),
    path('update_skills/<str:pk>/', views.updateSkills, name='update_skills'),
    path('delete_skills/<str:pk>/', views.deleteSkills, name='delete_skills'),
    path('inbox/', views.messageInbox, name='inbox'),
    path('view_message/<str:pk>/', views.viewMessage, name='view_message'),
    path('send_message/<str:pk>/', views.createMessage, name='send_message'),

]
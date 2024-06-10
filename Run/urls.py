from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.registerUser, name='register'),
    path('login/', views.loginUser, name='loginpage'),
    path('logout/', views.logoutUser, name='logout'),

    path('dashboard/', views.Dashboard, name='dashboard'),
    path('addAchievement/', views.add_achievement, name='addAchievement'),
    path('achievement/edit/<slug:slug>/', views.edit_achievement, name='edit_achievement'),
    path('create-profile/', views.create_profile, name='create_profile'),

    path('all_data/', views.all_data, name='all_data'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
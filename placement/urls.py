from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard, name='dashboard'),
    path('about/', views.About, name='about'),
    path('allcompanies/', views.AllCompanies, name='allcompanies'),
    path('registeredcompanies/', views.RegisteredCompanies,
         name='registeredcompanies'),
    path('profile/', views.Profile, name='profile'),
    path('register/', views.RegisterDeregister, name='register-deregister'),
    path('edit-profile/',
         views.EditProfile.as_view(), name='edit-profile'),
    path('add-company/',
         views.AddCompany.as_view(), name='add-company'),
    path('job-profile/',
         views.AddJobProfile.as_view(), name='job-profile'),
    path('create-user/', views.CreateUser.as_view(), name='create-user'),
    path('create-profile/', views.CreateProfile.as_view(), name='create-profile'),
    path('add-other-details/', views.AddOtherDetails.as_view(),
         name='add-other-details'),
    path('add-current-education-details/', views.AddCurrentEducationDetails.as_view(),
         name='add-current-education-details'),
    path('add-past-education-details/', views.AddPastEducationDetails.as_view(),
         name='add-past-education-details'),
]

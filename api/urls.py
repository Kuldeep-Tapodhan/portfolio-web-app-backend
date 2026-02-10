from django.urls import path
from .views import *

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Profile endpoints
    path('profiles/', ProfileView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    
    # Skill endpoints
    path('skills/', SkillView.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', SkillView.as_view(), name='skill-detail'),
    
    # Experience endpoints
    path('experiences/', ExperienceView.as_view(), name='experience-list-create'),
    path('experiences/<int:pk>/', ExperienceView.as_view(), name='experience-detail'),
    
    # Project endpoints
    path('projects/', ProjectView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='project-detail'),
    
    # Certification endpoints
    path('certifications/', CertificationView.as_view(), name='certification-list-create'),
    path('certifications/<int:pk>/', CertificationView.as_view(), name='certification-detail'),
    
    # Education endpoints
    path('education/', EducationView.as_view(), name='education-list-create'),
    path('education/<int:pk>/', EducationView.as_view(), name='education-detail'),
    
    # Contact endpoints
    path('contacts/', ContactView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactView.as_view(), name='contact-detail'),

    # ContactInfo endpoints
    path('contactinfo/', ContactInfoView.as_view(), name='contactinfo-list-create'),
    path('contactinfo/<int:pk>/', ContactInfoView.as_view(), name='contactinfo-detail'),
]
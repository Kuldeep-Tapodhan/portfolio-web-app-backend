from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from .util.responses import APIResponse


from .serializers import CustomTokenObtainPairSerializer
from .models import (
    Profile, Skill, Experience, Project, Certification, Education, Contact,ContactInfo
)
from .serializers import (
    ProfileSerializer, SkillSerializer, ExperienceSerializer,
    ProjectSerializer, CertificationSerializer, EducationSerializer, 
    ContactSerializer,ContactInfoSerializer
)
from .util.cloudinary_util import upload_to_cloudinary
# ==================== Authentication ====================
# class LoginView(TokenObtainPairView):
#     """Custom JWT login view"""
#     serializer_class = CustomTokenObtainPairSerializer
#     permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """Custom JWT login view"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return APIResponse.get_serializer_error_response(
                APIResponse.Codes.INVALID_CREDENTIALS,
                status.HTTP_401_UNAUTHORIZED
            )
        
        return APIResponse.get_success_response(
            APIResponse.Codes.LOGIN_SUCCESS,
            serializer.validated_data,
            status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return APIResponse.get_success_response(
                APIResponse.Codes.LOGOUT_SUCCESS, 
                {"message": "Successfully logged out"},
                status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return APIResponse.get_serializer_error_response(
                APIResponse.Codes.VALIDATION_ERROR,
                status.HTTP_400_BAD_REQUEST
            )


# ==================== Profile Views ====================
class ProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk=None):
        if pk:
            profile = self.get_object(pk)
            serializer = ProfileSerializer(profile)
        else:
            profiles = Profile.objects.all().order_by('-created_at', '-id') 
            serializer = ProfileSerializer(profiles, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.PROFILE_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        data = request.data.copy() # Make mutable copy

        # Handle file uploads manually
        if 'profile_picture' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['profile_picture'], folder="profile_pictures")
            data['profile_picture'] = upload_result.get('secure_url')
        
        if 'resume' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['resume'], folder="resumes")
            data['resume'] = upload_result.get('secure_url')

        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.PROFILE_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        profile = self.get_object(pk)
        data = request.data.copy() # Make mutable copy

        # Handle file uploads manually
        if 'profile_picture' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['profile_picture'], folder="profile_pictures")
            data['profile_picture'] = upload_result.get('secure_url')
        
        if 'resume' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['resume'], folder="resumes")
            data['resume'] = upload_result.get('secure_url')

        serializer = ProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.PROFILE_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Skill Views ====================
class SkillView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Skill, pk=pk)

    def get(self, request, pk=None):
        if pk:
            skill = self.get_object(pk)
            serializer = SkillSerializer(skill)
        else:
            skills = Skill.objects.all().order_by('-created_at', '-id') 
            serializer = SkillSerializer(skills, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.SKILL_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.SKILL_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        skill = self.get_object(pk)
        serializer = SkillSerializer(skill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.SKILL_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        skill = self.get_object(pk)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Experience Views ====================
class ExperienceView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Experience, pk=pk)

    def get(self, request, pk=None):
        if pk:
            experience = self.get_object(pk)
            serializer = ExperienceSerializer(experience)
        else:
            experiences = Experience.objects.all().order_by('-created_at', '-id') 
            serializer = ExperienceSerializer(experiences, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.EXPERIENCE_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        data = request.data.copy()
        if 'logo' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['logo'], folder="company_logos")
            data['logo'] = upload_result.get('secure_url')

        serializer = ExperienceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.EXPERIENCE_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        experience = self.get_object(pk)
        data = request.data.copy()
        if 'logo' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['logo'], folder="company_logos")
            data['logo'] = upload_result.get('secure_url')

        serializer = ExperienceSerializer(experience, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.EXPERIENCE_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        experience = self.get_object(pk)
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Project Views ====================
class ProjectView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

    def get(self, request, pk=None):
        if pk:
            project = self.get_object(pk)
            serializer = ProjectSerializer(project)
        else:
            projects = Project.objects.all().order_by('-created_at', '-id') 
            serializer = ProjectSerializer(projects, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.PROJECT_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        data = request.data.copy()
        if 'image' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['image'], folder="project_images")
            data['image'] = upload_result.get('secure_url')

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.PROJECT_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data.copy()
        if 'image' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['image'], folder="project_images")
            data['image'] = upload_result.get('secure_url')

        serializer = ProjectSerializer(project, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.PROJECT_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Certification Views ====================
class CertificationView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Certification, pk=pk)

    def get(self, request, pk=None):
        if pk:
            cert = self.get_object(pk)
            serializer = CertificationSerializer(cert)
        else:
            certs = Certification.objects.all().order_by('-created_at', '-id') 
            serializer = CertificationSerializer(certs, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.CERTIFICATION_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        data = request.data.copy()
        if 'image' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['image'], folder="cert_images")
            data['image'] = upload_result.get('secure_url')
        
        if 'pdf_file' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['pdf_file'], folder="cert_pdfs")
            data['pdf_file'] = upload_result.get('secure_url')

        serializer = CertificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.CERTIFICATION_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        cert = self.get_object(pk)
        data = request.data.copy()
        if 'image' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['image'], folder="cert_images")
            data['image'] = upload_result.get('secure_url')
        
        if 'pdf_file' in request.FILES:
            upload_result = upload_to_cloudinary(request.FILES['pdf_file'], folder="cert_pdfs")
            data['pdf_file'] = upload_result.get('secure_url')

        serializer = CertificationSerializer(cert, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.CERTIFICATION_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        cert = self.get_object(pk)
        cert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Education Views ====================
class EducationView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Education, pk=pk)

    def get(self, request, pk=None):
        if pk:
            education = self.get_object(pk)
            serializer = EducationSerializer(education)
        else:
            educations = Education.objects.all().order_by('-created_at', '-id') 
            serializer = EducationSerializer(educations, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.EDUCATION_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.EDUCATION_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        education = self.get_object(pk)
        serializer = EducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.EDUCATION_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        education = self.get_object(pk)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================== Contact Views ====================
class ContactView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        """
        Custom permission logic:
        - POST requests: AllowAny (anyone can submit contact form)
        - Other requests (GET, PUT, DELETE): IsAdminUser
        """
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_object(self, pk):
        return get_object_or_404(Contact, pk=pk)

    def get(self, request, pk=None):
        if pk:
            contact = self.get_object(pk)
            serializer = ContactSerializer(contact)
        else:
            contacts = Contact.objects.all().order_by('-created_at', '-id') 
            serializer = ContactSerializer(contacts, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.CONTACT_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.CONTACT_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        contact = self.get_object(pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.CONTACT_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        contact = self.get_object(pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ==================== ContactInfo Views ====================

class ContactInfoView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(ContactInfo, pk=pk)

    def get(self, request, pk=None):
        if pk:
            contact_info = self.get_object(pk)
            serializer = ContactInfoSerializer(contact_info)
        else:
            contact_infos = ContactInfo.objects.all().order_by('-created_at', '-id') 
            serializer = ContactInfoSerializer(contact_infos, many=True)
        
        return APIResponse.get_success_response(
            APIResponse.Codes.CONTACTINFO_RETRIEVED, 
            serializer.data
        )

    @transaction.atomic
    def post(self, request):
        serializer = ContactInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.CONTACTINFO_CREATED, 
                serializer.data,
                status.HTTP_201_CREATED
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def put(self, request, pk):
        contact_info = self.get_object(pk)
        serializer = ContactInfoSerializer(contact_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return APIResponse.get_success_response(
                APIResponse.Codes.CONTACTINFO_UPDATED, 
                serializer.data
            )
        return APIResponse.get_serializer_error_response(
            APIResponse.Codes.VALIDATION_ERROR, 
            serializer.errors
        )

    @transaction.atomic
    def delete(self, request, pk):
        contact_info = self.get_object(pk)
        contact_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

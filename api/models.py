from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    # Added blank=True, null=True to allow creating profile without uploading image immediately
    profile_picture = models.URLField(blank=True, null=True) 
    resume = models.URLField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    leetcode_link = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('LANG', 'Programming Languages'),
        ('WEB', 'Web Technologies'),
        ('AI', 'AI/ML Technologies'),
        ('SOFT', 'Soft Skills'),
    ]
    name = models.CharField(max_length=50)
    percentage = models.IntegerField()
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Experience(models.Model):
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    logo = models.URLField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.role} at {self.company_name}"

class Project(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, blank=True, null=True)
    github_link = models.URLField(blank=True)
    live_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Certification(models.Model):
    title = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    pdf_file = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Education(models.Model):
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class ContactInfo(models.Model):
    address = models.TextField()
    email = models.EmailField()
    description = models.TextField()
    phone = models.CharField(max_length=20)
    linkedin_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    leetcode_link = models.URLField(blank=True)

    def __str__(self):
        return "Contact Information"
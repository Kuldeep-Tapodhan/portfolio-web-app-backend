import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
django.setup()

from api.models import Profile, Skill, Experience, Project, Certification, Education
import datetime

def load_data():
    print("-----------------------------------")
    print("Starting data population script...")
    print("-----------------------------------")

    # --- 1. PROFILE ---
    print("Creating Profile...")
    if not Profile.objects.exists():
        Profile.objects.create(
            name="Kuldeep Tapodhan",
            title="Web Developer | AI/ML Enthusiast",
            bio="Welcome to my portfolio! I am Kuldeep Tapodhan, a passionate web developer with a keen interest in creating dynamic and responsive web applications.",
            email="kuldeep.tapodhan0306@gmail.com",
            phone="+91 9016568931",
            address="Samaras Boy's Hostel, Saurashtra University Campus, Rajkot, Gujarat 360005",
            github_link="https://github.com/Kuldeep-Tapodhan",
            linkedin_link="https://www.linkedin.com/in/kuldeep-tapodhan-780701251/",
            twitter_link="https://x.com/deeptapodhan143?t=pFEi5VLxsY1ud149SC5zqA&s=08",
            leetcode_link="https://leetcode.com/u/FeNEgYCzBq/"
        )
        print(" > Profile Created.")
    else:
        print(" > Profile already exists.")


    # --- 2. SKILLS ---
    print("Creating Skills...")
    skills_data = [
        {"name": "JavaScript", "percentage": 90, "category": "LANG"},
        {"name": "Python", "percentage": 85, "category": "LANG"},
        {"name": "Java", "percentage": 75, "category": "LANG"},
        {"name": "HTML", "percentage": 95, "category": "WEB"},
        {"name": "CSS", "percentage": 90, "category": "WEB"},
        {"name": "Django", "percentage": 85, "category": "WEB"},
        {"name": "Flask", "percentage": 80, "category": "WEB"},
        {"name": "FastAPI", "percentage": 80, "category": "WEB"},
        {"name": "TensorFlow", "percentage": 80, "category": "AI"},
        {"name": "Pandas", "percentage": 80, "category": "AI"},
        {"name": "Numpy", "percentage": 80, "category": "AI"},
        {"name": "Seaborn", "percentage": 80, "category": "AI"},
        {"name": "Matplotlib", "percentage": 80, "category": "AI"},
        {"name": "OpenCV", "percentage": 80, "category": "AI"},
        {"name": "PyTorch", "percentage": 80, "category": "AI"},
        {"name": "Problem Solving", "percentage": 90, "category": "SOFT"},
        {"name": "Team Collaboration", "percentage": 85, "category": "SOFT"},
        {"name": "Communication", "percentage": 80, "category": "SOFT"},
    ]

    for skill in skills_data:
        obj, created = Skill.objects.get_or_create(
            name=skill['name'],
            defaults={'percentage': skill['percentage'], 'category': skill['category']}
        )
        if created:
            print(f" > Skill added: {skill['name']}")

    # --- 3. EXPERIENCE ---
    print("Creating Experience...")
    Experience.objects.get_or_create(
        company_name="Karoza Tech",
        role="AI/ML Intern",
        defaults={
            "start_date": datetime.date(2025, 6, 1),
            "end_date": None,
            "description": "Worked on various projects that helped hone my skills in AI/ML, contributing to key development milestones."
        }
    )
    print(" > Experience added: Karoza Tech")


    # --- 4. PROJECTS ---
    print("Creating Projects...")
    projects_data = [
        {
            "title": "Disease prediction and Drug Recommendation(ML)",
            "description": "Built a web‑based machine learning app to predict diseases using Random Forest. Integrated Gemini API for disease info and health advice.",
            "github_link": "https://github.com/Kuldeep-Tapodhan/Disease-prediction-and-drug-recommendation/"
        },
        {
            "title": "Spotify Song Recommendation using KNN (ML)",
            "description": "Built a Spotify recommendation system that uses KNN to suggest songs based on features like actor, singer, and genre.",
            "github_link": "https://github.com/Kuldeep-Tapodhan/Bollywood-Song-Recommedation"
        }
    ]

    for proj in projects_data:
        obj, created = Project.objects.get_or_create(
            title=proj['title'],
            defaults={
                "description": proj['description'],
                "github_link": proj['github_link']
            }
        )
        if created:
            print(f" > Project added: {proj['title']}")

    # --- 5. CERTIFICATIONS ---
    print("Creating Certifications...")
    certs_data = [
        "AWS Machine Learning",
        "Python for Data Science",
        "Database Programming with SQL",
        "Java Programming",
        "AWS Academy Cloud Foundations"
    ]

    for cert_title in certs_data:
        obj, created = Certification.objects.get_or_create(title=cert_title)
        if created:
            print(f" > Certification added: {cert_title}")

    # --- 6. EDUCATION ---
    print("Creating Education...")
    edu_data = [
        {
            "institution": "Marwadi University, Rajkot",
            "degree": "Bachelor of Technology - Information Technology",
            "start_date": datetime.date(2022, 8, 1),
            "end_date": datetime.date(2026, 5, 31),
            "description": "Graduated with a CGPA of 8.5/10. Specialized in AI and Full‑Stack Web Development."
        },
        {
            "institution": "Adarsh Mahavidhyalay, Gandhidham",
            "degree": "Higher Secondary Certificate (HSC)",
            "start_date": datetime.date(2019, 6, 1),
            "end_date": datetime.date(2021, 5, 31),
            "description": "Completed high school with a focus on science and mathematics."
        }
    ]

    for edu in edu_data:
        obj, created = Education.objects.get_or_create(
            degree=edu['degree'],
            defaults={
                "institution": edu['institution'],
                "start_date": edu['start_date'],
                "end_date": edu['end_date'],
                "description": edu['description']
            }
        )
        if created:
            print(f" > Education added: {edu['degree']}")

    print("-----------------------------------")
    print("Data population completed successfully!")
    print("-----------------------------------")
    print("NOTE: Images were not uploaded here. Add logos/screenshots via the Django Admin Panel.")

if __name__ == '__main__':
    load_data()

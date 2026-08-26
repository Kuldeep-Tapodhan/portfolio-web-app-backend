import os
import django
import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
django.setup()

from api.models import Profile, Skill, Experience, Project, Certification, Education, ContactInfo

def load_data():
    print("-----------------------------------")
    print("Starting non-destructive data merge script...")
    print("-----------------------------------")

    # --- 1. PROFILE ---
    print("Merging Profile...")
    profile = Profile.objects.first()
    if profile:
        profile.name = "Kuldeep Tapodhan"
        profile.title = "Python AI/ML Developer"
        profile.bio = (
            "AI & Machine Learning Developer with hands-on experience in building intelligent, "
            "scalable applications powered by LLMs, RAG pipelines, multi-agent voice systems, "
            "and computer vision models. Strong expertise in Python-based backend development using "
            "FastAPI, Django, and Flask, with practical experience integrating AI systems into real-world applications."
        )
        if not profile.email:
            profile.email = "kuldeep.tapodhan0306@gmail.com"
        if not profile.phone:
            profile.phone = "+91 9016568931"
        if not profile.address:
            profile.address = "Rajkot, Gujarat, India"
        if not profile.github_link:
            profile.github_link = "https://github.com/Kuldeep-Tapodhan"
        if not profile.linkedin_link:
            profile.linkedin_link = "https://www.linkedin.com/in/kuldeep-tapodhan-780701251/"
        if not profile.twitter_link:
            profile.twitter_link = "https://x.com/deeptapodhan143?t=pFEi5VLxsY1ud149SC5zqA&s=08"
        if not profile.leetcode_link:
            profile.leetcode_link = "https://leetcode.com/u/FeNEgYCzBq/"
        profile.save()
        print(f" > Profile updated: {profile.name} ({profile.title})")
    else:
        profile = Profile.objects.create(
            name="Kuldeep Tapodhan",
            title="Python AI/ML Developer",
            bio=(
                "AI & Machine Learning Developer with hands-on experience in building intelligent, "
                "scalable applications powered by LLMs, RAG pipelines, multi-agent voice systems, "
                "and computer vision models. Strong expertise in Python-based backend development using "
                "FastAPI, Django, and Flask, with practical experience integrating AI systems into real-world applications."
            ),
            email="kuldeep.tapodhan0306@gmail.com",
            phone="+91 9016568931",
            address="Rajkot, Gujarat, India",
            github_link="https://github.com/Kuldeep-Tapodhan",
            linkedin_link="https://www.linkedin.com/in/kuldeep-tapodhan-780701251/",
            twitter_link="https://x.com/deeptapodhan143?t=pFEi5VLxsY1ud149SC5zqA&s=08",
            leetcode_link="https://leetcode.com/u/FeNEgYCzBq/"
        )
        print(" > Profile created.")

    # --- 2. CONTACT INFO ---
    print("Merging Contact Info...")
    contact_info = ContactInfo.objects.first()
    if contact_info:
        contact_info.email = profile.email
        contact_info.phone = profile.phone
        contact_info.address = profile.address
        contact_info.description = "Python AI/ML Developer at Amenity Technologies specializing in LLMs, RAG Pipelines, Multi-Agent Voice Systems, and Full-Stack AI Solutions."
        contact_info.github_link = profile.github_link
        contact_info.linkedin_link = profile.linkedin_link
        contact_info.twitter_link = profile.twitter_link
        contact_info.leetcode_link = profile.leetcode_link
        contact_info.save()
        print(" > Contact Info updated.")
    else:
        ContactInfo.objects.create(
            address=profile.address,
            email=profile.email,
            phone=profile.phone,
            description="Python AI/ML Developer at Amenity Technologies specializing in LLMs, RAG Pipelines, Multi-Agent Voice Systems, and Full-Stack AI Solutions.",
            github_link=profile.github_link,
            linkedin_link=profile.linkedin_link,
            twitter_link=profile.twitter_link,
            leetcode_link=profile.leetcode_link
        )
        print(" > Contact Info created.")

    # --- 3. SKILLS (MERGE) ---
    print("Merging Skills...")
    skills_list = [
        # Languages
        {"name": "Python", "percentage": 95, "category": "LANG"},
        {"name": "Java", "percentage": 85, "category": "LANG"},
        {"name": "Advanced Java (JSP, JDBC)", "percentage": 80, "category": "LANG"},
        {"name": "JavaScript", "percentage": 80, "category": "LANG"},
        {"name": "Kotlin", "percentage": 75, "category": "LANG"},
        {"name": "HTML", "percentage": 95, "category": "WEB"},
        {"name": "CSS", "percentage": 90, "category": "WEB"},

        # Web & Backend
        {"name": "FastAPI", "percentage": 92, "category": "WEB"},
        {"name": "Django", "percentage": 90, "category": "WEB"},
        {"name": "Flask", "percentage": 85, "category": "WEB"},
        {"name": "REST API Development", "percentage": 95, "category": "WEB"},
        {"name": "Streamlit", "percentage": 85, "category": "WEB"},
        {"name": "HTML5, CSS3, TailwindCSS", "percentage": 85, "category": "WEB"},

        # AI / ML / Data Science
        {"name": "Machine Learning", "percentage": 90, "category": "AI"},
        {"name": "Deep Learning", "percentage": 88, "category": "AI"},
        {"name": "PyTorch", "percentage": 85, "category": "AI"},
        {"name": "OpenCV", "percentage": 85, "category": "AI"},
        {"name": "Scikit-learn", "percentage": 90, "category": "AI"},
        {"name": "TensorFlow", "percentage": 80, "category": "AI"},
        {"name": "RAG Pipelines", "percentage": 92, "category": "AI"},
        {"name": "LangChain", "percentage": 85, "category": "AI"},
        {"name": "Vector DBs (ChromaDB)", "percentage": 90, "category": "AI"},
        {"name": "Embeddings (Sentence Transformers)", "percentage": 88, "category": "AI"},
        {"name": "LLM Integration (Llama 3.3, BioMistral)", "percentage": 90, "category": "AI"},
        {"name": "Prompt Engineering", "percentage": 92, "category": "AI"},
        {"name": "Multi-Agent Systems", "percentage": 88, "category": "AI"},
        {"name": "Pandas", "percentage": 90, "category": "AI"},
        {"name": "Numpy", "percentage": 90, "category": "AI"},
        {"name": "Data Processing (Pandas, NumPy)", "percentage": 92, "category": "AI"},
        {"name": "Seaborn", "percentage": 85, "category": "AI"},
        {"name": "Matplotlib", "percentage": 85, "category": "AI"},
        {"name": "Data Visualization (Matplotlib, Seaborn)", "percentage": 85, "category": "AI"},
        {"name": "LiveKit & WebRTC", "percentage": 85, "category": "AI"},

        # Soft / Infrastructure
        {"name": "Docker", "percentage": 88, "category": "SOFT"},
        {"name": "PostgreSQL", "percentage": 90, "category": "SOFT"},
        {"name": "MySQL", "percentage": 85, "category": "SOFT"},
        {"name": "MongoDB", "percentage": 85, "category": "SOFT"},
        {"name": "AWS (S3, EC2)", "percentage": 82, "category": "SOFT"},
        {"name": "Nginx, SSL, DNS", "percentage": 85, "category": "SOFT"},
        {"name": "GitHub Actions (CI/CD)", "percentage": 80, "category": "SOFT"},
        {"name": "SIP Trunking", "percentage": 80, "category": "SOFT"},
        {"name": "Problem Solving", "percentage": 90, "category": "SOFT"},
        {"name": "Team Collaboration", "percentage": 85, "category": "SOFT"},
        {"name": "Communication", "percentage": 80, "category": "SOFT"},
        {"name": "Debugging Skills", "percentage": 95, "category": "SOFT"},
    ]

    for item in skills_list:
        obj, created = Skill.objects.get_or_create(
            name=item['name'],
            defaults={'percentage': item['percentage'], 'category': item['category']}
        )
        if created:
            print(f" > Added new skill: {item['name']}")
        else:
            obj.percentage = item['percentage']
            obj.category = item['category']
            obj.save()
            print(f" > Merged existing skill: {item['name']}")

    # --- 4. EXPERIENCE (MERGE) ---
    print("Merging Experience...")
    # 1. Karoza Tech (Internship)
    Experience.objects.get_or_create(
        company_name="Karoza Tech",
        role="AI/ML Intern",
        defaults={
            "start_date": datetime.date(2025, 6, 1),
            "end_date": None,
            "description": "Worked on various projects that helped hone my skills in AI/ML, contributing to key development milestones."
        }
    )
    print(" > Maintained Experience: Karoza Tech")

    # 2. Amenity Technologies (Present Company)
    Experience.objects.get_or_create(
        company_name="Amenity Technologies",
        role="Python AI/ML Developer",
        defaults={
            "start_date": datetime.date(2024, 1, 1),
            "end_date": None,
            "description": (
                "AI & Machine Learning Developer with 1+ years of experience building intelligent, "
                "scalable applications powered by LLMs, RAG pipelines, multi-agent voice systems, and computer vision models. "
                "Strong expertise in Python backend development using FastAPI, Django, and Flask, with practical experience "
                "integrating AI systems into production-ready applications."
            )
        }
    )
    print(" > Added/Maintained Experience: Amenity Technologies")

    # --- 5. PROJECTS (MERGE) ---
    print("Merging Projects...")
    projects_list = [
        {
            "title": "Multi-Agent Voice Bot (Plugin & Play Architecture)",
            "description": (
                "Built a production-grade, domain-agnostic voice AI platform using LiveKit Agents SDK with a modular plugin-based multi-agent architecture. "
                "Designed a core framework that decouples orchestration, provider management, and persistence from domain-specific logic, enabling the addition of new domains (healthcare, banking, etc.) without modifying core code. "
                "Implemented specialized agents for different conversation stages with seamless tool-based handoffs and context preservation. "
                "Integrated multilingual support with dynamic language detection and real-time TTS switching (Hindi, English, Gujarati) alongside silence detection and interruption handling. "
                "Engineered backend using Django/PostgreSQL with Deepgram (STT), Cartesia (TTS), Gemini/OpenAI/Claude (LLMs), Silero VAD, AWS S3, WebRTC, SIP Trunking, and Docker on VPS."
            ),
            "tech_stack": "LiveKit Agents SDK, Python, Django, PostgreSQL, Docker, WebRTC, SIP Trunking, Deepgram, Cartesia, Gemini, AWS S3",
            "github_link": "https://github.com/Kuldeep-Tapodhan"
        },
        {
            "title": "Regional Health Assistance Chatbot",
            "description": (
                "Built a comprehensive AI-powered multilingual healthcare platform providing health consultations, medical report analysis, and hospital search capabilities. "
                "Developed a Retrieval-Augmented Generation (RAG) pipeline using 127+ curated health documents, ChromaDB vector storage, and 384-dimensional embeddings. "
                "Fine-tuned BioMistral-7B model on Lightning AI platform using 3 medical domain datasets (MedQuAD, HealthcareMagic, iCliniq). "
                "Implemented multi-agent routing for intent classification, OCR-based medical report analysis (Tesseract), Hospital Finder (Haversine distance, Google Places API), OTP authentication, and multilingual translation/TTS with FastAPI and Next.js."
            ),
            "tech_stack": "FastAPI, BioMistral-7B, RAG, LangChain, ChromaDB, Vector Embeddings, Tesseract OCR, Next.js, Appwrite",
            "github_link": "https://github.com/Kuldeep-Tapodhan"
        },
        {
            "title": "Plantify – Plant Disease Detection System (Phase 1)",
            "description": (
                "Developed an AI-powered plant disease detection system using Deep Learning and Computer Vision to classify plant leaf diseases from images. "
                "Trained CNN models using TensorFlow/Keras on structured plant disease datasets. "
                "Performed extensive image preprocessing, data augmentation, and class balancing to improve model generalization. "
                "Optimized hyperparameters and converted the model to TensorFlow Lite (TFLite) format for lightweight on-device inference."
            ),
            "tech_stack": "Python, TensorFlow, Keras, OpenCV, CNN, TensorFlow Lite, Deep Learning",
            "github_link": "https://github.com/Kuldeep-Tapodhan"
        },
        {
            "title": "Plantify – Plant Disease Detection App (Phase 2)",
            "description": (
                "Developed a full-stack Android mobile application (Kotlin) integrating the TFLite model from Phase 1 for real-time plant disease detection. "
                "Implemented image capture via Camera/Gallery, preprocessing, and real-time predictions with confidence scoring. "
                "Designed a modular architecture separating UI, Data, and ML layers. "
                "Integrated backend services including Firebase Authentication, Firebase Realtime Database for scan history, Storage, OpenWeather API (Retrofit), and multi-language support (English, Hindi, Gujarati, French)."
            ),
            "tech_stack": "Android (Kotlin), TensorFlow Lite, Firebase (Auth, Realtime DB, Storage), Retrofit API, Mobile ML",
            "github_link": "https://github.com/Kuldeep-Tapodhan"
        },
        {
            "title": "Bollywood Song Recommendation System",
            "description": (
                "Built a machine learning-based recommendation platform that suggests Bollywood songs using K-Nearest Neighbors (KNN) and cosine similarity. "
                "Performed feature engineering on audio attributes (tempo, energy, genre) to create an optimized feature matrix. "
                "Precomputed and serialized data using Pickle to enable fast, real-time recommendations. "
                "Developed and deployed a full-stack web application using Flask, with dynamic search, filtering, hosted on Render using Gunicorn."
            ),
            "tech_stack": "Machine Learning, KNN, Scikit-learn, Flask, Pandas, NumPy, Pickle, Render, Gunicorn",
            "github_link": "https://github.com/Kuldeep-Tapodhan/Bollywood-Song-Recommedation"
        },
        {
            "title": "Disease Prediction and Drug Recommendation Platform",
            "description": (
                "Built a web-based machine learning system that predicts diseases based on user-entered symptoms and recommends appropriate medications and treatments. "
                "Developed a Random Forest multi-class classification model using medical symptom datasets. "
                "Integrated Gemini API to dynamically generate detailed disease explanations (causes, precautions, advice). "
                "Designed and implemented full backend using Flask with responsive HTML/CSS/JavaScript frontend."
            ),
            "tech_stack": "Machine Learning, Random Forest, Scikit-learn, Flask, Gemini API, HTML/CSS/JS",
            "github_link": "https://github.com/Kuldeep-Tapodhan/Disease-prediction-and-drug-recommendation/"
        },
        {
            "title": "Dynamic Choice To-Do Management System",
            "description": (
                "Built a full-stack task management system with dynamic category selection and role-based access control. "
                "Developed backend APIs using Django and Django REST Framework (DRF) with PostgreSQL for structured data storage. "
                "Implemented JWT-based authentication, user-specific task isolation, priority tagging, and status tracking features. Deployed on Render."
            ),
            "tech_stack": "Django, Django REST Framework (DRF), PostgreSQL, JWT Authentication, REST API, Render",
            "github_link": "https://github.com/Kuldeep-Tapodhan"
        },
        {
            "title": "College Fest Event Management System",
            "description": (
                "Built a dynamic role-based web application to manage college fest events using JSP, Java (JDBC), and MySQL, following a 3-tier architecture. "
                "Designed separate modules for Admin and Participants, enabling secure authentication, event creation, seat management, real-time tracking, and transaction handling with PreparedStatements for SQL Injection prevention."
            ),
            "tech_stack": "Java, JSP, JDBC, MySQL, 3-Tier Architecture, Role-Based Auth",
            "github_link": "https://github.com/Kuldeep-Tapodhan"
        }
    ]

    for proj in projects_list:
        p, created = Project.objects.get_or_create(
            title=proj['title'],
            defaults={
                "description": proj['description'],
                "tech_stack": proj['tech_stack'],
                "github_link": proj['github_link']
            }
        )
        if created:
            print(f" > Added project: {p.title}")
        else:
            p.description = proj['description']
            p.tech_stack = proj['tech_stack']
            p.github_link = proj['github_link']
            p.save()
            print(f" > Updated/Merged project: {p.title}")

    # --- 6. CERTIFICATIONS (MERGE) ---
    print("Merging Certifications...")
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
            print(f" > Added certification: {cert_title}")

    # --- 7. EDUCATION (MERGE) ---
    print("Merging Education...")
    edu_list = [
        {
            "institution": "Marwadi University, Rajkot",
            "degree": "Bachelor of Technology - Information Technology",
            "start_date": datetime.date(2022, 8, 1),
            "end_date": datetime.date(2026, 5, 31),
            "description": "Graduated with a CGPA of 8.5/10. Specialized in Artificial Intelligence, Machine Learning, Full-Stack Web Development, and Software Engineering."
        },
        {
            "institution": "Adarsh Mahavidhyalay, Gandhidham",
            "degree": "Higher Secondary Certificate (HSC)",
            "start_date": datetime.date(2019, 6, 1),
            "end_date": datetime.date(2021, 5, 31),
            "description": "Completed high school with a focus on science and mathematics."
        }
    ]

    for edu in edu_list:
        e, created = Education.objects.get_or_create(
            degree=edu['degree'],
            defaults={
                "institution": edu['institution'],
                "start_date": edu['start_date'],
                "end_date": edu['end_date'],
                "description": edu['description']
            }
        )
        if created:
            print(f" > Added education: {e.degree}")
        else:
            e.institution = edu['institution']
            e.start_date = edu['start_date']
            e.end_date = edu['end_date']
            e.description = edu['description']
            e.save()
            print(f" > Merged education: {e.degree}")

    print("-----------------------------------")
    print("Data merged successfully without deleting existing database records!")
    print("-----------------------------------")

if __name__ == '__main__':
    load_data()

from django.shortcuts import render
from .models import Skill, Project

def home(request):
    skills = Skill.objects.all()
    projects = Project.objects.all()
    return render(request, "personal_site/home.html", {
        "skills": skills,
        "projects": projects,
    })

def experience(request):
    return render(request, "personal_site/experience.html")

def contact(request):
    return render(request, "personal_site/contact.html")

def projects(request):
    project_data = [
        {
            'title': 'Interactive Resume Platform',
            'category': 'webapps',
            'tags': ['Django', 'Python', 'Bootstrap 5', 'PostgreSQL', 'JavaScript'],
            'description': 'You are looking at it. A highly responsive digital resume application utilizing client-side filtering engines and custom metric dashboards. Built with Django, Bootstrap, and a sprinkle of JavaScript magic.',
            'live_url': '/', 
            'featured': True  
        },
        {
            'title': 'NBA Player Performance Visualizer',
            'category': 'webapps',
            'tags': ['Django', 'Python', 'Chart.js', 'NBA API'],
            'description': 'An interactive tracking engine translating raw positional basketball metrics and game histories into real-time SVG court mappings.',
            'live_url': '/nba_player_dashboard/',
            'featured': True
        }

    ]

    return render(request, 'personal_site/projects.html', {'projects': project_data})
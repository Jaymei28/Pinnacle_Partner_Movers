import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobstream_backend.settings')
django.setup()

from jobs.models import Job

def seed_jobs():
    jobs = [
        {
            'title': 'Senior Frontend Developer',
            'company': 'TechFlow Systems',
            'location': 'San Francisco, CA',
            'zip_code': '94105',
            'description': 'We are looking for a React expert to lead our dashboard team.',
            'job_type': 'full-time',
            'salary': '$140k - $180k',
            'requirements': '5+ years React experience, TypeScript, TailwindCSS.',
            'apply_link': 'https://example.com/apply/1'
        },
        {
            'title': 'Product Designer',
            'company': 'CreativeBox',
            'location': 'Remote / NYC',
            'zip_code': '10001',
            'description': 'Join our design studio to create beautiful user experiences.',
            'job_type': 'contract',
            'salary': '$80/hr - $110/hr',
            'requirements': 'Strong portfolio, Figma mastery, UI/UX principles.',
            'apply_link': 'https://example.com/apply/2'
        },
        {
            'title': 'Backend Engineer (Django)',
            'company': 'DataStream',
            'location': 'Austin, TX',
            'zip_code': '78701',
            'description': 'Scale our data pipelines using Python and Django.',
            'job_type': 'full-time',
            'salary': '$130k - $160k',
            'requirements': 'Python, Django, PostgreSQL, Docker.',
            'apply_link': 'https://example.com/apply/3'
        }
    ]

    for job_data in jobs:
        Job.objects.get_or_create(**job_data)
        print(f"Created/Verified job: {job_data['title']} at {job_data['company']}")

if __name__ == '__main__':
    seed_jobs()

import os
import subprocess

def install_requirements():
    """Install all required packages from requirements.txt"""
    print(" Installing required packages...")
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    print(" Installation complete!")

def setup_django():
    """Apply migrations and run basic setup"""
    print("⚙️ Applying migrations...")
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    print(" Migrations applied successfully!")

    print("👤 Creating superuser (optional)...")
    os.system('python manage.py createsuperuser')

    print("🚀 Starting development server...")
    os.system('python manage.py runserver')

if __name__ == "__main__":
    install_requirements()
    setup_django()

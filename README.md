# samasta-news-portal
# Create project directory
mkdir samasta-news-portal
cd samasta-news-portal

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install Django
pip install django

# Start project
django-admin startproject samasta_portal
cd samasta_portal

# Create apps
python manage.py startapp news
python manage.py startapp accounts

python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

python manage.py runserver

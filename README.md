# ToadCraft
portfolio website for toadcraft designs.

This project uses django tailwind.

Before running the project remember to install these packages

run
  -python -m venv tcenv
  -pip install django
  -pip install pillow
  -pip install django-tailwind
  -pip install django-browser-reload



edit the settings.py file in toadcraft directory.
  -remove "theme" from INSTALLED_APPS


run inside environment.
  -python manage.py tailwind init
  add "theme" back to INSTALLED_APPS
  -python manage.py tailwind install
  -python manage.py tailwind start
  python manage.py runserver

  

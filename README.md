# Django Blog App

A simple blog application built with Django that features user registration, blog post management, and profile management with Cloudinary image storage and Amazon SES email notifications.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Activate the Virtual Environment](#3-activate-the-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Set Up the Database](#5-set-up-the-database)
  - [6. Configure Cloudinary](#6-configure-cloudinary)
  - [7. Configure Amazon SES for Email Notifications](#7-configure-amazon-ses-for-email-notifications)
  - [8. Create a Superuser](#8-create-a-superuser)
  - [9. Run the Server](#9-run-the-server)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- User Authentication (Registration, Login, Logout, Password Reset)
- Blog Post Management (Create, Update, Delete)
- Profile Management with Cloudinary image hosting
- Email notifications via Amazon SES
- Responsive UI built with Bootstrap

## Technologies Used

- Django
- SQLite (for development)
- Cloudinary
- Amazon SES
- Bootstrap

## Installation

1. Clone the Repository
git clone https://github.com/your-username/django-blog-app.git
cd django-blog-app

2. Create a Virtual Environment
python -m venv venv

3. Activate the Virtual Environment
Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

5. Set Up the Database
python manage.py migrate

6. Configure Cloudinary
Sign up for a Cloudinary account.

Obtain your cloud_name, api_key, and api_secret from the Cloudinary dashboard.

Add the following to your settings.py:

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your-cloud-name',
    'API_KEY': 'your-api-key',
    'API_SECRET': 'your-api-secret'}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

7. Configure Amazon SES for Email Notifications
Set up an Amazon SES account.
Obtain your SES SMTP credentials.
Add the following to your settings.py:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-smtp-user'
EMAIL_HOST_PASSWORD = 'your-smtp-password'

8. Create a Superuser
python manage.py createsuperuser
Follow the prompts to create your admin account.

9. Run the Server
python manage.py runserver
Your application is now accessible at http://127.0.0.1:8000/.

<!-- Usage
User Registration: Users can register with a username, email, and password.
Login/Logout: Registered users can log in and log out.
Blog Management: Create, update, and delete blog posts.
Profile Management: Update profile information and upload profile pictures (hosted on Cloudinary).
Password Reset: Request password reset emails.
Admin Panel: Manage users and posts via /admin/. -->
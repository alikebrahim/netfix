# NetFix - Home Services Marketplace

A simple Django-based marketplace where companies can offer services and customers can request them.

## Project Overview

NetFix enables:
- Companies to register and create services in their specific field
- Customers to register and request services
- Basic user profiles for both company and customer accounts
- Service browsing by category

## Setup Instructions

### Prerequisites
- Python 3.x
- Basic Django knowledge

### Installation

1. Clone the repository:
```bash
git clone [repository URL]
cd netfix
```

2. Set up virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Collect static files:
```bash
python manage.py collectstatic
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

- **main**: Basic pages and navigation
- **users**: Simple user management (registration, login, profiles)
- **services**: Service creation, listing, and request handling

## Usage

- Register as a company or customer at /users/register/
- Login at /users/login/
- Browse services at /services/
- Companies can create services at /services/create/
- View your profile at /company/[username] or /customer/[username]

## Development Notes

This project is built with Django 3.1.14 and focuses on simplicity and ease of maintenance.
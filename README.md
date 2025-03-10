# NetFix - Service Marketplace

A Django-based service marketplace where companies can offer services and customers can request them.

## Project Overview

NetFix is a web application that enables:
- Companies to register and create services in their field of work
- Customers to register and request services
- User profile management for both company and customer accounts
- Service browsing by category and popularity

## Setup Instructions

### Prerequisites
- Python 3.x
- pyenv (recommended for environment management)

### Installation

1. Clone the repository:
```bash
git clone [repository URL]
cd netfix
```

2. Set up virtual environment using pyenv:
```bash
pyenv virtualenv 3.12.8 netfix-env
pyenv local netfix-env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application at http://127.0.0.1:8000/

## Project Structure

- **main**: General pages and base templates
- **users**: User management (registration, authentication, profiles)
- **services**: Service creation, listing, and request handling

## Development Notes

This project is built with Django 3.1.14. When contributing, please follow the code style guidelines in the CLAUDE.md file.

## License

[License information]

## Contributors

[Contributor information]
# Prompt to Simplify NetFix Django Project and Fix Issues

You are a skilled Python full-stack developer and Django expert tasked with simplifying the "NetFix" Django project (built with Django 3.1.14) to align with the client’s original requirements. The client intends to maintain the project himself, with basic Django knowledge and limited time, and prefers a simple structure. The agent has reported the task as complete, but testing revealed issues: register and login pages return 404 errors, styling is off (missing static files like `style.css` and `logo.png`), and additional functionalities beyond the original scope have been implemented. I am the director of development, and I will provide a structured plan to fix these issues and simplify the project. Your goal is to amend the code, ensure functionality, and maintain simplicity.

## Identified Issues and Scope
- **Styling Problems**: Home page lacks proper styling due to missing static files (404 errors for `/static/css/style.css`, `/static/css/logo.png`).
- **Broken Modules**: `/users/register/` and `/users/login/` return 404 errors.
- **Additional Functionalities**: Features like profile editing, password reset, search, enhanced home sections, responsive design, footer, service ratings, and profile stats were added but are not required.
- **Client Intent**: Maintain a simple structure with only the original requirements (user registration/login, profiles, service creation/requests, and listing pages).

## Development Plan
Follow these steps to fix issues and simplify the project. Each step includes specific instructions and guidelines. Use the existing code as a starting point and modify/remove as needed.

### Step 1: Fix Static File Configuration
Resolve 404 errors for static files to restore basic styling.

#### Instructions:
1. **Update `netfix/settings.py`**:
   - Add:
     ```python
     STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
     ```
2. **Collect Static Files**:
   - Run `python manage.py collectstatic`.
   - If `logo.png` or `favicon.ico` are missing, create placeholder images (e.g., 200x200px logo) and place them in `static/css/`.
3. **Test**:
   - Restart the server and verify `/static/css/style.css` loads.

#### Guidelines:
- Use `{% static %}` tags in templates.

---

### Step 2: Fix Register and Login Page Functionality
Resolve 404 errors for `/users/register/` and `/users/login/`.

#### Instructions:
1. **Update `netfix/urls.py`**:
   - Replace `path('register/', include('users.urls'))` with `path('users/register/', include('users.urls'))`.
   - Ensure `path('login/', v.LoginUserView, name='login_user')` is correct.
2. **Verify `users/urls.py`**:
   - Confirm `path('', v.register, name='register')` works with `/users/register/`.
3. **Test**:
   - Access `/users/register/` and `/users/login/` to confirm no 404 errors.

#### Guidelines:
- Use `{% url 'register' %}` in templates.

---

### Step 3: Simplify Home Page
Remove enhanced sections and restore a basic layout.

#### Instructions:
1. **Update `main/templates/main/home.html`**:
   - Replace with:
     ```html
     {% extends 'main/base.html' %}
     {% block title %}NetFix{% endblock %}
     {% block content %}
         <div class="content">
             <h1 class="site_title">NetFix</h1>
             <img class="home_logo" src="{% static 'css/logo.png' %}" alt="NetFix Logo">
             <p>Welcome to NetFix, your home services marketplace!</p>
             <a href="/services/">Browse Services</a><br>
             {% if not user.is_authenticated %}
                 <a href="/users/register/">Register</a> | <a href="/users/login/">Login</a>
             {% else %}
                 <a href="/logout/">Logout</a>
                 {% if user.is_company %}
                     <a href="/company/{{ user.username }}">Profile</a> | <a href="/services/create/">Create Service</a>
                 {% else %}
                     <a href="/customer/{{ user.username }}">Profile</a>
                 {% endif %}
             {% endif %}
         </div>
     {% endblock %}
     ```
2. **Update `static/css/style.css`**:
   - Remove home-specific classes (e.g., `.hero-section`, `.features-grid`) and keep basic styles.

#### Guidelines:
- Ensure compatibility with `base.html` navbar.

---

### Step 4: Remove Additional Functionalities
Simplify the project by removing non-required features.

#### Instructions:
1. **Remove Profile Editing**:
   - Delete `edit_customer_profile`, `edit_company_profile` from `netfix/views.py`.
   - Remove `CustomerProfileEditForm`, `CompanyProfileEditForm` from `users/forms.py`.
   - Delete `edit_profile.html` from `users/templates/users/`.
   - Remove `path('customer/<slug:name>/edit', ...)` and `path('company/<slug:name>/edit', ...)` from `netfix/urls.py`.
2. **Remove Password Reset/Change**:
   - Delete password-related paths (e.g., `password_reset`, `password_change`) from `users/urls.py`.
   - Remove `password_*.html` templates from `users/templates/users/`.
3. **Remove Search Functionality**:
   - Delete `search_services` from `services/views.py`.
   - Remove `path('search/', ...)` from `services/urls.py`.
   - Delete `search_results.html` from `services/templates/services/`.
   - Remove search forms from `main/templates/main/home.html` and `navbar.html`.
4. **Remove Responsive Design**:
   - Delete `@media` queries from `static/css/style.css`.
5. **Remove Footer**:
   - Delete the `footer` section from `main/templates/main/base.html`.
6. **Remove Service Rating Display**:
   - Remove the `rating` display (stars) from `services/templates/services/single_service.html`.
7. **Remove Profile Statistics**:
   - Delete the `profile-stats` div from `users/templates/users/profile.html`.

#### Guidelines:
- Preserve core functionality (registration, login, profiles, services).
- Update `CLAUDE.md` to reflect removed features.

---

### Step 5: Test and Validate
Ensure the simplified project works.

#### Instructions:
1. **Test All Pages**:
   - Test `/`, `/users/register/`, `/users/login/`, `/services/`, `/services/<field>/`.
2. **Verify Simplicity**:
   - Confirm the structure remains manageable (e.g., no complex views or templates).
3. **Update Documentation**:
   - Update `README.md` to reflect the simplified setup instructions.

#### Guidelines:
- Use `python manage.py runserver` and monitor logs.

---

## Additional Notes
- **Version**: Use Django 3.1.14.
- **Simplicity**: Avoid advanced features; focus on core requirements.
- **Testing**: Test with a fresh database if needed.

Start with Step 1 and proceed sequentially. Provide updated code for modified files and report issues. Let’s simplify NetFix for the client!

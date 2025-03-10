# Development Prompt for Completing the NetFix Django Project

You are a skilled Python full-stack developer and Django expert tasked with completing a partially built Django project called "NetFix." This is a service marketplace where **companies** can create services and **customers** can request them. The project uses **Django 3.1.14**, and your task is to implement the missing features based on the client’s requirements and the current project state. I am the director of development, and I will provide you with a structured plan to follow. Your goal is to implement the code, fix errors, and ensure the application runs as expected.

## Project Overview
- **Objective**: Create a website where users (companies and customers) can register, log in, and interact with services. Companies create services, and customers request them.
- **User Types**:
  - **Company**: Can create services tied to their field of work.
  - **Customer**: Can request existing services.
- **Key Features**:
  - User registration and login with email and password.
  - Unique email and username validation.
  - Profile pages showing user info and (for customers) requested services or (for companies) offered services.
  - Service creation (by companies) and service requests (by customers).
  - Pages for displaying all services, services by category, and the most requested services.
- **Current State**: The project has a basic structure with apps (`main`, `services`, `users`), templates, and some implemented views/models, but key functionality is incomplete.

## Project Directory and Files
The project structure and file contents have been provided separately. Key observations:
- **Apps**: `main` (general pages), `services` (service-related logic), `users` (user management).
- **Issues**: 
  - `users/models.py`: `Customer` model is incomplete.
  - `users/views.py`: Login functionality is missing.
  - `services/views.py`: Service creation and request logic are incomplete.
  - Templates and forms need updates to match requirements.

## Development Plan
Follow these steps in order to complete the project. Each step includes specific instructions and guidelines. Use the existing code as a starting point and modify/add as needed.

### Step 1: Fix and Complete the Models
The database models need to be fully defined to support the requirements.

#### Instructions:
1. **Update `users/models.py`**:
   - Complete the `Customer` model:
     - Add `user` (OneToOneField with `User`).
     - Add `birth` (DateField for date of birth).
   - Ensure `User` and `Company` models match requirements (already mostly correct).
   - Add a `ServiceRequest` model in `services/models.py` to track customer requests:
     - Fields: `customer` (ForeignKey to `Customer`), `service` (ForeignKey to `Service`), `address` (CharField), `hours` (DecimalField), `request_date` (DateTimeField, auto_now_add=True), `total_cost` (DecimalField, calculated).
2. **Update `services/models.py`**:
   - Fix `Service.price_hour` max_digits (currently 100, reduce to 7 for practicality).
   - Remove "All in One" from `field` choices (per requirements).
3. **Run Migrations**:
   - After updating models, run:
     ```bash
     python3 manage.py makemigrations
     python3 manage.py migrate
     ```
   - Fix any migration errors by adjusting model fields or adding default values if prompted.

#### Guidelines:
- Use Django’s built-in validators where applicable (e.g., `MinValueValidator` for `hours`).
- Ensure foreign keys use `on_delete=models.CASCADE`.

---

### Step 2: Implement User Registration and Login
User registration and login are partially implemented but need completion.

#### Instructions:
1. **Update `users/forms.py`**:
   - Complete `CustomerSignUpForm`:
     - Fields: `email`, `username`, `password1`, `password2`, `birth` (use `DateInput` widget).
     - Add validation for unique email and username.
   - Complete `CompanySignUpForm`:
     - Fields: `email`, `username`, `password1`, `password2`, `field` (ChoiceField with company field choices).
     - Add validation for unique email and username.
   - Update `UserLoginForm`:
     - Add authentication logic in `clean` method to verify email/password.
2. **Update `users/views.py`**:
   - Complete `LoginUserView`:
     - Use `UserLoginForm` to authenticate and log in users.
     - Redirect to homepage on success.
   - Update `CustomerSignUpView` and `CompanySignUpView`:
     - In `form_valid`, create related `Customer` or `Company` instance after saving `User`.
3. **Update Templates**:
   - `register_customer.html`: Display form with birth field.
   - `register_company.html`: Display form with field dropdown.
   - Add `login.html` in `users/templates/users/` with email/password fields.

#### Guidelines:
- Use Django’s authentication system (`authenticate`, `login`).
- Display form errors if validation fails (e.g., duplicate email).

---

### Step 3: Implement Service Creation
Companies need to create services restricted by their field of work.

#### Instructions:
1. **Update `services/forms.py`**:
   - Update `CreateNewService`:
     - Ensure `field` choices match `Service` model choices.
     - Add validation to restrict field based on company’s field (unless "All in One").
2. **Update `services/views.py`**:
   - Complete `create` view:
     - Check if user is a company.
     - Use `CreateNewService` form, populate field choices dynamically based on user’s company field.
     - Save service with company reference on valid form submission.
3. **Update `services/templates/services/create.html`**:
   - Add form with fields for name, description, price_hour, and field.
   - Include CSRF token and submit button.

#### Guidelines:
- Redirect to service list page after creation.
- Restrict access to authenticated company users only.

---

### Step 4: Implement Service Request
Customers need to request services with address and hours.

#### Instructions:
1. **Update `services/forms.py`**:
   - Complete `RequestServiceForm`:
     - Fields: `address` (CharField), `hours` (DecimalField, min_value=0.5).
2. **Update `services/views.py`**:
   - Complete `request_service` view:
     - Check if user is a customer.
     - Use `RequestServiceForm` to create a `ServiceRequest` instance.
     - Calculate `total_cost` as `service.price_hour * hours`.
     - Save request and redirect to profile.
3. **Update `services/templates/services/request_service.html`**:
   - Display service details and form with address/hours fields.

#### Guidelines:
- Ensure only authenticated customers can request services.
- Save `request_date` automatically.

---

### Step 5: Enhance Profile Pages
Profiles need to display requested services (customers) or offered services (companies).

#### Instructions:
1. **Update `netfix/views.py`**:
   - Update `customer_profile`:
     - Fetch `Customer` and their `ServiceRequest` objects.
     - Pass to `profile.html`.
2. **Update `users/templates/users/profile.html`**:
   - Fix customer section to loop through `ServiceRequest` objects (not `sh`).
   - Ensure company section works with existing `services` context.

#### Guidelines:
- Use conditional logic to differentiate customer vs. company profiles.
- Link service names to their detail pages.

---

### Step 6: Implement Service Listing Pages
Add pages for all services and most requested services.

#### Instructions:
1. **Update `services/views.py`**:
   - Update `service_list`:
     - Pass all services to `list.html`.
   - Add `most_requested` view:
     - Query `ServiceRequest` to count requests per service, order by count.
     - Render in new `most_requested.html`.
2. **Update `services/urls.py`**:
   - Add path for `most_requested` (e.g., `path('most-requested/', v.most_requested, name='most_requested')`).
3. **Create `services/templates/services/most_requested.html`**:
   - Extend `base.html`, list services with request counts.

#### Guidelines:
- Use Django’s `annotate` and `Count` for most requested services.
- Ensure `field.html` works for category filtering (already implemented).

---

### Step 7: Final Touches and Testing
Ensure everything works and polish the project.

#### Instructions:
1. **Update `netfix/settings.py`**:
   - Add `STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]` if static files fail to load.
2. **Test the Application**:
   - Run `python3 manage.py runserver`.
   - Test registration, login, service creation, and requests for both user types.
   - Verify profile pages and service listings.
3. **CSS Adjustments**:
   - Tweak `style.css` if needed for better visuals (optional).

#### Guidelines:
- Handle edge cases (e.g., unauthenticated access).
- Ensure migrations apply cleanly.

---

## Additional Notes
- **Version**: Stick to Django 3.1.14 conventions (e.g., `url` instead of `re_path` where possible).
- **Security**: Keep `DEBUG = True` for development, but note it should be `False` in production.
- **Templates**: Use Django template syntax (`{% %}`) consistently.
- **Existing Code**: Build on what’s provided, only rewriting if necessary.

Start with Step 1 and proceed sequentially. Provide the updated code for each step as you complete it, and report any issues or questions. Let’s build a fully functional NetFix!

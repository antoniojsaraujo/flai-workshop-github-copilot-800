---
description: 'Diagnose and fix GitHub Actions validation issues for any workshop step'
model: Claude Sonnet 4.5 (copilot)
---

# Workshop Step Troubleshooter

This prompt helps diagnose and fix issues when a workshop step fails GitHub Actions validation.

## Usage

When using this prompt, **you must specify the step number** you're having trouble with:
- `/fix-step 2` - Fix Step 2 (Application Initial Setup)
- `/fix-step 3` - Fix Step 3 (Django Project Setup)
- `/fix-step 4` - Fix Step 4 (Django REST Framework)
- `/fix-step 5` - Fix Step 5 (React Frontend Setup)

## Your Task

Based on the step number provided by the user, perform the following:

### Step 2: Application Initial Setup
**What GitHub Actions checks for:**
- File: `octofit-tracker/backend/requirements.txt` exists
- Content: Must contain `Django==4.1` (case-insensitive, minimum 1 occurrence)

**Diagnostic steps:**
1. Check if `octofit-tracker/backend/requirements.txt` exists
2. Verify it contains the exact string `Django==4.1`
3. Check if the file has been committed and pushed to the `build-octofit-app` branch

**Common fixes:**
- Create the file if missing in the correct location
- Add `Django==4.1` to requirements.txt if not present
- Ensure the Python virtual environment structure exists:
  - `octofit-tracker/backend/` directory
  - `octofit-tracker/frontend/` directory
- Verify requirements.txt includes all necessary packages:
  - Django==4.1
  - djongo
  - pymongo
  - djangorestframework
  - django-cors-headers

**Self-healing actions:**
- Read the instruction file: `.github/instructions/octofit_tracker_setup_project.instructions.md`
- Create or update requirements.txt with proper dependencies
- Commit and push changes to `build-octofit-app` branch

---

### Step 3: Django Project Setup and Database
**What GitHub Actions checks for:**
- File: `octofit-tracker/backend/octofit_tracker/settings.py` exists
  - Must contain `octofit_db` (case-insensitive, minimum 1 occurrence)
  - Must contain `djongo` (case-insensitive, minimum 2 occurrences)
- File: `octofit-tracker/backend/octofit_tracker/management/commands/populate_db.py` exists
  - Must contain `Populate the octofit_db database with test data` (exact string)

**Diagnostic steps:**
1. Verify Django project `octofit_tracker` was created in `octofit-tracker/backend/`
2. Check if `settings.py` has MongoDB configuration with djongo
3. Verify `populate_db.py` management command exists
4. Confirm the database name is `octofit_db` in settings
5. Check if all files are committed to `build-octofit-app` branch

**Common fixes:**
- Ensure Django project was created with: `django-admin startproject octofit_tracker` in the backend directory
- Update `settings.py` DATABASES configuration:
  - ENGINE: 'djongo'
  - NAME: 'octofit_db'
  - ENFORCE_SCHEMA: False
  - CLIENT settings with host and port
- Add to INSTALLED_APPS: `'octofit_tracker'`, `'rest_framework'`, `'djongo'`
- Enable CORS: Add `'corsheaders'` to INSTALLED_APPS
- Create management command structure: `octofit-tracker/backend/octofit_tracker/management/commands/`
- Create `populate_db.py` with:
  - Help text: `'Populate the octofit_db database with test data'`
  - Collections: users, teams, activities, leaderboard, workouts
  - Sample data with superhero themes (Team Marvel, Team DC)

**Self-healing actions:**
- Read instruction files:
  - `.github/instructions/octofit_tracker_setup_project.instructions.md`
  - `.github/instructions/octofit_tracker_django_backend.instructions.md`
- Create missing directories and files
- Update settings.py with proper MongoDB configuration
- Create and populate the database management command
- Ensure models.py, serializers.py, views.py, urls.py are properly configured
- Run migrations: `python manage.py makemigrations` and `python manage.py migrate`
- Commit all changes to `build-octofit-app` branch

---

### Step 4: Django REST Framework Setup
**What GitHub Actions checks for:**
- File: `octofit-tracker/backend/octofit_tracker/settings.py` exists
  - Must contain `-8000.app.github.dev` (case-insensitive, minimum 1 occurrence)
- File: `octofit-tracker/backend/octofit_tracker/urls.py` exists
  - Must contain `-8000.app.github.dev` (case-insensitive, minimum 1 occurrence)

**Diagnostic steps:**
1. Check if codespace URL is configured in `settings.py` ALLOWED_HOSTS
2. Verify `urls.py` has REST API endpoints with codespace URL format
3. Confirm REST API endpoints are returning correct URLs in api_root
4. Check if both files are committed to `build-octofit-app` branch

**Common fixes:**
- Update `settings.py` ALLOWED_HOSTS to include:
  - The codespace URL pattern: `'*.app.github.dev'`
  - Or specific: `f'{os.environ.get("CODESPACE_NAME")}-8000.app.github.dev'`
  - Also include: `'localhost'`, `'127.0.0.1'`, `'*'`
- Update `urls.py` api_root view to use environment variable:
  - Use `$CODESPACE_NAME` environment variable
  - Format: `https://$CODESPACE_NAME-8000.app.github.dev/api/[endpoint]/`
  - Available endpoints: activities, leaderboard, teams, users, workouts
- Ensure the URL pattern includes the codespace domain format with port 8000
- Do NOT hardcode the CODESPACE_NAME value - use the environment variable
- The key requirement is that both files contain the string `-8000.app.github.dev`

**Self-healing actions:**
- Read instruction file: `.github/instructions/octofit_tracker_django_backend.instructions.md`
- Update ALLOWED_HOSTS in settings.py
- Update api_root return values in urls.py to use codespace URL format
- Ensure views.py is NOT modified (only settings.py and urls.py)
- Test the API endpoints with curl commands
- Commit changes to `build-octofit-app` branch

---

### Step 5: React Frontend Setup
**What GitHub Actions checks for:**
Five React component files must each contain `-8000.app.github.dev/api/[component]/`:
- File: `octofit-tracker/frontend/src/components/Activities.js`
  - Must contain `-8000.app.github.dev/api/activities` (case-insensitive)
- File: `octofit-tracker/frontend/src/components/Leaderboard.js`
  - Must contain `-8000.app.github.dev/api/leaderboard` (case-insensitive)
- File: `octofit-tracker/frontend/src/components/Teams.js`
  - Must contain `-8000.app.github.dev/api/teams` (case-insensitive)
- File: `octofit-tracker/frontend/src/components/Users.js`
  - Must contain `-8000.app.github.dev/api/users` (case-insensitive)
- File: `octofit-tracker/frontend/src/components/Workouts.js`
  - Must contain `-8000.app.github.dev/api/workouts` (case-insensitive)

**Diagnostic steps:**
1. Verify React app was created in `octofit-tracker/frontend/` directory
2. Check if all 5 component files exist in `src/components/`
3. Verify each component has fetch() calls to the correct API endpoint
4. Confirm the codespace URL format is used with the correct component path
5. Check if all files are committed to `build-octofit-app` branch

**Common fixes:**
- Ensure React app structure exists in `octofit-tracker/frontend/`
- Create missing component files in `src/components/` directory
- Update each component's fetch URL to use environment variable format:
  - Format: `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/[component]/`
  - Use the environment variable `REACT_APP_CODESPACE_NAME`, not hardcoded values
  - Each component must point to its specific endpoint (activities, leaderboard, teams, users, workouts)
- Ensure components handle both paginated (.results) and plain array responses
- Add console.log statements to debug API calls
- Install required packages: react, bootstrap, react-router-dom
- Import bootstrap CSS in src/index.js
- Update App.js to include navigation for all components
- The key requirement is that each file contains the string pattern `-8000.app.github.dev/api/[componentname]`

**Self-healing actions:**
- Read instruction file: `.github/instructions/octofit_tracker_react_frontend.instructions.md`
- Create React app if missing (using npx create-react-app with --prefix)
- Create missing component files with proper structure
- Update all fetch() calls to use codespace URL environment variable
- Ensure proper error handling and data display in each component
- Configure react-router-dom for navigation
- Update App.js with navigation menu
- Style components with Bootstrap tables, buttons, cards
- Commit all changes to `build-octofit-app` branch

---

## Execution Process

1. **Identify the step** from the user's input (must be 2, 3, 4, or 5)
2. **Read the relevant workflow file** from `.github/workflows/[step-number]-*.yml` to understand exact validation criteria
3. **Check all required files** against the validation criteria
4. **Diagnose the issue** by comparing what exists vs. what's expected
5. **Apply fixes** based on the common fixes and self-healing actions for that step
6. **Verify the fix** by re-checking files against validation criteria
7. **Commit and push** changes to the `build-octofit-app` branch if fixes were applied
8. **Report back** with:
   - What was wrong
   - What was fixed
   - Current validation status
   - Next steps for the user

## Important Notes

- Always activate the Python virtual environment before running Django commands: `source octofit-tracker/backend/venv/bin/activate`
- All changes must be committed to the `build-octofit-app` branch, not main
- Don't start the Django/React apps automatically - let the user use VS Code's launch.json
- When reading instruction files, follow them carefully as they provide the correct implementation details
- Use environment variables (CODESPACE_NAME, REACT_APP_CODESPACE_NAME) instead of hardcoding URLs
- MongoDB should be configured with no authentication for local development
- If a step depends on previous steps, verify prerequisites are in place

## Error Messages to Watch For

- `FileNotFoundError` - File doesn't exist in expected location
- `KeyError: 'CODESPACE_NAME'` - Environment variable not set
- `ModuleNotFoundError` - Python package not installed
- `Migration errors` - Database migrations not run
- `CORS errors` - CORS middleware not configured
- `404 errors` - API endpoints not properly configured
- `Connection refused` - MongoDB service not running or backend not started

## Success Criteria

After running this prompt, the GitHub Actions workflow for the specified step should pass all validation checks. If it doesn't, iterate and fix remaining issues until all checks pass.

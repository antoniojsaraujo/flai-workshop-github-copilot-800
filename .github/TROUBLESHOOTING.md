# Workshop Troubleshooting Guide

## Quick Fix for GitHub Actions Failures

If your GitHub Actions validation is failing for any workshop step, use the troubleshooting prompt to automatically diagnose and fix the issue.

### How to Use

1. **Open GitHub Copilot Chat** in VS Code
2. **Select "Agent" mode** from the dropdown (not "Ask" or "Edit")
3. **Run the fix command** with your step number:

```prompt
/fix-step 2
```

Replace `2` with the step number you're stuck on (2, 3, 4, or 5).

### Available Commands

- `/fix-step 2` - Fix Step 2: Application Initial Setup (requirements.txt)
- `/fix-step 3` - Fix Step 3: Django Project Setup (settings.py, populate_db.py)
- `/fix-step 4` - Fix Step 4: Django REST Framework (codespace URLs)
- `/fix-step 5` - Fix Step 5: React Frontend (component API endpoints)

### What the Prompt Does

The troubleshooting prompt will automatically:

1. **Diagnose** - Check what files exist and what's missing
2. **Compare** - Verify file contents against GitHub Actions requirements
3. **Fix** - Create or update files to meet validation criteria
4. **Verify** - Confirm all checks will pass
5. **Report** - Tell you what was wrong and what was fixed

### Common Issues by Step

#### Step 2 Issues
- ❌ `requirements.txt` missing or in wrong location
- ❌ `Django==4.1` not in requirements.txt
- ✅ **Fix**: Creates file with all required packages

#### Step 3 Issues
- ❌ Django project not created in correct directory
- ❌ `settings.py` missing MongoDB configuration
- ❌ `populate_db.py` management command doesn't exist
- ✅ **Fix**: Creates Django project, configures MongoDB, adds data population script

#### Step 4 Issues
- ❌ Codespace URL not in `settings.py` ALLOWED_HOSTS
- ❌ API root in `urls.py` not using codespace URL format
- ✅ **Fix**: Updates both files with proper codespace URL configuration

#### Step 5 Issues
- ❌ React components missing API endpoint URLs
- ❌ Components not fetching from `-8000.app.github.dev` domain
- ❌ Wrong endpoint paths in component files
- ✅ **Fix**: Updates all 5 components with correct API URLs

### Example Usage

```
User: /fix-step 3

Copilot Agent Mode:
- Checking Step 3 validation requirements...
- Found issue: settings.py missing 'djongo' configuration
- Found issue: populate_db.py doesn't exist
- Creating management command structure...
- Updating settings.py with MongoDB configuration...
- Creating populate_db.py with test data...
- Verifying fixes against validation criteria...
- ✅ All Step 3 checks will now pass!
- Committing changes to build-octofit-app branch...

Ready to push! Your changes should pass GitHub Actions validation.
```

### Tips

- **Wait for completion** - Agent mode may take a minute to analyze and fix issues
- **Press Continue** - Allow agent mode to execute commands when prompted
- **Keep changes** - Don't cancel or undo files created by the agent
- **Push after fixing** - Remember to push your changes after the fix completes
- **Re-run if needed** - You can run the fix command multiple times

### When to Use This

Use the fix-step prompt when:
- ⚠️ GitHub Actions workflow fails validation
- ⚠️ Mona reports validation errors in the issue comments
- ⚠️ You're not sure what's missing or incorrect
- ⚠️ You want to quickly verify your work meets requirements

### Manual Verification

After running the fix prompt, you can manually verify:

**Step 2:**
```bash
cat octofit-tracker/backend/requirements.txt | grep "Django==4.1"
```

**Step 3:**
```bash
grep -i "octofit_db" octofit-tracker/backend/octofit_tracker/settings.py
grep -i "djongo" octofit-tracker/backend/octofit_tracker/settings.py
cat octofit-tracker/backend/octofit_tracker/management/commands/populate_db.py
```

**Step 4:**
```bash
grep "8000.app.github.dev" octofit-tracker/backend/octofit_tracker/settings.py
grep "8000.app.github.dev" octofit-tracker/backend/octofit_tracker/urls.py
```

**Step 5:**
```bash
grep "8000.app.github.dev/api/activities" octofit-tracker/frontend/src/components/Activities.js
grep "8000.app.github.dev/api/leaderboard" octofit-tracker/frontend/src/components/Leaderboard.js
grep "8000.app.github.dev/api/teams" octofit-tracker/frontend/src/components/Teams.js
grep "8000.app.github.dev/api/users" octofit-tracker/frontend/src/components/Users.js
grep "8000.app.github.dev/api/workouts" octofit-tracker/frontend/src/components/Workouts.js
```

### Still Having Issues?

If the automatic fix doesn't resolve your issue:

1. **Check the branch** - Ensure you're on `build-octofit-app` branch
2. **Verify file paths** - Files must be in exact locations specified
3. **Check for typos** - Validation is case-insensitive but requires exact strings
4. **Review the step instructions** - Re-read the step requirements in `.github/steps/`
5. **Check GitHub Actions logs** - Review the actual error messages in the Actions tab

### Need More Help?

- Review step instructions: `.github/steps/[1-6]-*.md`
- Check instruction files: `.github/instructions/*.md`
- Review other prompts: `.github/prompts/*.prompt.md`
- Ask Copilot: "What did I miss in Step X?"

---

**Remember**: This troubleshooting prompt is designed to save you time by automatically fixing common validation issues. Let agent mode do the heavy lifting!

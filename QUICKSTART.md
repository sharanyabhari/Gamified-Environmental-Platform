# QUICKSTART GUIDE - Gamified Environmental Educational Platform

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher installed
- Windows PowerShell or Command Prompt
- A modern web browser (Chrome, Firefox, Edge, Safari)

---

## Step 1: Install Dependencies (30 seconds)

Open PowerShell and navigate to the project folder:

```powershell
cd "C:\Users\nanda\OneDrive\Desktop\Gamified Environemental Platofrm"
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed flask-2.3.0 flask-cors-4.0.0
```

---

## Step 2: Initialize the Database (10 seconds)

Run the database initialization script:

```powershell
cd backend
python init_db.py
```

**Expected output:**
```
✓ Database initialized successfully at environmental_platform.db
✓ Created tables: Users, Challenges, UserProgress
✓ Inserted sample challenges and users
```

---

## Step 3: Start the Flask Server (10 seconds)

From the backend folder, run:

```powershell
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

✅ **Server is now running!**

---

## Step 4: Open in Browser (10 seconds)

Go to: **http://localhost:5000**

You should see the login page with "🌍 EcoQuest" branding.

---

## 🎮 Test the Platform

### Option 1: Login with Pre-Created Account

Use these test credentials:

| Username | Password | Experience |
|----------|----------|--------------|
| alice_eco | password123 | 450 points, Level 5 ⭐⭐⭐⭐⭐ |
| bob_green | password456 | 320 points, Level 3 ⭐⭐⭐ |
| diana_nature | passwordabc | 510 points, Level 6 🏆 |

**Steps:**
1. Enter username and password
2. Click "Login"
3. You'll see the dashboard with:
   - Your current points and level
   - Progress bar to next level
   - Available challenges
   - Global leaderboard

### Option 2: Create a New Account

1. Click "Register here"
2. Fill in:
   - Username: Your choice
   - Password: At least 6 characters
   - Confirm password
3. Click "Create Account"
4. Login with your new credentials

---

## 📚 Features to Test

### 1. Complete a Challenge
- Click "Challenges" tab
- Browse 12+ environmental challenges
- Click any challenge card to see details
- Click "Complete Challenge"
- 🎉 Watch the success celebration and earn points!
- Your level will update automatically

### 2. Check Your Progress
- **Overview tab**: See current points, level, and recent achievements
- **Progress bar**: Watch it fill as you earn points
- **Level up**: When you reach the next level threshold, you'll see a celebration!

### 3. View the Leaderboard
- Click "Leaderboard" tab
- See top 10 players ranked by total points
- 🥇🥈🥉 Medal indicators for top 3

### 4. Check Your Profile
- Click "Profile" tab
- View detailed stats
- See learning breakdown by category
- Check recent challenge history

---

## 🎯 Challenge Difficulty Levels

| Level | Points | Time to Complete |
|-------|--------|------------------|
| **Easy** 🟢 | 50-65 | 5-10 minutes |
| **Medium** 🟡 | 70-90 | 15-30 minutes |
| **Hard** 🔴 | 100+ | 30+ minutes |

---

## 📊 Level Progression

As you earn points, you level up:

- **Level 1**: 0-99 points
- **Level 2**: 100-249 points
- **Level 3**: 250-499 points
- **Level 4**: 500-749 points
- **Level 5**: 750-999 points
- **Level 6**: 1000+ points

---

## 🛑 Troubleshooting

### Port 5000 Already in Use
If you get "Address already in use":
```powershell
# Kill existing process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or modify port in app.py (change 5000 to 5001)
```

### Database Errors
If database-related errors occur:
```powershell
cd backend
del environmental_platform.db
python init_db.py
```

### Python Not Found
Ensure Python is in your PATH:
```powershell
python --version
```

### CORS or Connection Errors
1. Ensure Flask server is running
2. Clear browser cache (Ctrl+Shift+Delete)
3. Try a different browser
4. Check that JavaScript console shows no errors (F12)

---

## 📁 Project Structure

```
📦 Gamified Environmental Platform
├── 📄 README.md                    # Full documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 QUICKSTART.md               # This file!
│
├── 📁 backend/
│   ├── 📜 app.py                  # Flask application
│   ├── 📜 init_db.py              # Database setup
│   ├── 📁 templates/
│   │   ├── index.html             # Login page
│   │   └── dashboard.html         # Main app interface
│   ├── 📁 static/
│   │   ├── 📁 css/
│   │   │   ├── style.css          # Main styles
│   │   │   └── dashboard.css      # Dashboard styles
│   │   └── 📁 js/
│   │       ├── auth.js            # Login/signup logic
│   │       └── dashboard.js       # App functionality
│   └── 🗄️ environmental_platform.db
│
└── 📁 frontend/
    └── [Source files - reference only]
```

---

## 🔧 Next Steps (Optional)

### Customize Your Platform

**Add New Challenges:**
Edit `backend/init_db.py`, find `sample_challenges` list, and add:
```python
('Challenge Title', 'Description', 'Category', PointsValue, 'Difficulty'),
```

**Change Colors:**
Edit `backend/static/css/style.css`:
```css
:root {
    --primary-color: #2ecc71;      /* Green */
    --secondary-color: #3498db;    /* Blue */
    --accent-color: #f39c12;       /* Yellow */
}
```

**Modify Level Thresholds:**
Edit `calculate_level()` in `backend/app.py`

---

## 📞 Need Help?

1. **Check the README.md** for detailed documentation
2. **Review app.py comments** for API structure
3. **Check browser console** (F12) for JavaScript errors
4. **Check terminal** for Flask server errors

---

## ✨ Key Features

✅ User Authentication (Login/Register)
✅ 12+ Environmental Education Challenges
✅ Gamification (Points, Levels, Badges)
✅ Real-time Leaderboard
✅ User Progress Tracking
✅ Challenge Categories & Difficulty Levels
✅ Responsive Design (Mobile-Friendly)
✅ Smooth Animations & UX
✅ Secure Session Management
✅ Achievement System

---

## 🎉 Ready to Go!

You now have a fully functional gamified environmental learning platform!

**Time to complete this guide:** ~5 minutes
**Time to explore features:** 10-15 minutes
**Time to conquer all challenges:** 2-3 hours

Happy learning! 🌍♻️

---

**Last Updated:** April 2026
**Version:** 1.0

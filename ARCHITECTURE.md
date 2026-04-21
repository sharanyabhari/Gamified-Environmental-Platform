# Architecture & API Documentation

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │   index.html     │  │  dashboard.html  │  │   Static     │  │
│  │   (Login/Reg)    │  │   (Main App)     │  │   Assets     │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                            ↓                                      │
│                    ┌──────────────────────┐                      │
│                    │     JavaScript       │                      │
│                    │  - auth.js (login)   │                      │
│                    │  - dashboard.js      │                      │
│                    │    (interaction)     │                      │
│                    └──────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                             ↓ (HTTP/JSON)
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (Flask)                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Backend Routes (app.py)                     │   │
│  │  • /api/register - POST (create user)                   │   │
│  │  • /api/login - POST (authenticate)                     │   │
│  │  • /api/logout - POST (session end)                     │   │
│  │  • /api/challenges - GET (all challenges)               │   │
│  │  • /api/challenges/<uid> - GET (with status)            │   │
│  │  • /api/complete-challenge - POST (mark complete)       │   │
│  │  • /api/leaderboard - GET (top 10 users)                │   │
│  │  • /api/user/<uid> - GET (profile)                      │   │
│  │  • /api/user/<uid>/stats - GET (detailed stats)         │   │
│  │  • /api/user/<uid>/completed-challenges - GET           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             ↓ (SQL Queries)
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER (SQLite)                       │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │  Users Table  │  │ Challenges   │  │  UserProgress       │  │
│  ├───────────────┤  ├──────────────┤  ├─────────────────────┤  │
│  │ UserID        │  │ ChallengeID  │  │ UserProgressID      │  │
│  │ Username      │  │ Title        │  │ UserID (FK)         │  │
│  │ Password      │  │ Description  │  │ ChallengeID (FK)    │  │
│  │ TotalPoints   │  │ Category     │  │ CompletionDate      │  │
│  │ CurrentLevel  │  │ PointsAwarded│  │ UNIQUE(UserID, CID) │  │
│  │ CreatedDate   │  │ Difficulty   │  └─────────────────────┘  │
│  └───────────────┘  │ CreatedDate  │                            │
│                     └──────────────┘                            │
│                                                                  │
│  File: environmental_platform.db                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### 1. User Registration Flow
```
User Input (HTML Form)
    ↓
auth.js (Frontend Validation)
    ↓
POST /api/register (JSON)
    ↓
app.py (Hash Password)
    ↓
SQLite (INSERT INTO Users)
    ↓
Response (success/error)
    ↓
Redirect to Login
```

### 2. Challenge Completion Flow
```
User Clicks "Complete Challenge"
    ↓
dashboard.js (Modal Popup)
    ↓
User Confirms
    ↓
POST /api/complete-challenge (with challenge_id)
    ↓
app.py:
  • Get challenge points
  • Update UserProgress table
  • Calculate new total points
  • Calculate new level
  • Return results
    ↓
SQLite (INSERT + UPDATE)
    ↓
JavaScript Shows Success Modal
    ↓
Reload Dashboard Data
```

### 3. Leaderboard Update Flow
```
User Clicks "Leaderboard"
    ↓
GET /api/leaderboard
    ↓
app.py (Query & Sort)
    ↓
SQLite (SELECT top 10)
    ↓
Response (JSON array)
    ↓
JavaScript Renders Table
```

---

## 📡 API Endpoints Reference

### Authentication Endpoints

#### POST /api/register
Create a new user account

**Request:**
```json
{
  "username": "john_eco",
  "password": "password123"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user_id": 1
}
```

**Error (400):**
```json
{
  "error": "Username already exists"
}
```

---

#### POST /api/login
Authenticate user and create session

**Request:**
```json
{
  "username": "john_eco",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "user_id": 1,
  "username": "john_eco"
}
```

**Error (401):**
```json
{
  "error": "Invalid username or password"
}
```

---

#### POST /api/logout
Logout current user

**Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

#### GET /api/check-session
Verify if user is logged in

**Response (200) - Logged In:**
```json
{
  "logged_in": true,
  "user_id": 1,
  "username": "john_eco"
}
```

**Response (200) - Not Logged In:**
```json
{
  "logged_in": false
}
```

---

### Challenge Endpoints

#### GET /api/challenges
Get all available challenges

**Response (200):**
```json
[
  {
    "ChallengeID": 1,
    "Title": "Learn About Recycling",
    "Description": "Complete a quiz about proper recycling practices...",
    "Category": "Education",
    "PointsAwarded": 50,
    "Difficulty": "Easy",
    "CreatedDate": "2026-04-01"
  },
  ...
]
```

---

#### GET /api/challenges/<user_id>
Get challenges with completion status for user

**Response (200):**
```json
[
  {
    "ChallengeID": 1,
    "Title": "Learn About Recycling",
    "Description": "...",
    "Category": "Education",
    "PointsAwarded": 50,
    "Difficulty": "Easy",
    "Completed": true    // ← Indicates if user completed it
  },
  {
    "ChallengeID": 2,
    "Title": "Carbon Footprint Calculator",
    "Description": "...",
    "Category": "Assessment",
    "PointsAwarded": 75,
    "Difficulty": "Medium",
    "Completed": false   // ← Not yet completed
  },
  ...
]
```

---

#### POST /api/complete-challenge
Mark a challenge as completed

**Request:**
```json
{
  "challenge_id": 2
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Challenge completed! +75 points",
  "points_awarded": 75,
  "new_total_points": 425,
  "new_level": 3,
  "level_up": true,
  "old_level": 2
}
```

**Error (400):**
```json
{
  "error": "Challenge already completed"
}
```

---

### User Endpoints

#### GET /api/user/<user_id>
Get user profile information

**Response (200):**
```json
{
  "UserID": 1,
  "Username": "john_eco",
  "TotalPoints": 425,
  "CurrentLevel": 3,
  "NextLevelPoints": 500,
  "ProgressToNextLevel": 85.0
}
```

---

#### GET /api/user/<user_id>/stats
Get detailed user statistics

**Response (200):**
```json
{
  "UserID": 1,
  "Username": "john_eco",
  "TotalPoints": 425,
  "CurrentLevel": 3,
  "NextLevelPoints": 500,
  "ChallengesCompleted": 8,
  "CategoryBreakdown": [
    {
      "Category": "Education",
      "count": 3,
      "points": 175
    },
    {
      "Category": "Assessment",
      "count": 2,
      "points": 160
    },
    {
      "Category": "Action",
      "count": 2,
      "points": 80
    },
    {
      "Category": "Lifestyle",
      "count": 1,
      "points": 10
    }
  ]
}
```

---

#### GET /api/user/<user_id>/completed-challenges
Get user's completed challenges

**Response (200):**
```json
[
  {
    "ChallengeID": 1,
    "Title": "Learn About Recycling",
    "Description": "...",
    "PointsAwarded": 50,
    "Category": "Education",
    "Difficulty": "Easy",
    "CompletionDate": "2026-04-05"
  },
  ...
]
```

---

### Leaderboard Endpoint

#### GET /api/leaderboard
Get top 10 users by total points

**Response (200):**
```json
[
  {
    "UserID": 4,
    "Username": "diana_nature",
    "TotalPoints": 510,
    "CurrentLevel": 6,
    "Rank": 1
  },
  {
    "UserID": 1,
    "Username": "alice_eco",
    "TotalPoints": 450,
    "CurrentLevel": 5,
    "Rank": 2
  },
  {
    "UserID": 2,
    "Username": "bob_green",
    "TotalPoints": 320,
    "CurrentLevel": 3,
    "Rank": 3
  },
  ...
]
```

---

## 🗄️ Database Schema Details

### Users Table
```sql
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE NOT NULL,
    Password TEXT NOT NULL,           -- SHA256 hashed
    TotalPoints INTEGER DEFAULT 0,
    CurrentLevel INTEGER DEFAULT 1,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Key Constraints:**
- `Username`: Must be unique
- `TotalPoints`: Updated when challenge is completed
- `CurrentLevel`: Calculated from TotalPoints (see levels.md)

---

### Challenges Table
```sql
CREATE TABLE Challenges (
    ChallengeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Description TEXT NOT NULL,
    Category TEXT DEFAULT 'General',
    PointsAwarded INTEGER NOT NULL,
    Difficulty TEXT DEFAULT 'Easy',  -- 'Easy', 'Medium', 'Hard'
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Categories:**
- Education (learning content)
- Assessment (quizzes/knowledge)
- Action (real-world tasks)
- Lifestyle (behavior change)

**Difficulty Distribution:**
- Easy: 50-65 points
- Medium: 70-90 points
- Hard: 100+ points

---

### UserProgress Table
```sql
CREATE TABLE UserProgress (
    UserProgressID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    ChallengeID INTEGER NOT NULL,
    CompletionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ChallengeID) REFERENCES Challenges(ChallengeID),
    UNIQUE(UserID, ChallengeID)        -- Prevent duplicate completions
);
```

**Key Design:**
- `UNIQUE constraint`: Prevents users from completing same challenge twice
- `CompletionDate`: Tracks when challenge was completed
- Foreign keys ensure referential integrity

---

## 🎯 Gamification Algorithm

### Level Calculation
```python
def calculate_level(total_points):
    if total_points >= 1000:
        return 6
    elif total_points >= 750:
        return 5
    elif total_points >= 500:
        return 4
    elif total_points >= 250:
        return 3
    elif total_points >= 100:
        return 2
    else:
        return 1
```

### Points Table
| Level | Min Points | Max Points | Total to Reach |
|-------|-----------|-----------|-----------------|
| 1 | 0 | 99 | - |
| 2 | 100 | 249 | 100 |
| 3 | 250 | 499 | 250 |
| 4 | 500 | 749 | 500 |
| 5 | 750 | 999 | 750 |
| 6 | 1000+ | ∞ | 1000 |

---

## 🔐 Security Considerations

### Current Implementation
- ✅ Session-based authentication
- ✅ Password hashing (SHA256)
- ✅ UNIQUE constraints on usernames
- ✅ CORS enabled for cross-origin requests

### Production Recommendations
- 🔴 Replace SHA256 with bcrypt/Argon2
- 🔴 Add CSRF protection
- 🔴 Implement rate limiting
- 🔴 Use HTTPS/TLS
- 🔴 Move secrets to environment variables
- 🔴 Add input validation & sanitization
- 🔴 Implement request throttling
- 🔴 Add logging & monitoring

---

## 📊 Database Queries Reference

### Get User's Total Points
```sql
SELECT TotalPoints FROM Users WHERE UserID = ?
```

### Get All Completed Challenges for User
```sql
SELECT c.* FROM Challenges c
JOIN UserProgress up ON c.ChallengeID = up.ChallengeID
WHERE up.UserID = ?
ORDER BY up.CompletionDate DESC
```

### Update User Points After Challenge
```sql
UPDATE Users SET TotalPoints = ? WHERE UserID = ?
```

### Get Leaderboard
```sql
SELECT UserID, Username, TotalPoints, CurrentLevel,
       ROW_NUMBER() OVER (ORDER BY TotalPoints DESC) AS Rank
FROM Users
ORDER BY TotalPoints DESC
LIMIT 10
```

### Check If Challenge Is Already Completed
```sql
SELECT UserProgressID FROM UserProgress 
WHERE UserID = ? AND ChallengeID = ?
```

---

## 📱 Frontend Architecture

### Page Structure

**index.html (Authentication)**
- Login form
- Registration form
- Feature highlights
- Form validation

**dashboard.html (Main App)**
- Navigation bar (sticky)
- Overview section (stats, progress)
- Challenges section (grid with filters)
- Leaderboard section (table)
- Profile section (user stats + history)
- Challenge modal (details popup)
- Success modal (celebration)

### JavaScript Modules

**auth.js**
- Form submission handling
- Fetch API calls to register/login
- Error display
- Form switching

**dashboard.js**
- Session verification
- Data loading functions
- Section navigation
- Challenge interaction
- Modal management
- Real-time updates

---

## 🚀 Performance Optimizations

1. **Lazy Loading**: Challenges loaded on demand when switching tabs
2. **Caching**: User data cached in JavaScript variables
3. **Debouncing**: Navigation buttons debounced
4. **Minimal API Calls**: Data fetched only when sections are opened
5. **Database Indexing**: SQLite uses indexes on UserID, ChallengeID

---

## 📝 Notes for Developers

### Adding New Features
1. Add database schema changes to `init_db.py`
2. Create API routes in `app.py`
3. Add frontend UI in HTML files
4. Add interactivity in JS files
5. Style with CSS

### Testing Endpoints
Use curl or Postman:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice_eco","password":"password123"}' \
  --cookie-jar cookies.txt

curl -X GET http://localhost:5000/api/leaderboard \
  --cookie cookies.txt
```

### Database Inspection
```bash
sqlite3 environmental_platform.db
.schema
SELECT * FROM Users LIMIT 5;
SELECT * FROM Challenges LIMIT 3;
SELECT * FROM UserProgress LIMIT 10;
```

---

**Version:** 1.0
**Last Updated:** April 2026
**Author:** Full Stack Developer

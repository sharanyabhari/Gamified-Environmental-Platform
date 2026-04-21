# Gamified Environmental Educational Platform

A web application designed to teach environmental awareness through gamification, featuring challenges, points, levels, and leaderboards.

## Project Structure

```
├── backend/
│   ├── app.py                 # Flask application (main backend)
│   ├── init_db.py            # Database initialization script
│   └── environmental_platform.db  # SQLite database (created after init_db.py)
├── frontend/
│   ├── index.html            # Login/Register page
│   ├── dashboard.html        # Main dashboard
│   └── static/
│       ├── css/
│       │   ├── style.css     # Main stylesheet
│       │   └── dashboard.css # Dashboard-specific styles
│       └── js/
│           ├── auth.js       # Authentication logic
│           └── dashboard.js  # Dashboard functionality
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Features

### Gamification System
- **Points & Levels**: Users earn points by completing challenges and level up based on accumulated points
- **Challenges**: 12+ environmental education challenges with difficulty levels
- **Leaderboard**: Real-time global leaderboard showing top 10 players
- **Progressive Difficulty**: Easy, Medium, and Hard challenges with varying rewards
- **Categories**: Challenges organized by topic (Education, Assessment, Action, Lifestyle)

### User Management
- User registration and authentication
- Secure password hashing
- Session management
- User profile with statistics
- Personal challenge history

### Database Schema

#### Users Table
- UserID (Primary Key)
- Username (Unique)
- Password (Hashed)
- TotalPoints
- CurrentLevel
- CreatedDate

#### Challenges Table
- ChallengeID (Primary Key)
- Title
- Description
- Category
- PointsAwarded
- Difficulty (Easy/Medium/Hard)
- CreatedDate

#### UserProgress Table
- UserProgressID (Primary Key)
- UserID (Foreign Key)
- ChallengeID (Foreign Key)
- CompletionDate
- UNIQUE constraint on (UserID, ChallengeID)

### Level System
- Level 1: 0-99 points
- Level 2: 100-249 points
- Level 3: 250-499 points
- Level 4: 500-749 points
- Level 5: 750-999 points
- Level 6: 1000+ points

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
cd "Gamified Environemental Platofrm"
pip install -r requirements.txt
```

### Step 2: Initialize the Database
```bash
cd backend
python init_db.py
```

You should see:
```
✓ Database initialized successfully at environmental_platform.db
✓ Created tables: Users, Challenges, UserProgress
✓ Inserted sample challenges and users
```

### Step 3: Start the Flask Application
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Creating an Account
1. Click "Register here" on the login page
2. Enter a username and password (minimum 6 characters)
3. Confirm your password
4. Click "Create Account"

### Test Accounts (Pre-created)
- **Username**: alice_eco | **Password**: password123 (450 points, Level 5)
- **Username**: bob_green | **Password**: password456 (320 points, Level 3)
- **Username**: diana_nature | **Password**: passwordabc (510 points, Level 6)

### Completing Challenges
1. Click "Challenges" in the dashboard navigation
2. Browse available challenges or filter by difficulty
3. Click a challenge card to view details
4. Click "Complete Challenge" to earn points
5. Watch your progress bar fill and level up when reaching thresholds!

### Checking Your Progress
- **Overview**: See your current points, level, and recent achievements
- **Leaderboard**: View your ranking compared to other players
- **Profile**: Check detailed statistics, learning breakdown by category, and challenge history

## API Endpoints

### Authentication
- `POST /api/register` - Create new user account
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/check-session` - Verify logged-in status

### Challenges
- `GET /api/challenges` - Get all available challenges
- `GET /api/challenges/<user_id>` - Get challenges with completion status
- `POST /api/complete-challenge` - Mark challenge as completed

### User Data
- `GET /api/user/<user_id>` - Get user profile information
- `GET /api/user/<user_id>/stats` - Get detailed user statistics
- `GET /api/user/<user_id>/completed-challenges` - Get user's completed challenges

### Leaderboard
- `GET /api/leaderboard` - Get top 10 users by total points

## Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **SQLite**: Database (zero-configuration, file-based)
- **Python**: Server-side logic and API

### Frontend
- **HTML5**: Structure and semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (Vanilla)**: Interactive elements and API communication

### Architecture
- RESTful API design
- Session-based authentication
- CORS-enabled for cross-origin requests
- Responsive design for mobile and desktop

## Customization

### Adding New Challenges
Edit `backend/init_db.py` and add to the `sample_challenges` list:
```python
('Challenge Title', 'Challenge Description', 'Category', PointsValue, 'Difficulty'),
```

### Modifying Level Thresholds
Edit the `calculate_level()` function in `backend/app.py`:
```python
def calculate_level(total_points):
    if total_points >= 2000:
        return 7  # Add new level
    # ... modify values as needed
```

### Changing Colors
Edit CSS variables in `frontend/static/css/style.css`:
```css
:root {
    --primary-color: #2ecc71;      /* Change green color */
    --secondary-color: #3498db;    /* Change blue color */
    --accent-color: #f39c12;       /* Change yellow color */
}
```

## Troubleshooting

### Database Issues
If you get database errors, delete the existing database and reinitialize:
```bash
cd backend
del environmental_platform.db  # On Windows
python init_db.py
```

### Port Already in Use
If port 5000 is in use, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### CORS Errors
Ensure Flask-CORS is installed:
```bash
pip install flask-cors
```

## Future Enhancements

- [ ] Email verification for registration
- [ ] Password reset functionality
- [ ] Social login (Google, GitHub)
- [ ] Real-time notifications for level ups
- [ ] Friend system and social competition
- [ ] Achievement badges with unlock conditions
- [ ] Carbon footprint calculator integration
- [ ] Mobile app version
- [ ] Admin dashboard for managing challenges
- [ ] Analytics and progress tracking

## Security Notes

**⚠️ IMPORTANT**: This is a demonstration project. For production use:

1. **Password Hashing**: Use `werkzeug.security` instead of raw SHA256
2. **Database**: Use proper migrations with Alembic
3. **Authentication**: Implement JWT tokens or proper session management
4. **HTTPS**: Always use SSL/TLS in production
5. **Environment Variables**: Store sensitive data in `.env` files
6. **Input Validation**: Implement stricter validation and sanitization
7. **Rate Limiting**: Add rate limiting to prevent abuse
8. **CSRF Protection**: Implement CSRF tokens for form submissions

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please review the code comments or create an issue in the repository.

---

**Happy Learning! 🌍♻️**

"""
Gamified Environmental Educational Platform
Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
CORS(app)

DATABASE_PATH = 'environmental_platform.db'

# ============================================================================
# Database Helper Functions
# ============================================================================

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hash a password for secure storage (basic - use werkzeug in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_level(total_points):
    """
    Calculate user level based on accumulated points
    Level 1: 0-99 points
    Level 2: 100-249 points
    Level 3: 250-499 points
    Level 4: 500-749 points
    Level 5: 750-999 points
    Level 6: 1000+ points
    """
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

def get_points_for_next_level(current_level):
    """Get the total points needed to reach the next level"""
    level_thresholds = {1: 100, 2: 250, 3: 500, 4: 750, 5: 1000}
    return level_thresholds.get(current_level, 1000)

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# Authentication Routes
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO Users (Username, Password, TotalPoints, CurrentLevel)
        VALUES (?, ?, ?, ?)
        ''', (username, hash_password(password), 0, 1))
        conn.commit()
        
        # Get the new user's ID
        user = cursor.execute('SELECT UserID FROM Users WHERE Username = ?', (username,)).fetchone()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user_id': user['UserID']
        }), 201
    
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Username already exists'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate a user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM Users WHERE Username = ? AND Password = ?',
        (username, hash_password(password))
    ).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['UserID']
        session['username'] = user['Username']
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user_id': user['UserID'],
            'username': user['Username']
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout the current user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session['user_id'],
            'username': session['username']
        }), 200
    else:
        return jsonify({'logged_in': False}), 200

# ============================================================================
# User Routes
# ============================================================================

@app.route('/api/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get user profile information"""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE UserID = ?', (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    next_level_points = get_points_for_next_level(user['CurrentLevel'])
    progress_to_next_level = (user['TotalPoints'] / next_level_points) * 100
    
    return jsonify({
        'UserID': user['UserID'],
        'Username': user['Username'],
        'TotalPoints': user['TotalPoints'],
        'CurrentLevel': user['CurrentLevel'],
        'NextLevelPoints': next_level_points,
        'ProgressToNextLevel': min(progress_to_next_level, 100)
    }), 200

# ============================================================================
# Challenge Routes
# ============================================================================

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    """Get all available challenges"""
    conn = get_db_connection()
    challenges = conn.execute('''
    SELECT * FROM Challenges ORDER BY ChallengeID
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(ch) for ch in challenges]), 200

@app.route('/api/challenges/<int:user_id>', methods=['GET'])
@login_required
def get_challenges_with_status(user_id):
    """Get all challenges with completion status for a specific user"""
    conn = get_db_connection()
    
    # Get all challenges
    challenges = conn.execute('SELECT * FROM Challenges ORDER BY ChallengeID').fetchall()
    
    # Get completed challenges for this user
    completed = conn.execute('''
    SELECT ChallengeID FROM UserProgress WHERE UserID = ?
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    completed_ids = {ch['ChallengeID'] for ch in completed}
    
    result = []
    for ch in challenges:
        challenge_dict = dict(ch)
        challenge_dict['Completed'] = ch['ChallengeID'] in completed_ids
        result.append(challenge_dict)
    
    return jsonify(result), 200

# ============================================================================
# Challenge Completion Route
# ============================================================================

@app.route('/api/complete-challenge', methods=['POST'])
@login_required
def complete_challenge():
    """Mark a challenge as completed for the user"""
    data = request.get_json()
    user_id = session['user_id']
    challenge_id = data.get('challenge_id')
    
    if not challenge_id:
        return jsonify({'error': 'Challenge ID required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if challenge already completed
        existing = cursor.execute('''
        SELECT UserProgressID FROM UserProgress WHERE UserID = ? AND ChallengeID = ?
        ''', (user_id, challenge_id)).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'error': 'Challenge already completed'}), 400
        
        # Get challenge points
        challenge = cursor.execute('''
        SELECT PointsAwarded FROM Challenges WHERE ChallengeID = ?
        ''', (challenge_id,)).fetchone()
        
        if not challenge:
            conn.close()
            return jsonify({'error': 'Challenge not found'}), 404
        
        points_awarded = challenge['PointsAwarded']
        
        # Record completion
        cursor.execute('''
        INSERT INTO UserProgress (UserID, ChallengeID)
        VALUES (?, ?)
        ''', (user_id, challenge_id))
        
        # Get current user points
        user = cursor.execute('''
        SELECT TotalPoints, CurrentLevel FROM Users WHERE UserID = ?
        ''', (user_id,)).fetchone()
        
        new_total_points = user['TotalPoints'] + points_awarded
        old_level = user['CurrentLevel']
        new_level = calculate_level(new_total_points)
        
        # Update user points and level
        cursor.execute('''
        UPDATE Users SET TotalPoints = ?, CurrentLevel = ? WHERE UserID = ?
        ''', (new_total_points, new_level, user_id))
        
        conn.commit()
        conn.close()
        
        level_up = new_level > old_level
        
        return jsonify({
            'success': True,
            'message': f'Challenge completed! +{points_awarded} points',
            'points_awarded': points_awarded,
            'new_total_points': new_total_points,
            'new_level': new_level,
            'level_up': level_up,
            'old_level': old_level
        }), 200
    
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Challenge already completed'}), 400
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Leaderboard Route
# ============================================================================

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top 10 users ranked by total points"""
    conn = get_db_connection()
    
    leaderboard = conn.execute('''
    SELECT UserID, Username, TotalPoints, CurrentLevel,
           ROW_NUMBER() OVER (ORDER BY TotalPoints DESC) AS Rank
    FROM Users
    ORDER BY TotalPoints DESC
    LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return jsonify([dict(user) for user in leaderboard]), 200

# ============================================================================
# User Statistics Routes
# ============================================================================

@app.route('/api/user/<int:user_id>/completed-challenges', methods=['GET'])
@login_required
def get_user_completed_challenges(user_id):
    """Get list of challenges completed by a user"""
    conn = get_db_connection()
    
    completed = conn.execute('''
    SELECT 
        c.ChallengeID,
        c.Title,
        c.Description,
        c.PointsAwarded,
        c.Category,
        c.Difficulty,
        up.CompletionDate
    FROM UserProgress up
    JOIN Challenges c ON up.ChallengeID = c.ChallengeID
    WHERE up.UserID = ?
    ORDER BY up.CompletionDate DESC
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return jsonify([dict(ch) for ch in completed]), 200

@app.route('/api/user/<int:user_id>/stats', methods=['GET'])
@login_required
def get_user_stats(user_id):
    """Get user statistics"""
    conn = get_db_connection()
    
    user = conn.execute('SELECT * FROM Users WHERE UserID = ?', (user_id,)).fetchone()
    completed_count = conn.execute('''
    SELECT COUNT(*) as count FROM UserProgress WHERE UserID = ?
    ''', (user_id,)).fetchone()
    
    # Get category breakdown
    category_stats = conn.execute('''
    SELECT c.Category, COUNT(*) as count, SUM(c.PointsAwarded) as points
    FROM UserProgress up
    JOIN Challenges c ON up.ChallengeID = c.ChallengeID
    WHERE up.UserID = ?
    GROUP BY c.Category
    ORDER BY points DESC
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    next_level_points = get_points_for_next_level(user['CurrentLevel'])
    
    return jsonify({
        'UserID': user['UserID'],
        'Username': user['Username'],
        'TotalPoints': user['TotalPoints'],
        'CurrentLevel': user['CurrentLevel'],
        'NextLevelPoints': next_level_points,
        'ChallengesCompleted': completed_count['count'],
        'CategoryBreakdown': [dict(cat) for cat in category_stats]
    }), 200

# ============================================================================
# Main Page Routes
# ============================================================================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if database exists, if not create it
    if not os.path.exists(DATABASE_PATH):
        print("Database not found. Please run: python backend/init_db.py")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

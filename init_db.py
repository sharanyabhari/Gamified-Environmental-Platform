"""
Database Initialization Script for Gamified Environmental Platform
Creates the SQLite database with all required tables and sample data
"""

import sqlite3
import os

DATABASE_PATH = 'environmental_platform.db'

def init_database():
    """Initialize the database with schema and sample data"""
    
    # Remove existing database if it exists (for fresh start)
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    
    # Create connection
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
    CREATE TABLE Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        TotalPoints INTEGER DEFAULT 0,
        CurrentLevel INTEGER DEFAULT 1,
        CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create Challenges table
    cursor.execute('''
    CREATE TABLE Challenges (
        ChallengeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Description TEXT NOT NULL,
        Category TEXT DEFAULT 'General',
        PointsAwarded INTEGER NOT NULL,
        Difficulty TEXT DEFAULT 'Easy',
        CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create UserProgress table
    cursor.execute('''
    CREATE TABLE UserProgress (
        UserProgressID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER NOT NULL,
        ChallengeID INTEGER NOT NULL,
        CompletionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (ChallengeID) REFERENCES Challenges(ChallengeID),
        UNIQUE(UserID, ChallengeID)
    )
    ''')
    
    # Insert sample challenges
    sample_challenges = [
        ('Learn About Recycling', 'Complete a quiz about proper recycling practices and sustainability.', 'Education', 50, 'Easy'),
        ('Carbon Footprint Calculator', 'Calculate your personal carbon footprint and identify reduction areas.', 'Assessment', 75, 'Medium'),
        ('Plant a Tree Virtually', 'Learn about reforestation and plant a tree through our partner program.', 'Action', 100, 'Medium'),
        ('Save Water Challenge', 'Track water usage for a week and reduce consumption by 20%.', 'Lifestyle', 60, 'Easy'),
        ('Renewable Energy Quiz', 'Test your knowledge on solar, wind, and hydroelectric power.', 'Education', 55, 'Medium'),
        ('Ocean Conservation', 'Learn about marine ecosystems and ocean pollution prevention.', 'Education', 70, 'Medium'),
        ('Reduce Plastic Usage', 'Go plastic-free for 7 days and log your progress.', 'Lifestyle', 80, 'Hard'),
        ('Climate Change Facts', 'Complete the comprehensive climate science certification.', 'Education', 90, 'Hard'),
        ('Sustainable Shopping', 'Research and purchase 5 items from eco-friendly brands.', 'Action', 65, 'Medium'),
        ('Wildlife Protection', 'Learn about endangered species and support conservation efforts.', 'Action', 85, 'Hard'),
        ('Energy Audit Challenge', 'Conduct a home energy audit and improve efficiency.', 'Lifestyle', 75, 'Medium'),
        ('Composting Mastery', 'Start a compost bin and successfully process waste for 30 days.', 'Action', 70, 'Medium'),
    ]
    
    cursor.executemany('''
    INSERT INTO Challenges (Title, Description, Category, PointsAwarded, Difficulty)
    VALUES (?, ?, ?, ?, ?)
    ''', sample_challenges)
    
    # Insert sample users (passwords are plain text for demo - use hashing in production!)
    sample_users = [
        ('alice_eco', 'password123', 450, 5),
        ('bob_green', 'password456', 320, 3),
        ('charlie_planet', 'password789', 275, 3),
        ('diana_nature', 'passwordabc', 510, 6),
        ('evan_earth', 'passworddef', 190, 2),
    ]
    
    cursor.executemany('''
    INSERT INTO Users (Username, Password, TotalPoints, CurrentLevel)
    VALUES (?, ?, ?, ?)
    ''', sample_users)
    
    # Insert sample progress records (showing which challenges users completed)
    sample_progress = [
        (1, 1, '2026-04-05'),
        (1, 2, '2026-04-06'),
        (1, 3, '2026-04-07'),
        (1, 5, '2026-04-08'),
        (1, 7, '2026-04-10'),
        (2, 1, '2026-04-01'),
        (2, 2, '2026-04-03'),
        (2, 4, '2026-04-05'),
        (3, 2, '2026-04-02'),
        (3, 5, '2026-04-04'),
        (4, 1, '2026-03-30'),
        (4, 3, '2026-04-01'),
        (4, 6, '2026-04-05'),
        (4, 8, '2026-04-10'),
        (5, 1, '2026-04-09'),
    ]
    
    cursor.executemany('''
    INSERT INTO UserProgress (UserID, ChallengeID, CompletionDate)
    VALUES (?, ?, ?)
    ''', sample_progress)
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"✓ Database initialized successfully at {DATABASE_PATH}")
    print("✓ Created tables: Users, Challenges, UserProgress")
    print("✓ Inserted sample challenges and users")

if __name__ == '__main__':
    init_database()

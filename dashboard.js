/* ============================================================================
   Dashboard JavaScript - Main Application Logic
   ============================================================================ */

const API_BASE_URL = 'http://localhost:5000/api';
let currentUserId = null;
let currentUsername = null;
let allChallenges = [];
let activeFilters = 'all';
let selectedChallenge = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Check if user is logged in
    const sessionResponse = await fetch(`${API_BASE_URL}/check-session`, {
        credentials: 'include'
    });
    
    const sessionData = await sessionResponse.json();
    
    if (!sessionData.logged_in) {
        window.location.href = '/';
        return;
    }
    
    currentUserId = sessionData.user_id;
    currentUsername = sessionData.username;
    
    // Load dashboard data
    await loadDashboardData();
    await loadChallenges();
    await loadLeaderboard();
});

// ============================================================================
// Navigation Functions
// ============================================================================

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('section-active');
    });
    
    // Remove active class from nav items
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('section-active');
    }
    
    // Mark nav item as active
    event.target.classList.add('active');
    
    // Load section-specific data
    if (sectionId === 'leaderboard') {
        loadLeaderboard();
    } else if (sectionId === 'profile') {
        loadUserProfile();
    } else if (sectionId === 'challenges') {
        loadChallenges();
    } else if (sectionId === 'overview') {
        loadDashboardData();
    }
}

// ============================================================================
// Dashboard Overview Functions
// ============================================================================

async function loadDashboardData() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/${currentUserId}`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            console.error('Failed to load user data');
            return;
        }
        
        const userData = await response.json();
        
        // Update greeting
        document.getElementById('user-greeting').textContent = `Welcome back, ${currentUsername}! 🎮`;
        
        // Update stats
        document.getElementById('display-points').textContent = userData.TotalPoints;
        document.getElementById('display-level').textContent = userData.CurrentLevel;
        
        // Update progress bar
        const progressPercent = Math.min(userData.ProgressToNextLevel, 100);
        document.getElementById('level-progress').style.width = progressPercent + '%';
        document.getElementById('progress-text').textContent = 
            `${userData.TotalPoints} / ${userData.NextLevelPoints} points`;
        
        // Load completed challenges count
        await loadCompletedChallengesCount();
        
        // Load achievements
        await loadAchievements();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

async function loadCompletedChallengesCount() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/${currentUserId}/completed-challenges`, {
            credentials: 'include'
        });
        
        if (!response.ok) return;
        
        const challenges = await response.json();
        document.getElementById('display-completed').textContent = challenges.length;
    } catch (error) {
        console.error('Error loading completed challenges count:', error);
    }
}

async function loadAchievements() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/${currentUserId}/completed-challenges`, {
            credentials: 'include'
        });
        
        if (!response.ok) return;
        
        const completedChallenges = await response.json();
        const achievementsList = document.getElementById('achievements-list');
        
        if (completedChallenges.length === 0) {
            achievementsList.innerHTML = '<p class="placeholder">Complete challenges to earn badges!</p>';
            return;
        }
        
        // Show recent 4 achievements
        const recentChallenges = completedChallenges.slice(0, 4);
        
        const achievementsHTML = recentChallenges.map(ch => `
            <div class="achievement-badge" title="${ch.Title}">
                <div class="achievement-icon">🏅</div>
                <div class="achievement-name">${ch.Title}</div>
            </div>
        `).join('');
        
        achievementsList.innerHTML = achievementsHTML;
    } catch (error) {
        console.error('Error loading achievements:', error);
    }
}

// ============================================================================
// Challenges Functions
// ============================================================================

async function loadChallenges() {
    try {
        const response = await fetch(`${API_BASE_URL}/challenges/${currentUserId}`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            console.error('Failed to load challenges');
            return;
        }
        
        allChallenges = await response.json();
        displayChallenges(allChallenges);
    } catch (error) {
        console.error('Error loading challenges:', error);
    }
}

function displayChallenges(challenges) {
    const grid = document.getElementById('challenges-grid');
    
    if (challenges.length === 0) {
        grid.innerHTML = '<p class="placeholder">No challenges found</p>';
        return;
    }
    
    const html = challenges.map(challenge => `
        <div class="challenge-card ${challenge.Completed ? 'completed' : ''}" 
             onclick="selectChallenge(${challenge.ChallengeID})">
            <span class="difficulty-badge ${challenge.Difficulty}">${challenge.Difficulty}</span>
            <h3>${challenge.Title}</h3>
            <p>${challenge.Description}</p>
            <div class="challenge-footer">
                <span class="category-tag">${challenge.Category}</span>
                <span class="points-reward">+${challenge.PointsAwarded}pts</span>
            </div>
        </div>
    `).join('');
    
    grid.innerHTML = html;
}

function filterChallenges(difficulty) {
    activeFilters = difficulty;
    
    // Update filter button active state
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filter challenges
    let filtered = allChallenges;
    if (difficulty !== 'all') {
        filtered = allChallenges.filter(c => c.Difficulty === difficulty);
    }
    
    displayChallenges(filtered);
}

function selectChallenge(challengeId) {
    const challenge = allChallenges.find(c => c.ChallengeID === challengeId);
    if (!challenge) return;
    
    selectedChallenge = challenge;
    
    // Populate modal
    document.getElementById('modal-title').textContent = challenge.Title;
    document.getElementById('modal-description').textContent = challenge.Description;
    document.getElementById('modal-category').textContent = challenge.Category;
    document.getElementById('modal-difficulty').textContent = challenge.Difficulty;
    document.getElementById('modal-points').textContent = `+${challenge.PointsAwarded}`;
    
    // Show/hide complete button based on completion status
    const completeBtn = document.getElementById('complete-btn');
    if (challenge.Completed) {
        completeBtn.textContent = 'Already Completed';
        completeBtn.disabled = true;
    } else {
        completeBtn.textContent = 'Complete Challenge';
        completeBtn.disabled = false;
    }
    
    // Show modal
    document.getElementById('challenge-modal').classList.add('show');
}

function closeChallengeModal() {
    document.getElementById('challenge-modal').classList.remove('show');
    selectedChallenge = null;
}

async function completeChallenge() {
    if (!selectedChallenge) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/complete-challenge`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                challenge_id: selectedChallenge.ChallengeID
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            alert(data.error || 'Failed to complete challenge');
            return;
        }
        
        // Close challenge modal
        closeChallengeModal();
        
        // Show success modal
        showSuccessModal(data);
        
        // Reload data after a delay
        setTimeout(() => {
            loadDashboardData();
            loadChallenges();
        }, 1500);
    } catch (error) {
        console.error('Error completing challenge:', error);
        alert('Error completing challenge');
    }
}

function showSuccessModal(data) {
    document.getElementById('success-title').textContent = data.message;
    document.getElementById('success-message').textContent = `+${data.points_awarded} Points Earned!`;
    
    // Show level up if applicable
    const levelUpInfo = document.getElementById('level-up-info');
    if (data.level_up) {
        levelUpInfo.style.display = 'block';
        document.getElementById('level-up-detail').textContent = 
            `You've reached Level ${data.new_level}! 🎉`;
    } else {
        levelUpInfo.style.display = 'none';
    }
    
    document.getElementById('success-modal').classList.add('show');
}

function closeSuccessModal() {
    document.getElementById('success-modal').classList.remove('show');
}

// ============================================================================
// Leaderboard Functions
// ============================================================================

async function loadLeaderboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/leaderboard`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            console.error('Failed to load leaderboard');
            return;
        }
        
        const leaderboard = await response.json();
        displayLeaderboard(leaderboard);
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

function displayLeaderboard(users) {
    const tbody = document.getElementById('leaderboard-body');
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="loading">No users found</td></tr>';
        return;
    }
    
    const html = users.map((user, index) => `
        <tr class="rank-${user.Rank}">
            <td class="rank-medal">${user.Rank}</td>
            <td class="player-name">${user.Username}</td>
            <td>${user.TotalPoints.toLocaleString()}</td>
            <td><span class="level-badge" style="font-size: 1rem; width: 50px; height: 50px;">${user.CurrentLevel}</span></td>
        </tr>
    `).join('');
    
    tbody.innerHTML = html;
}

// ============================================================================
// Profile Functions
// ============================================================================

async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/${currentUserId}/stats`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            console.error('Failed to load user stats');
            return;
        }
        
        const stats = await response.json();
        
        // Update profile header
        document.getElementById('profile-username').textContent = stats.Username;
        document.getElementById('profile-level').textContent = `Level ${stats.CurrentLevel}`;
        
        // Update stats
        document.getElementById('profile-points').textContent = stats.TotalPoints.toLocaleString();
        document.getElementById('profile-level-num').textContent = stats.CurrentLevel;
        document.getElementById('profile-completed').textContent = stats.ChallengesCompleted;
        
        // Display category breakdown
        displayCategoryBreakdown(stats.CategoryBreakdown);
        
        // Load challenge history
        await loadChallengeHistory();
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
}

function displayCategoryBreakdown(categories) {
    const container = document.getElementById('category-breakdown');
    
    if (categories.length === 0) {
        container.innerHTML = '<p>No challenges completed yet.</p>';
        return;
    }
    
    const html = categories.map(cat => `
        <div class="category-item">
            <span class="category-name">${cat.Category}</span>
            <div class="category-info">
                <div class="category-stat">
                    <div class="label">Challenges</div>
                    <div class="value">${cat.count}</div>
                </div>
                <div class="category-stat">
                    <div class="label">Points</div>
                    <div class="value">${cat.points}</div>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

async function loadChallengeHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/user/${currentUserId}/completed-challenges`, {
            credentials: 'include'
        });
        
        if (!response.ok) return;
        
        const completed = await response.json();
        const container = document.getElementById('challenge-history');
        
        if (completed.length === 0) {
            container.innerHTML = '<p>No challenges completed yet.</p>';
            return;
        }
        
        // Show recent 5
        const recent = completed.slice(0, 5);
        
        const html = recent.map(ch => {
            const date = new Date(ch.CompletionDate).toLocaleDateString();
            return `
                <div class="history-item">
                    <div>
                        <div class="history-title">${ch.Title}</div>
                        <div class="history-date">${date}</div>
                    </div>
                    <span class="history-points">+${ch.PointsAwarded}</span>
                </div>
            `;
        }).join('');
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading challenge history:', error);
    }
}

// ============================================================================
// Logout Function
// ============================================================================

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        // Redirect to login
        window.location.href = '/';
    } catch (error) {
        console.error('Error logging out:', error);
        window.location.href = '/';
    }
}

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    const challengeModal = document.getElementById('challenge-modal');
    const successModal = document.getElementById('success-modal');
    
    if (e.target === challengeModal) {
        closeChallengeModal();
    }
    if (e.target === successModal) {
        closeSuccessModal();
    }
});

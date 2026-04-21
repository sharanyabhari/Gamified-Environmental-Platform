/* ============================================================================
   Authentication JavaScript - Login & Register Functionality
   ============================================================================ */

const API_BASE_URL = 'http://localhost:5000/api';

// Switch between login and register forms
function switchForm(formType) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    if (formType === 'login') {
        loginForm.classList.add('auth-form-active');
        registerForm.classList.remove('auth-form-active');
    } else {
        registerForm.classList.add('auth-form-active');
        loginForm.classList.remove('auth-form-active');
    }
}

// Handle Login Form Submission
document.getElementById('login-submit').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');
    
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            errorDiv.textContent = data.error || 'Login failed';
            errorDiv.classList.add('show');
            return;
        }
        
        // Login successful
        errorDiv.classList.remove('show');
        console.log('Login successful:', data);
        
        // Redirect to dashboard
        window.location.href = '/dashboard';
    } catch (error) {
        console.error('Error:', error);
        errorDiv.textContent = 'Connection error. Please try again.';
        errorDiv.classList.add('show');
    }
});

// Handle Register Form Submission
document.getElementById('register-submit').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;
    const errorDiv = document.getElementById('register-error');
    
    // Validate passwords match
    if (password !== confirm) {
        errorDiv.textContent = 'Passwords do not match';
        errorDiv.classList.add('show');
        return;
    }
    
    // Validate password length
    if (password.length < 6) {
        errorDiv.textContent = 'Password must be at least 6 characters';
        errorDiv.classList.add('show');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            errorDiv.textContent = data.error || 'Registration failed';
            errorDiv.classList.add('show');
            return;
        }
        
        // Registration successful
        errorDiv.classList.remove('show');
        console.log('Registration successful:', data);
        
        // Show success message and switch to login
        alert('Account created successfully! Please login.');
        switchForm('login');
        document.getElementById('login-submit').reset();
        document.getElementById('register-submit').reset();
    } catch (error) {
        console.error('Error:', error);
        errorDiv.textContent = 'Connection error. Please try again.';
        errorDiv.classList.add('show');
    }
});

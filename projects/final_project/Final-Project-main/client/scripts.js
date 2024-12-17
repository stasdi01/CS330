// Helper function to set a cookie
function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days  *24 * 60 * 60 * 1000).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/;`;
}

// Helper function to get a cookie
function getCookie(name) {
    const cookie = document.cookie
        .split('; ')
        .find(row => row.startsWith(`${name}=`));
    return cookie ? cookie.split('=')[1] : null;

}

// Helper function to delete a cookie
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// Register logic
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://localhost:5000/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();
            if (response.ok) {
                alert('Registration successful!');
                window.location.href = 'login.html';
            } else {
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error('Error during registration:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// Login logic
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();
            if (response.ok) {
                setCookie('access_token', data.access_token, 1); // Save token for 1 day
                alert('Login successful!');
                window.location.href = 'protected.html';
            } else {
                alert(`Error: ${data.message}`);
            }
        } catch (error) {
            console.error('Error during login:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// Logout logic
function logout() {
    deleteCookie('access_token');
    alert('Logged out successfully!');
    window.location.href = 'login.html';
}

// Fetch user details on the protected page
if (window.location.pathname.endsWith('protected.html')) {
    document.addEventListener('DOMContentLoaded', async () => {
        const token = getCookie('access_token');
        console.log(token)

        if (!token) {
            alert('Not logged in! Redirecting to login.');
            window.location.href = 'login.html';
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/protected', {
                method: 'GET',
                headers: {'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
                
                },
                credentials:'include',
            });

            if (!response.ok) {
                throw new Error('Failed to access protected route.');
            }

           
            const data = await response.json();
            document.getElementById('user-details').textContent = `Welcome, ${data.user.username}`;

        } catch (error) {
            console.error('Error accessing protected route:', error);
        }
    });

    // Attach logout button logic
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('error-message');

            // Clear previous errors
            if (errorMessage) errorMessage.style.display = 'none';

            try {
                // Use FormData as OAuth2PasswordRequestForm expects form data
                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);

                const response = await fetch('/auth/login', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    const token = data.access_token;

                    // Store token
                    localStorage.setItem('access_token', token);
                    document.cookie = `access_token=${token}; path=/; max-age=1800; SameSite=Strict`;

                    // Redirect to dashboard
                    window.location.href = '/dashboard';
                } else {
                    const errorData = await response.json();
                    if (errorMessage) {
                        errorMessage.textContent = errorData.detail || 'Login failed';
                        errorMessage.style.display = 'block';
                    }
                }
            } catch (error) {
                console.error('Login error:', error);
                if (errorMessage) {
                    errorMessage.textContent = 'Network error occurred';
                    errorMessage.style.display = 'block';
                }
            }
        });
    }
});

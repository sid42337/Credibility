const passwordInput = document.getElementById('passwordInput');
const strengthText = document.getElementById('strengthText');
const strengthBar = document.getElementById('strengthBar');
const suggestionsList = document.getElementById('suggestionsList');
const breachStatus = document.getElementById('breachStatus');
const loadingIndicator = document.getElementById('loadingIndicator');
const togglePassword = document.getElementById('togglePassword'); // Get toggle icon container
const eyeOpenIcon = document.getElementById('eyeOpen');       // Get open eye icon
const eyeClosedIcon = document.getElementById('eyeClosed');   // Get closed eye icon

let debounceTimer;

async function checkPassword() {
    clearTimeout(debounceTimer); // Clear any existing timer

    const password = passwordInput.value;

    // Reset UI if password is empty
    if (password.length === 0) {
        strengthText.textContent = 'N/A';
        strengthText.className = 'font-bold text-gray-500';
        strengthBar.style.width = '0%';
        strengthBar.className = 'bg-blue-500 h-2.5 rounded-full transition-all duration-300 ease-in-out';
        suggestionsList.innerHTML = '';
        breachStatus.textContent = 'Type a password to check.';
        loadingIndicator.classList.add('hidden');
        return;
    }

    // Debounce the API calls to avoid too many requests on rapid typing
    // This debounce is no longer strictly necessary if triggered only by button click,
    // but kept for robustness if onkeyup is re-added or for future features.
    debounceTimer = setTimeout(async () => {
        // Show loading indicator for breach check
        loadingIndicator.classList.remove('hidden');
        breachStatus.textContent = ''; // Clear previous status

        try {
            // 1. Check Password Strength
            const strengthResponse = await fetch('/analyze-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password }),
            });
            const strengthData = await strengthResponse.json();
            updateStrengthUI(strengthData);

            // 2. Check Password Breach
            const breachResponse = await fetch('/check-breach', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password }),
            });
            const breachData = await breachResponse.json();
            updateBreachUI(breachData);

        } catch (error) {
            console.error('Error:', error);
            strengthText.textContent = 'Error';
            breachStatus.textContent = 'Error checking password. Please try again.';
        } finally {
            loadingIndicator.classList.add('hidden'); // Hide loading indicator
        }
    }, 500); // 500ms debounce time
}

function updateStrengthUI(data) {
    strengthText.textContent = data.strength;
    strengthBar.style.width = `${data.score}%`;

    // Update strength text color and bar color based on strength
    strengthText.classList.remove('text-red-500', 'text-amber-500', 'text-green-500', 'text-gray-500', 'text-emerald-600');
    strengthBar.classList.remove('strength-weak', 'strength-medium', 'strength-strong', 'strength-very-strong', 'bg-blue-500');

    if (data.strength === 'Weak') {
        strengthText.classList.add('text-red-500');
        strengthBar.classList.add('strength-weak');
    } else if (data.strength === 'Medium') {
        strengthText.classList.add('text-amber-500');
        strengthBar.classList.add('strength-medium');
    } else if (data.strength === 'Strong') {
        strengthText.classList.add('text-green-500');
        strengthBar.classList.add('strength-strong');
    } else if (data.strength === 'Very Strong') {
        strengthText.classList.add('text-emerald-600');
        strengthBar.classList.add('strength-very-strong');
    }
    else {
        strengthText.classList.add('text-gray-500'); // Default for N/A or initial state
        strengthBar.classList.add('bg-blue-500');
    }

    // Update suggestions
    suggestionsList.innerHTML = '';
    data.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        li.classList.add('suggestion-item'); // Add a class for styling
        suggestionsList.appendChild(li);
    });
}

function updateBreachUI(data) {
    breachStatus.textContent = data.message;
    if (data.is_pwned) {
        breachStatus.classList.add('text-red-600', 'font-semibold');
        breachStatus.classList.remove('text-green-600', 'text-gray-600');
    } else {
        breachStatus.classList.remove('text-red-600', 'font-semibold', 'text-gray-600');
        breachStatus.classList.add('text-green-600');
    }
}

// Function to toggle password visibility
function togglePasswordVisibility() {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeOpenIcon.classList.add('hidden');
        eyeClosedIcon.classList.remove('hidden');
    } else {
        passwordInput.type = 'password';
        eyeOpenIcon.classList.remove('hidden');
        eyeClosedIcon.classList.add('hidden');
    }
}

// Initial call to set up the UI
document.addEventListener('DOMContentLoaded', () => {
    checkPassword(); // Call on load to set initial state for empty input
});

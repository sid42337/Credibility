# Credibility - Password Strength & Breach Checker

**Credibility** is a comprehensive web tool designed to help users create stronger passwords and check if their existing passwords have been compromised in known data breaches. It combines robust local password analysis with external breach data, providing immediate feedback and actionable suggestions.

## ✨ Features

- **Real-time Password Strength Analysis:** Evaluates password strength, providing a score and visual strength bar, along with intelligent suggestions.
- **Have I Been Pwned (HIBP) Integration:** Securely checks if a password (using a k-anonymity partial hash) has appeared in known data breaches.
- **Password Visibility Toggle:** Allows users to show or hide their typed password for convenience and verification.
- **Responsive Design:** A clean and intuitive user interface built with Tailwind CSS, ensuring usability across various devices.
- **Flask Backend:** A lightweight and efficient Python Flask server handles the analysis and API interactions.

## 🚀 Live Demo

Experience "Credibility" live: [https://credibility-password-checker.onrender.com](https://credibility-password-checker.onrender.com)

## 📁 Project Structure

```markdown
```
credibility/
├── main.py                     # Main Flask application file
├── password_analyzer.py        # Python module for password strength analysis (custom + zxcvbn)
├── hibp_checker.py             # Python module for Have I Been Pwned API interaction
├── requirements.txt            # Lists all Python dependencies
├── templates/                  # Contains HTML templates
│   └── index.html              # Main HTML page for the application
└── static/                     # Contains static assets (CSS, JavaScript)
    ├── style.css               # Custom CSS for styling
    └── script.js               # Frontend JavaScript for interactivity
```


## ⚙️ Local Setup

Follow these steps to get **Credibility** running on your local machine.

### Prerequisites

- Python 3.7+ installed on your system.
- `pip` (Python package installer).

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/YourUsername/credibility.git
    cd credibility
    ```

    *(Replace `YourUsername` with your actual GitHub username if necessary)*

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - **On Windows:**

        ```bash
        .\venv\Scripts\activate
        ```

    - **On macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Flask development server:**

    ```bash
    python main.py
    ```

    You should see output similar to:

    ```
     * Serving Flask app 'main'
     * Debug mode: off
     * Running on http://127.0.0.1:8000
     Press CTRL+C to quit
    ```

2. **Access the application:**

    Open your browser and navigate to:

    ```
    http://127.0.0.1:8000
    ```

## 💡 Usage

1. **Enter your password:** Type any password into the input field.
2. **Check Strength:** The "Strength" bar and suggestions will update in real-time to help you improve your password.
3. **Check Breach Status:** The "Breach Status" section shows if your password has appeared in known data breaches via the HIBP API.
4. **Toggle Visibility:** Use the eye icon to show/hide the entered password.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

*(Note: You’ll need to create a `LICENSE` file in your repository containing the MIT License text.)*

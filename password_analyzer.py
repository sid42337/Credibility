import re
from zxcvbn import zxcvbn

def analyze_password_strength(password: str) -> dict:
    """
    Analyzes the strength of a given password based on length, character types,
    common patterns, repetition, dictionary words, and also incorporates zxcvbn's analysis.
    """
    score = 0
    suggestions = []

    # 1. Length Check
    if len(password) >= 21:
        score += 40
    elif len(password) >= 17:
        score += 30
    elif len(password) >= 12:
        score += 20
    elif len(password) >= 8:
        score += 10
    
    if len(password) < 8:
        suggestions.append("Password should be at least 8 characters long, preferably 12 or more.")


    # 2. Character Type Checks
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    char_types = sum([has_lowercase, has_uppercase, has_digit, has_symbol])

    if char_types == 4:
        score += 30
    elif char_types == 3:
        score += 20
    
    if char_types < 3:
        suggestions.append("Include a mix of at least three of uppercase letters, lowercase letters, numbers, and symbols.")


    # 3. Avoid common sequential patterns (3 or more characters)
    sequential_patterns_regex = (
        r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|'
        r'zyx|yxw|xwv|wvu|vut|uts|tsr|srq|rqp|qpo|pon|onm|nml|mlk|lkj|kji|jih|ihg|hgf|gfe|fed|edc|dcb|cba|'
        r'012|123|234|345|456|567|678|789|'
        r'987|876|765|654|543|432|321|210)'
    )
    if not re.search(sequential_patterns_regex, password, re.IGNORECASE):
        score += 10
    if re.search(sequential_patterns_regex, password, re.IGNORECASE):
        suggestions.append("Avoid common sequential patterns (e.g., 'abc', '123').")

    # 4. Avoid repetition (3 or more identical characters consecutively)
    repetition_regex = r'(.)\1{2,}'
    if not re.search(repetition_regex, password):
        score += 10
    if re.search(repetition_regex, password):
        suggestions.append("Avoid repeating the same character three or more times consecutively.")

    # 5. Avoid common dictionary words found in data breaches
    common_words_regex = r'(qwerty|password|admin|login|welcome|letmein)'
    if not re.search(common_words_regex, password, re.IGNORECASE):
        score += 10
    if re.search(common_words_regex, password, re.IGNORECASE):
        suggestions.append("Avoid very common words like 'password' or 'qwerty' as they are easily guessable and common targets.")

    # Calculate custom score scaled to 0-100
    custom_scaled_score = score

    # 6. Zxcvbn Score Integration
    zxcvbn_result = zxcvbn(password)
    zxcvbn_scaled_score = zxcvbn_result['score'] * 25

    # Combine suggestions from zxcvbn
    if zxcvbn_result.get('feedback') and zxcvbn_result['feedback'].get('suggestions'):
        for suggestion in zxcvbn_result['feedback']['suggestions']:
            if suggestion not in suggestions:
                suggestions.append(suggestion)

    # Calculate final score as a weighted average of custom and zxcvbn scores
    final_score = (custom_scaled_score * 0.5 + zxcvbn_scaled_score * 0.5)

    # Determine strength level based on the final averaged score
    strength = "Weak"
    if final_score >= 90:
        strength = "Very Strong"
    elif final_score >= 80:
        strength = "Strong"
    elif final_score >= 50:
        strength = "Medium"

    final_suggestions = suggestions if suggestions else ["Great password!"]

    return {
        "strength": strength,
        "score": min(round(final_score), 100),
        "suggestions": final_suggestions
    }

# if __name__ == "__main__":
#     # Example usage for testing
#     print("--- Password Strength Analysis Examples ---")
#     print("Password 'password123':", analyze_password_strength("password123"))
#     print("Password 'MySuperSecureP@ssw0rd!':", analyze_password_strength("MySuperSecureP@ssw0rd!"))
#     print("Password 'short':", analyze_password_strength("short"))
#     print("Password 'aaaaaa':", analyze_password_strength("aaaaaa"))
#     print("Password '123':", analyze_password_strength("123"))
#     print("Password 'abcabc':", analyze_password_strength("abcabc"))
#     print("Password 'Tr0ub4dor&3':", analyze_password_strength("Tr0ub4dor&3"))
#     print("Password 'p@$$w0rd':", analyze_password_strength("p@$$w0rd"))
#     print("Password 'a':", analyze_password_strength("a"))
#     print("Password '111':", analyze_password_strength("111"))

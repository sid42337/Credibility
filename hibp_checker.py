import hashlib
import httpx
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def check_password_breach(password: str) -> dict:
    # Hash the password using SHA-1
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # Extract prefix (first 5 chars) and suffix for HIBP API
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]

    hibp_api_url = f"https://api.pwnedpasswords.com/range/{prefix}"

    # Production considerations:
    # 1. Timeout for HTTP requests to prevent hanging
    # 2. Retry mechanism for transient network issues or rate limits
    # 3. Consider an API key if HIBP ever requires one for this endpoint (currently not needed for range API)
    
    max_retries = 3
    initial_backoff = 0.5 # seconds

    for attempt in range(max_retries):
        try:
            # Use a timeout for the request
            async with httpx.AsyncClient(timeout=5.0) as client: # 5-second timeout
                response = await client.get(hibp_api_url)
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

            pwned_hashes = response.text.splitlines()

            found_count = 0
            for line in pwned_hashes:
                # Each line in HIBP response is in format: Suffix:Count
                parts = line.split(':')
                if len(parts) == 2:
                    hibp_suffix = parts[0]
                    count = int(parts[1])
                    if hibp_suffix == suffix:
                        found_count = count
                        break # Match found, no need to check further

            return {
                "is_pwned": found_count > 0,
                "pwn_count": found_count,
                "message": f"Found in {found_count} breaches." if found_count > 0 else "Not found in any known breaches."
            }
        except httpx.HTTPStatusError as e:
            # Handle specific HTTP errors
            if e.response.status_code == 429: # Too Many Requests (Rate Limit)
                retry_after = int(e.response.headers.get('Retry-After', initial_backoff * (2 ** attempt)))
                logging.warning(f"Rate limit hit. Retrying in {retry_after} seconds (Attempt {attempt + 1}/{max_retries})...")
                await asyncio.sleep(retry_after)
            elif 400 <= e.response.status_code < 500:
                logging.error(f"Client error checking breach status: HTTP {e.response.status_code} - {e.response.text}")
                return {
                    "is_pwned": False,
                    "pwn_count": 0,
                    "message": f"Error checking breach status: Client Error {e.response.status_code}"
                }
            else: # Server errors (5xx) or other unhandled HTTP errors
                logging.error(f"Server error checking breach status: HTTP {e.response.status_code} - {e.response.text}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(initial_backoff * (2 ** attempt)) # Exponential backoff
                else:
                    return {
                        "is_pwned": False,
                        "pwn_count": 0,
                        "message": f"Error checking breach status: Server Error {e.response.status_code}"
                    }
        except httpx.RequestError as e:
            # Handle network-related errors (e.g., DNS resolution, connection refused, timeout)
            logging.error(f"Network error checking breach status (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(initial_backoff * (2 ** attempt)) # Exponential backoff
            else:
                return {
                    "is_pwned": False,
                    "pwn_count": 0,
                    "message": f"Network error checking breach status: {e}"
                }
        except Exception as e:
            # Catch any other unexpected errors
            logging.critical(f"An unexpected error occurred in HIBP checker: {e}", exc_info=True)
            return {
                "is_pwned": False,
                "pwn_count": 0,
                "message": f"An unexpected error occurred: {e}"
            }
    
    # If all retries fail
    return {
        "is_pwned": False,
        "pwn_count": 0,
        "message": "Failed to check breach status after multiple retries."
    }


# if __name__ == "__main__":
#     import asyncio

#     async def test_hibp():
#         print("--- HaveIBeenPwned API Examples ---")
#         # Example of a known pwned password (for testing purposes)
#         print("Password 'password':", await check_password_breach("password"))
#         # Example of a likely not pwned password (highly random)
#         print("Password 'aVerySecureRandomPassword123!':", await check_password_breach("aVerySecureRandomPassword123!"))
#         # Example to test timeout/error handling (might need to simulate network issues)
#         # print("Password 'testtimeout':", await check_password_breach("testtimeout"))

#     asyncio.run(test_hibp())

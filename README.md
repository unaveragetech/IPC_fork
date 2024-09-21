

# InstagramPasswordCracker

This script is designed to brute-force an Instagram account using a specified username and a list of passwords provided via standard input.

**I take NO responsibility for the use of this script. This code is intended for educational purposes. Please DO NOT use this program for malicious purposes.**

## Overview

The script automates the process of logging into Instagram by testing a series of passwords against a given username. It uses the `splinter` library to interact with the Instagram website, allowing for automated browser actions. This makes it easier to attempt multiple password logins without manual input.

## Features

### 1. **Brute-Force Password Cracking**
The script attempts to log in to the specified Instagram account using a list of passwords. This list should be provided through standard input, with each password on a new line.

### 2. **Browser Selection**
Users can select from several browsers:
- Firefox (default)
- Chrome
- Edge
- Safari
- Opera

This flexibility allows users to choose their preferred browser or the one that best suits their system configuration.

### 3. **Password Strength Check**
Before testing a password, the script evaluates its strength based on its length:
- **Weak**: Less than 8 characters
- **Medium**: Between 8 and 12 characters
- **Strong**: More than 12 characters

This check helps prioritize stronger passwords and can guide users in refining their password lists.

### 4. **Automatic Package Installation**
The script checks for required libraries (`splinter`, `tqdm`) upon execution. If any are missing, the script automatically installs them using `pip`. After installation, the script restarts itself to ensure all dependencies are loaded, simplifying setup for the user.

### 5. **Retry Limit**
To prevent excessive login attempts that could trigger Instagram's security measures, the script implements a retry limit. If the script encounters a specific error message repeatedly (indicating login failure), it counts these retries and stops after a defined number (default: 5 retries). This feature reduces the risk of account lockout.

### 6. **User-Friendly Progress Indicator**
Using the `tqdm` library, the script includes a progress bar that visually indicates the number of passwords tested. This provides immediate feedback to the user, making the process more engaging.

### 7. **Timeout Management**
Instagram imposes timeouts when too many incorrect login attempts are made in a short period. Typically, this timeout occurs after 14 to 25 failed attempts and lasts about 11 minutes and 35 seconds. The script is designed to:
- Detect this timeout condition through specific error messages.
- Automatically wait for the specified timeout period before resuming password testing.

This feature helps avoid unnecessary account lockouts and ensures a more strategic approach to brute-forcing.

### 8. **Logging**
All password attempts and results are logged to a file named `login_attempts.log`. This log includes timestamps and details about each attempted password, making it easy to track progress and analyze results after execution.

## How the Script Works

1. **Initialization**: The script starts by importing necessary libraries and checking for required packages. If any packages are missing, they are installed automatically.

2. **User Input**: The script takes the Instagram username and an optional timeout duration from command-line arguments. If the timeout is not specified, it defaults to 11 minutes and 35 seconds.

3. **Browser Setup**: The user selects the browser they wish to use for testing. The script initializes a headless browser session for seamless operation.

4. **Password Testing**:
   - The script reads passwords from standard input and iterates through each password.
   - For each password, it checks its strength and logs this information.
   - The password is filled into the login form, and the script attempts to log in.

5. **Handling Failures**:
   - If the login attempt fails, the script checks for a timeout error.
   - If a timeout is detected, it waits for the defined timeout period, displaying a countdown for user awareness.
   - If the maximum retry limit is reached, the script exits gracefully, preventing further lockout.

6. **Successful Login**: If a password successfully logs in, the script captures it and displays the result, concluding the execution.

## Usage

To run the script, provide the Instagram username and pipe the password list to the script. The password list must separate each password with a newline.

### Command Format:
```bash
python script.py <username> [timeout_seconds]
```

- `<username>`: The Instagram username you wish to test.
- `[timeout_seconds]`: Optional parameter to specify a custom timeout duration (in seconds). If not provided, the default timeout of 11 minutes and 35 seconds will be used.

### Example:
```bash
python script.py myusername < password_list.txt
```

## Notes

- Instagram's security measures can trigger a timeout after a series of incorrect password attempts. This script intelligently waits during these timeouts and resumes testing, minimizing the chance of account lockout.
- The average speed for testing passwords is around 60 to 125 per hour, mainly limited by Instagram’s timeout policies.


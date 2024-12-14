import os

def main():
     # Initialize password storage file in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    passwords_file = os.path.join(script_dir, "passwords.txt")
    
    # Display student info
    studentInfo()

    # Display welcome message
    welcomeMsg()

    # Prompt user for a password
    passWord = input("\nPlease create a password:\n")

    # Call function for password validation and reuse check
    passWord = correctPW(passWord, passwords_file)

    # Save the valid password to the file
    save_password(passWord, passwords_file)

# --- Functions ----------

# Student info
def studentInfo():
    print("\nName:\tRicardo Casillas")
    print("Class:\tCYB333")
    print("Date:\t13DEC2024")

# Welcome message
def welcomeMsg():
    print("\nThis program will prompt the user to enter a password with the following requirements:")
    print("\t- No less than 6 characters in length")
    print("\t- No more than 12 characters in length")
    print("\t- No spaces")
    print("\t- At least one numerical digit")
    print("\t- At least one alphabetical character")
    print("\t- At least one UpperCase character")

def containsLetterAndNumber(input_password):
    return input_password.isalnum() and not input_password.isalpha() and not input_password.isdigit()

def containsBlankSpace(input_password):
    return ' ' in input_password

# Validate password requirements
def correctPW(passWord, passwords_file):
    while True:
        # Check if password has been used before
        if is_password_used(passWord, passwords_file):
            print("\nSorry! This password has already been used. Please choose a different one.")
            passWord = input("\nPlease create a new password:\n")
            continue

        # Check for minimum and maximum character requirement
        if (len(passWord) < 6) or (len(passWord) > 12):
            print("\nSorry! Your password is invalid.")
            print("It must be no less than 6 characters and no more than 12 characters in length.")
            passWord = input("\nPlease create a password:\n")
            continue

        # Check for one numerical digit and alphabetical character requirement
        if not containsLetterAndNumber(passWord):
            print("\nSorry! Your password is invalid.")
            print("It must contain at least one alphabetical character and one numerical digit.")
            passWord = input("\nPlease create a password:\n")
            continue

        # Check for spaces
        if containsBlankSpace(passWord):
            print("\nSorry! Your password is invalid.")
            print("It shouldn't have any blank space in it.")
            passWord = input("\nPlease create a password:\n")
            continue

        # Check for at least one uppercase letter
        if not any(char.isupper() for char in passWord):
            print("\nSorry! Your password is invalid.")
            print("It should contain at least one Uppercase letter.")
            passWord = input("\nPlease create a password:\n")
            continue

        # If all conditions are met, break the loop
        print("\nCongratulations! Your password is valid!")
        break
    
    return passWord

# Check if the password has already been used
def is_password_used(passWord, passwords_file):
    try:
        with open(passwords_file, "r") as file:
            used_passwords = file.read().splitlines()
            return passWord in used_passwords
    except FileNotFoundError:
        return False

# Save the valid password to a file
def save_password(passWord, passwords_file):
    with open(passwords_file, "a") as file:
        file.write(passWord + "\n")

# --- Execute ----------
main()
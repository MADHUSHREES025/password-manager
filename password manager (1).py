#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sqlite3
import base64
from cryptography.fernet import Fernet
import getpass
import hashlib

# Database setup
def init_db():
    with sqlite3.connect('password_manager.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                website TEXT,
                username TEXT,
                password TEXT
            )
        ''')
    conn.close()

init_db()

# Generate a 32-byte URL-safe base64-encoded key based on the master password
def generate_key(master_password):
    hash = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hash[:32])

# Encrypt and decrypt functions
def encrypt_password(key, password):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

# Add a new password entry
def add_password(key):
    website = input("Enter website: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    encrypted_password = encrypt_password(key, password)

    with sqlite3.connect('password_manager.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)', (website, username, encrypted_password))
        conn.commit()
    print("Password added successfully!")

# Retrieve and decrypt stored passwords
def view_passwords(key):
    with sqlite3.connect('password_manager.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT website, username, password FROM passwords')
        rows = cursor.fetchall()

        for row in rows:
            decrypted_password = decrypt_password(key, row[2])
            print(f"Website: {row[0]}, Username: {row[1]}, Password: {decrypted_password}")

# Main function to handle user input
def main():
    master_password = getpass.getpass("Enter master password: ")
    key = generate_key(master_password)

    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Quit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_password(key)
        elif choice == '2':
            view_passwords(key)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()


# In[ ]:





import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import gnupg
import os
import threading
import time
import subprocess

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize GPG with gnupg home
        self.gpg_home = os.path.expanduser("~/.password_manager_gpg")
        if not os.path.exists(self.gpg_home):
            os.makedirs(self.gpg_home, mode=0o700)
        
        self.gpg = gnupg.GPG(gnupghome=self.gpg_home)
        
        # Dictionary to store passwords and their encrypted versions
        self.password_storage = {}
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Password Manager", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Password entries
        self.entries = []
        self.encrypted_labels = []
        
        for i in range(5):
            row = i + 1
            
            # Label for entry number
            label = ttk.Label(main_frame, text=f"Password {i+1}:", font=("Arial", 10))
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            
            # Password entry frame
            entry_frame = ttk.Frame(main_frame)
            entry_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
            entry_frame.columnconfigure(0, weight=1)
            
            # Password entry
            password_entry = ttk.Entry(entry_frame, show="*", width=30)
            password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
            
            # Bind right-click to decrypt and paste
            password_entry.bind("<Button-3>", lambda e, idx=i: self.on_right_click(e, idx))
            
            self.entries.append(password_entry)
            
            # Create Random Password button
            gen_btn = ttk.Button(
                entry_frame,
                text="Create Random",
                command=lambda idx=i: self.generate_random_password(idx)
            )
            gen_btn.grid(row=0, column=1, padx=5)
            
            # Button frame for encrypt and clipboard
            btn_frame = ttk.Frame(main_frame)
            btn_frame.grid(row=row, column=2, sticky=tk.E, padx=5, pady=5)
            
            # Encrypt button
            encrypt_btn = ttk.Button(
                btn_frame,
                text="Encrypt",
                command=lambda idx=i: self.encrypt_password(idx)
            )
            encrypt_btn.grid(row=0, column=0, padx=2)
            
            # Clipboard button
            clipboard_btn = ttk.Button(
                btn_frame,
                text="Clipboard",
                command=lambda idx=i: self.copy_to_clipboard(idx)
            )
            clipboard_btn.grid(row=0, column=1, padx=2)
            
            # Encrypted label
            encrypted_label = ttk.Label(main_frame, text="Not encrypted", foreground="gray", font=("Arial", 8))
            encrypted_label.grid(row=row+5, column=0, columnspan=3, sticky=tk.W, pady=2)
            self.encrypted_labels.append(encrypted_label)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green", font=("Arial", 9))
        self.status_label.grid(row=11, column=0, columnspan=3, pady=10)
    
    def generate_random_password(self, idx):
        """Generate a random password"""
        # Create a dialog to get password length
        dialog = tk.Toplevel(self.root)
        dialog.title("Password Length")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter password length:").pack(pady=10)
        length_entry = ttk.Entry(dialog, width=10)
        length_entry.pack(pady=5)
        length_entry.focus()
        
        def create_password():
            try:
                length = int(length_entry.get())
                if length < 1:
                    messagebox.showerror("Error", "Length must be at least 1")
                    return
                
                # Generate password with uppercase, lowercase, numbers, and symbols
                characters = string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#"
                password = ''.join(random.choice(characters) for _ in range(length))
                
                # Store the original password
                self.password_storage[idx] = password
                
                # Display as stars
                self.entries[idx].delete(0, tk.END)
                self.entries[idx].insert(0, "*" * length)
                
                self.update_status(f"Password {idx+1} generated ({length} characters)")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        ttk.Button(dialog, text="Generate", command=create_password).pack(pady=10)
    
    def encrypt_password(self, idx):
        """Encrypt the password using GPG"""
        if idx not in self.password_storage:
            messagebox.showerror("Error", "No password to encrypt. Generate one first.")
            return
        
        password = self.password_storage[idx]
        
        # Encrypt with symmetric encryption (no passphrase needed for this app)
        # Using a fixed passphrase for consistency
        encrypted_data = self.gpg.encrypt(
            password,
            recipients=None,
            symmetric='AES256',
            always_trust=True,
            passphrase='password_manager_default_key'
        )
        
        if not encrypted_data.ok:
            messagebox.showerror("Error", f"Encryption failed: {encrypted_data.status}")
            return
        
        encrypted_str = str(encrypted_data)
        self.password_storage[f"{idx}_encrypted"] = encrypted_str
        
        # Update label to show encrypted status
        encrypted_display = encrypted_str[:50] + "..." if len(encrypted_str) > 50 else encrypted_str
        self.encrypted_labels[idx].config(text=f"Encrypted: {encrypted_display}")
        
        self.update_status(f"Password {idx+1} encrypted")
    
    def copy_to_clipboard(self, idx):
        """Copy encrypted password to clipboard"""
        if f"{idx}_encrypted" not in self.password_storage:
            messagebox.showerror("Error", "Password must be encrypted first")
            return
        
        encrypted_str = self.password_storage[f"{idx}_encrypted"]
        pyperclip.copy(encrypted_str)
        
        self.update_status(f"Password {idx+1} encrypted key copied to clipboard")
    
    def on_right_click(self, event, idx):
        """Handle right-click to decrypt and paste from clipboard"""
        # Get encrypted data from clipboard
        try:
            clipboard_data = pyperclip.paste()
        except:
            messagebox.showerror("Error", "Could not read clipboard")
            return
        
        # Decrypt the data using the same passphrase
        decrypted_data = self.gpg.decrypt(
            clipboard_data,
            always_trust=True,
            passphrase='password_manager_default_key'
        )
        
        if not decrypted_data.ok:
            messagebox.showerror("Error", "Decryption failed. Clipboard may not contain valid encrypted data")
            return
        
        password = str(decrypted_data)
        
        # Display as stars
        self.entries[idx].delete(0, tk.END)
        self.entries[idx].insert(0, "*" * len(password))
        
        # Store the decrypted password
        self.password_storage[idx] = password
        
        self.update_status(f"Password {idx+1} decrypted and pasted")
        
        # Start the clipboard replacement process
        self.replace_clipboard_content()
    
    def replace_clipboard_content(self):
        """Replace clipboard with random 264-character strings 5 times"""
        def do_replacement():
            for i in range(5):
                # Generate random string of 264 characters
                random_str = ''.join(
                    random.choice(string.ascii_letters + string.digits + string.punctuation)
                    for _ in range(264)
                )
                pyperclip.copy(random_str)
                time.sleep(0.1)  # Brief delay between replacements
            
            self.update_status("Clipboard sanitized (5 times)")
        
        # Run in a separate thread to not block the GUI
        thread = threading.Thread(target=do_replacement, daemon=True)
        thread.start()
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Ready"))


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()

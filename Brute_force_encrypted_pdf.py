import PyPDF2
import itertools
import string
import concurrent.futures
import tkinter as tk
from tkinter import filedialog


def try_password(file_path, password):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        if pdf_reader.decrypt(password) == 1:
            return password
        else:
            print(f"Attempted password: {password}")
    return None


def brute_force_password(file_path, min_length=1, max_length=8, charset=string.printable, max_workers=None):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        if not pdf_reader.is_encrypted:
            print("PDF is not encrypted.")
            return

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for length in range(min_length, max_length + 1):
                password_tuples = itertools.product(charset, repeat=length)
                passwords = (''.join(password_tuple)
                             for password_tuple in password_tuples)
                results = executor.map(
                    try_password, itertools.repeat(file_path), passwords)

                for result in results:
                    if result:
                        print(f"Password found: {result}")
                        return

                print(f"Brute force attempts for length {length} failed.")

    print("Password not found within specified constraints.")


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    file_path = filedialog.askopenfilename(
        title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])

    if file_path:
        # Adjust 'max_workers' as needed based on your CPU.
        brute_force_password(file_path, max_workers=4)
    else:
        print("No file selected.")


if __name__ == '__main__':
    main()

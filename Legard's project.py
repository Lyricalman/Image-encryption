import cv2
import os
import uuid
from tkinter import Tk, Label, Button, Entry, Text, filedialog, messagebox

# Initialize dictionaries for character-to-ASCII and ASCII-to-character mapping
char_to_ascii = {}
ascii_to_char = {}
for i in range(255):
    char_to_ascii[chr(i)] = i
    ascii_to_char[i] = chr(i)

# Function to hide text in image
def hide_text(image_path, key, text):
    text += "\0"  # Append a null character as the delimiter
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Failed to open or find the image.")
        return
    
    width = image.shape[0]
    height = image.shape[1]
    
    key_length = len(key)
    text_length = len(text)
    text_index = 0

    for i in range(text_length):
        image[text_index, i % width, i % height % 3] = char_to_ascii[text[i]] ^ char_to_ascii[key[i % key_length]]
        text_index += 1

    # Save the modified image with a unique filename
    encrypted_image_path = f"encrypted_{uuid.uuid4().hex}.png"
    cv2.imwrite(encrypted_image_path, image)
    messagebox.showinfo("Success", f"Encryption complete. Image saved as {encrypted_image_path}")

# Function to extract text from the encrypted image
def extract_text(image_path, key):
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Failed to open or find the image.")
        return

    key_length = len(key)
    text = ""

    try:
        for i in range(image.shape[0]):
            char = ascii_to_char[image[i, i % image.shape[1], i % image.shape[2]] ^ char_to_ascii[key[i % key_length]]]
            if char == "\0":
                break
            text += char
    except KeyError:
        return None
    
    return text

# GUI setup
def select_image_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        image_path_entry.delete(0, 'end')
        image_path_entry.insert(0, file_path)

def encrypt():
    image_path = image_path_entry.get()
    key = key_entry.get()
    text = text_entry.get("1.0", 'end-1c')
    if not image_path or not key or not text:
        messagebox.showerror("Error", "Fill in all required fields.")
        return
    hide_text(image_path, key, text)

def decrypt():
    image_path = image_path_entry.get()
    key = key_entry.get()
    if not image_path or not key:
        messagebox.showerror("Error", "Fill in all required fields.")
        return
    decrypted_text = extract_text(image_path, key)
    if decrypted_text is None:
        messagebox.showerror("Error", "Decryption failed. Invalid key.")
    else:
        text_entry.delete("1.0", 'end')
        text_entry.insert("1.0", decrypted_text)

# Main application window
root = Tk()
root.title("Image Steganography")

Label(root, text="Image Path:").grid(row=0, column=0, padx=10, pady=10)
image_path_entry = Entry(root, width=50)
image_path_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_image_file).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Key:").grid(row=1, column=0, padx=10, pady=10)
key_entry = Entry(root, width=50)
key_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Text:").grid(row=2, column=0, padx=10, pady=10)
text_entry = Text(root, width=50, height=10)
text_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

Button(root, text="Encrypt Image", command=encrypt).grid(row=3, column=1, padx=10, pady=10)
Button(root, text="Decrypt Image", command=decrypt).grid(row=3, column=2, padx=10, pady=10)

root.mainloop()

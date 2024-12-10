import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Fungsi koneksi ke database
def create_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# Fungsi untuk menambah buku
def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    year = entry_year.get().strip()

    if not title or not author or not year:
        messagebox.showwarning("Warning", "Semua field harus diisi!")
        return

    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
            cursor.execute(query, (title, author, year))
            connection.commit()
            cursor.close()
            connection.close()
            load_books()
            clear_inputs()
            messagebox.showinfo("Success", "Buku berhasil ditambahkan!")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Fungsi untuk membaca (read) buku yang dipilih
def read_book():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Pilih buku yang ingin dilihat!")
        return

    book_id = treeview.item(selected_item, "values")[0]
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM books WHERE id = %s"
            cursor.execute(query, (book_id,))
            book = cursor.fetchone()
            cursor.close()
            connection.close()
            messagebox.showinfo("Book Details", f"ID: {book[0]}\nJudul: {book[1]}\nPenulis: {book[2]}\nTahun: {book[3]}")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Fungsi untuk mengupdate buku
def update_book():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Pilih buku yang akan diperbarui!")
        return

    book_id = treeview.item(selected_item, "values")[0]
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    year = entry_year.get().strip()

    if not title or not author or not year:
        messagebox.showwarning("Warning", "Semua field harus diisi!")
        return

    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s"
            cursor.execute(query, (title, author, year, book_id))
            connection.commit()
            cursor.close()
            connection.close()
            load_books()
            clear_inputs()
            messagebox.showinfo("Success", "Buku berhasil diperbarui!")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Fungsi untuk menghapus buku
def delete_book():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Pilih buku yang akan dihapus!")
        return

    book_id = treeview.item(selected_item, "values")[0]
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "DELETE FROM books WHERE id = %s"
            cursor.execute(query, (book_id,))
            connection.commit()
            cursor.close()
            connection.close()
            load_books()
            messagebox.showinfo("Success", "Buku berhasil dihapus!")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Fungsi untuk memuat buku
def load_books():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT id, title, author, year FROM books ORDER BY id ASC"
        cursor.execute(query)
        books = cursor.fetchall()
        for row in treeview.get_children():
            treeview.delete(row)
        for book in books:
            treeview.insert("", "end", values=book)
        cursor.close()
        connection.close()

# Fungsi untuk mengosongkan input
def clear_inputs():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year.delete(0, tk.END)

# GUI utama
def main_app():
    global entry_title, entry_author, entry_year, treeview

    main_window = tk.Tk()
    main_window.title("Library Manager")
    main_window.geometry("800x600")

    # Form tambah/update buku
    form_frame = tk.Frame(main_window)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Judul Buku").grid(row=0, column=0, padx=5, pady=5)
    entry_title = tk.Entry(form_frame, width=40)
    entry_title.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Penulis").grid(row=1, column=0, padx=5, pady=5)
    entry_author = tk.Entry(form_frame, width=40)
    entry_author.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Tahun Terbit").grid(row=2, column=0, padx=5, pady=5)
    entry_year = tk.Entry(form_frame, width=20)
    entry_year.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(form_frame, text="Tambahkan Buku", command=add_book).grid(row=3, column=0, pady=10)
    tk.Button(form_frame, text="Perbarui Buku", command=update_book).grid(row=3, column=1, pady=10)

    # Tabel buku
    columns = ("ID", "Judul", "Penulis", "Tahun Terbit")
    treeview = ttk.Treeview(main_window, columns=columns, show="headings", height=15)
    treeview.heading("ID", text="ID")
    treeview.heading("Judul", text="Judul Buku")
    treeview.heading("Penulis", text="Penulis")
    treeview.heading("Tahun Terbit", text="Tahun Terbit")
    treeview.pack(pady=10)

    # Tombol tambahan
    tk.Button(main_window, text="Hapus Buku", command=delete_book).pack(side="left", padx=10)
    tk.Button(main_window, text="Lihat Detail", command=read_book).pack(side="left", padx=10)

    load_books()
    main_window.mainloop()

# Main program
if __name__ == "__main__":
    main_app()

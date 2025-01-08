import streamlit as st
import requests

# Base URL for Flask API
API_BASE_URL = "http://127.0.0.1:5000"

# Function to display all books
def view_books():
    st.subheader("View All Books")
    response = requests.get(f"{API_BASE_URL}/books")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            st.write(f"**Title:** {book['title']}")
            st.write(f"**Author:** {book['author']}")
            st.write(f"**Published Year:** {book.get('published_year', 'N/A')}")
            st.write(f"**Genre:** {book.get('genre', 'N/A')}")
            st.write("---")
    else:
        st.error("Failed to fetch books.")

# Function to add a new book
def add_book():
    st.subheader("Add New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    published_year = st.text_input("Published Year")
    genre = st.text_input("Genre")

    if st.button("Add Book"):
        if title and author:
            book_data = {
                "title": title,
                "author": author,
                "published_year": published_year,
                "genre": genre
            }
            response = requests.post(f"{API_BASE_URL}/books", json=book_data)
            if response.status_code == 201:
                st.success("Book added successfully!")
            else:
                st.error(f"Failed to add book: {response.json().get('error')}")
        else:
            st.error("Title and Author are required fields.")

# Function to update book details
def update_book():
    st.subheader("Update Book Details")
    
    # Input to specify the book to be updated
    book_id = st.text_input("Enter Book ID to Update")
    
    if book_id:
        # Check if the book exists by fetching its details (optional)
        response = requests.get(f"{API_BASE_URL}/books/{book_id}")
        if response.status_code != 200:
            st.error("Book not found!")
            return
        
        # Fields for updating
        title = st.text_input("New Book Title", value=response.json().get("title"))
        author = st.text_input("New Book Author", value=response.json().get("author"))
        published_year = st.text_input("New Published Year", value=response.json().get("published_year", ""))
        genre = st.text_input("New Genre", value=response.json().get("genre", ""))
        
        # Submit the update request
        if st.button("Update Book"):
            updated_data = {
                "title": title,
                "author": author,
                "published_year": published_year,
                "genre": genre
            }

            # Remove any empty fields from the updated data
            updated_data = {key: value for key, value in updated_data.items() if value}

            if updated_data:
                # Send the PUT request to update the book
                response = requests.put(f"{API_BASE_URL}/books/{book_id}", json=updated_data)
                if response.status_code == 200:
                    st.success("Book updated successfully!")
                else:
                    st.error(f"Error: {response.json().get('error')}")
            else:
                st.error("Please fill in at least one field to update.")
    else:
        st.error("Please enter a Book ID to update.")

# Function to delete a book
def delete_book():
    st.subheader("Delete Book")
    book_id = st.text_input("Enter Book ID to Delete")
    
    if st.button("Delete Book") and book_id:
        response = requests.delete(f"{API_BASE_URL}/books/{book_id}")
        if response.status_code == 200:
            st.success("Book deleted successfully!")
        else:
            st.error(f"Failed to delete book: {response.json().get('error')}")

# Main function to define Streamlit app layout
def main():
    st.title("Book Management System")
    
    menu = ["View Books", "Add Book", "Update Book", "Delete Book"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "View Books":
        view_books()
    elif choice == "Add Book":
        add_book()
    elif choice == "Update Book":
        update_book()
    elif choice == "Delete Book":
        delete_book()

if __name__ == "__main__":
    main()

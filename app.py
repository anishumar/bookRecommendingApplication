import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import messagebox``

# Sample dataset
data = {
    'Title': [
        'The Great Gatsby', 'To Kill a Mockingbird', '1984', 
        'Pride and Prejudice', 'The Catcher in the Rye', 'Moby-Dick'
    ],
    'Author': [
        'F. Scott Fitzgerald', 'Harper Lee', 'George Orwell', 
        'Jane Austen', 'J.D. Salinger', 'Herman Melville'
    ],
    'Genre': [
        'Classic, Fiction', 'Classic, Fiction, Drama', 'Dystopian, Fiction', 
        'Classic, Romance', 'Classic, Fiction, Coming-of-Age', 'Classic, Adventure'
    ],
    'Description': [
        'A story of love and obsession in the roaring 1920s.',
        'A tale of racial injustice and childhood innocence.',
        'A dystopian novel about totalitarian surveillance.',
        'A romantic story about societal expectations and personal growth.',
        'The struggles of a teenage boy in a confusing adult world.',
        'A sailor’s epic journey in pursuit of a legendary whale.'
    ]
}

# Create DataFrame
books = pd.DataFrame(data)

# Combine relevant columns for comparison
books['Content'] = books['Genre'] + ' ' + books['Description']

# Recommendation function
def get_recommendations(user_input):
    # Text Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(books['Content'])

    # Vectorize user input
    user_vector = vectorizer.transform([user_input])

    # Calculate similarity
    cosine_sim = cosine_similarity(user_vector, tfidf_matrix)

    # Get top recommendations
    top_indices = cosine_sim[0].argsort()[-5:][::-1]
    recommended_books = books.iloc[top_indices]

    # Prepare the recommendation text
    recommendations = ""
    for i, row in recommended_books.iterrows():
        recommendations += f"Title: {row['Title']}\nAuthor: {row['Author']}\nGenre: {row['Genre']}\nDescription: {row['Description']}\n\n"
    
    return recommendations

# GUI
def recommend_books():
    user_input = entry.get()
    if not user_input.strip():
        messagebox.showwarning("Input Error", "Please enter your preferences!")
        return
    
    recommendations = get_recommendations(user_input)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, recommendations)

# Create the main window
window = tk.Tk()
window.title("Book Recommendation System")
window.geometry("600x600")

# Title Label
title_label = tk.Label(window, text="Book Recommendation System", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# User Input
input_label = tk.Label(window, text="Enter your preferred genres or keywords:")
input_label.pack(pady=5)
entry = tk.Entry(window, width=50)
entry.pack(pady=5)

# Recommend Button
recommend_button = tk.Button(window, text="Get Recommendations", command=recommend_books)
recommend_button.pack(pady=10)

# Result Area
result_label = tk.Label(window, text="Recommended Books:")
result_label.pack(pady=5)
result_text = tk.Text(window, width=70, height=20, wrap="word")
result_text.pack(pady=5)

# Run the GUI
window.mainloop()
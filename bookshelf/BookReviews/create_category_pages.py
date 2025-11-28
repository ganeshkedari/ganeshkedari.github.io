import csv
import os
import re

# Configuration
SOURCE_CSV = 'booklist.csv'
TEMPLATE_FILE = '../BookCategory.html'
OUTPUT_DIR = '../' # Relative to the script location (bookshelf/BookReviews -> bookshelf/)

# Categories and their keywords/quotes
CATEGORIES = {
    'Fiction': {
        'filename': 'Fiction.html',
        'keywords': ['Fiction'],
        'quote': "Fiction is the lie through which we tell the truth. - Albert Camus",
        'title': 'Fiction Collection'
    },
    'Mystery & Thriller': {
        'filename': 'MysteryThriller.html',
        'keywords': ['Mystery', 'Thriller', 'Suspense', 'Crime'],
        'quote': "The mystery of life isn't a problem to solve, but a reality to experience. - Frank Herbert",
        'title': 'Mystery & Thriller Collection'
    },
    'Fantasy': {
        'filename': 'Fantasy.html',
        'keywords': ['Fantasy', 'Mythology', 'Magic', 'Retelling'],
        'quote': "Fantasy is hardly an escape from reality. It's a way of understanding it. - Lloyd Alexander",
        'title': 'Fantasy Collection'
    },
    'Science Fiction': {
        'filename': 'ScienceFiction.html',
        'keywords': ['Science Fiction', 'Sci-Fi', 'Dystopian', 'Space'],
        'quote': "Science fiction is the most important literature in the history of the world, because it's the history of ideas. - Ray Bradbury",
        'title': 'Science Fiction Collection'
    },

    'Historical': {
        'filename': 'Historical.html',
        'keywords': ['Historical', 'History'],
        'quote': "History is a gallery of pictures in which there are few originals and many copies. - Alexis de Tocqueville",
        'title': 'Historical Collection'
    },

    'Biography & Memoir': {
        'filename': 'BiographyMemoir.html',
        'keywords': ['Biography', 'Memoir', 'Autobiography'],
        'quote': "There is properly no history; only biography. - Ralph Waldo Emerson",
        'title': 'Biography & Memoir Collection'
    },
    'Knowledge & Learning': {
        'filename': 'KnowledgeLearning.html',
        'keywords': ['Philosophy', 'Psychology', 'Science', 'Economics', 'Business', 'Finance', 'Strategy'],
        'quote': "An investment in knowledge pays the best interest. - Benjamin Franklin",
        'title': 'Knowledge & Learning Collection'
    },
    'Self-Help & Personal Development': {
        'filename': 'SelfHelp.html',
        'keywords': ['Self-Help', 'Personal Development', 'Productivity', 'Motivation', 'Spirituality', 'Habits'],
        'quote': "What lies behind us and what lies before us are tiny matters compared to what lies within us. - Ralph Waldo Emerson",
        'title': 'Self-Help & Personal Development'
    }
}

def get_book_cover_path(book_name):
    # Simple heuristic to guess cover path, similar to previous scripts
    # Assuming images are in img/BookCovers/ and named somewhat like the book
    # In a real scenario, we might need to check the HTML files, but let's try to derive it or use a placeholder
    # Actually, the best way is to check the HTML file for the book if possible, or just use the book name
    # Let's try to find the HTML file and extract the image path
    
    # Clean book name for filename matching
    clean_name = book_name.replace(' ', '').replace(':', '').replace('&', 'And').replace("'", "").replace(',', '')
    # This is a guess. Let's try to find the actual HTML file in the directory
    return f"img/BookCovers/{clean_name}.jpg" # Default guess

def find_html_file(book_name):
    # Try to find the HTML file for the book in the current directory
    # This is a bit fuzzy because filenames don't always match book names exactly
    # We can use the booklist.csv order or try to match filenames
    
    # Let's list all HTML files
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    # Normalize book name
    norm_name = book_name.lower().replace(' ', '').replace(':', '').replace('&', 'and').replace("'", "").replace(',', '')
    
    for f in files:
        if f.lower().replace('.html', '') == norm_name:
            return f
        # specific overrides or partial matches could go here
        
    # Fallback: try to find a file that contains the book name
    for f in files:
        if norm_name in f.lower().replace('.html', ''):
            return f
            
    return None

def extract_cover_from_html(html_file):
    if not html_file or not os.path.exists(html_file):
        return None
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'<img class="cover-img[^"]*" src="([^"]+)"', content)
        if match:
            src = match.group(1)
            # Fix path: usually ../img/BookCovers/... -> img/BookCovers/...
            return src.replace('../', '')
    return None

def main():
    # Read template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Read books
    books_by_category = {cat: [] for cat in CATEGORIES}
    
    with open(SOURCE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            book_name = row['Book Name'].strip()
            category_str = row['Category']
            tags = row['Book Tags']
            
            # Determine which categories this book belongs to
            # A book can belong to multiple categories
            
            combined_text = (category_str + ' ' + tags).lower()
            
            for cat_name, cat_data in CATEGORIES.items():
                # Check if any keyword matches
                for keyword in cat_data['keywords']:
                    if keyword.lower() in combined_text:
                        # Found a match
                        html_file = find_html_file(book_name)
                        if html_file:
                            cover_img = extract_cover_from_html(html_file) or get_book_cover_path(book_name)
                            
                            book_entry = {
                                'href': f'BookReviews/{html_file}',
                                'img': cover_img,
                                'alt': book_name
                            }
                            
                            # Avoid duplicates
                            if book_entry not in books_by_category[cat_name]:
                                books_by_category[cat_name].append(book_entry)
                        break # Stop checking keywords for this category, move to next category

    # Generate pages
    for cat_name, books in books_by_category.items():
        if not books:
            print(f"Warning: No books found for category '{cat_name}'")
            continue
            
        print(f"Generating {cat_name} ({len(books)} books)...")
        
        cat_data = CATEGORIES[cat_name]
        
        # Prepare JS array
        js_books_array = "const books = [\n"
        for book in books:
            js_books_array += f"      {{ href: '{book['href']}', img: '{book['img']}', alt: '{book['alt'].replace("'", "\\'")}' }},\n"
        js_books_array += "    ];"
        
        # Replace content in template
        new_content = template_content
        
        # Replace Title
        new_content = new_content.replace('<title>Book Category | Geeky Tales</title>', f'<title>{cat_data["title"]} | Geeky Tales</title>')
        
        # Replace Hero H1
        new_content = new_content.replace('<h1>Book Category</h1>', f'<h1>{cat_data["title"]}</h1>')
        
        # Replace Hero Quote
        new_content = new_content.replace('The ruins of time build mansions in eternity - William Blake', cat_data['quote'])
        
        # Replace Inner Header
        # Note: The template currently has "Explore Books" / "Discover our curated collection..."
        # We can customize this or leave it generic. Let's customize it.
        new_content = new_content.replace('<h2>Explore Books</h2>', f'<h2>Explore {cat_name}</h2>')
        
        # Replace JS Data
        # Exact string replacement for safety
        placeholder_str = """    const books = [
      // { href: 'BookReviews/BookName.html', img: 'img/BookCovers/BookCover.jpg', alt: 'Book Title' },
    ];"""
        
        if placeholder_str in new_content:
            new_content = new_content.replace(placeholder_str, js_books_array)
        else:
            print(f"Warning: Could not find placeholder in template for {cat_name}")
            # Fallback to regex if exact match fails (e.g. whitespace differences)
            new_content = re.sub(
                r'const books = \[\s*(//.*)?\s*\];', 
                js_books_array, 
                new_content, 
                flags=re.DOTALL
            )
        
        # Write to file
        output_path = os.path.join(OUTPUT_DIR, cat_data['filename'])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    print("Done!")

if __name__ == "__main__":
    main()

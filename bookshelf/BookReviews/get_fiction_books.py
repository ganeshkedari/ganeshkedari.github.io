import os
import re
from pathlib import Path

def extract_category_from_html(file_path):
    """Extract the category from an HTML book review file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for the category pattern: <p class="h6 mb-0 text-uppercase text-primary">CATEGORY</p>
            match = re.search(r'<p class="h6 mb-0 text-uppercase text-primary">([^<]+)</p>', content)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def get_book_cover_path(html_file):
    """Extract book cover image path from HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for cover image pattern
            match = re.search(r'<img class="cover-img[^"]*" src="([^"]+)"', content)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Error extracting cover from {html_file}: {e}")
    return None

def get_book_title(html_file):
    """Extract book title from HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for title in h1 tag
            match = re.search(r'<h1 class="display-4">([^<]+)</h1>', content)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Error extracting title from {html_file}: {e}")
    return None

def main():
    # Directory containing book review HTML files
    reviews_dir = Path(__file__).parent
    
    fiction_books = []
    
    # Iterate through all HTML files
    for html_file in reviews_dir.glob('*.html'):
        if html_file.name == 'template.html':
            continue
            
        category = extract_category_from_html(html_file)
        
        # Check if category contains "Fiction" (case-insensitive)
        if category and 'fiction' in category.lower():
            title = get_book_title(html_file)
            cover = get_book_cover_path(html_file)
            
            fiction_books.append({
                'file': html_file.name,
                'title': title or html_file.stem,
                'category': category,
                'cover': cover or f'../img/BookCovers/{html_file.stem}.jpg'
            })
    
    # Sort by title
    fiction_books.sort(key=lambda x: x['title'])
    
    # Print results
    print(f"Found {len(fiction_books)} Fiction books:\n")
    print("="*80)
    for book in fiction_books:
        print(f"Title: {book['title']}")
        print(f"File: {book['file']}")
        print(f"Category: {book['category']}")
        print(f"Cover: {book['cover']}")
        print("-"*80)
    
    # Generate JavaScript array for the books
    print("\n\nJavaScript Array:")
    print("const fictionBooks = [")
    for book in fiction_books:
        print(f"    {{ href: 'BookReviews/{book['file']}', img: '{book['cover']}', alt: '{book['title']}' }},")
    print("];")
    
    return fiction_books

if __name__ == "__main__":
    fiction_books = main()
    print(f"\n\nTotal Fiction books: {len(fiction_books)}")

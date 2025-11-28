import os
import re
import glob

reviews_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\BookReviews'
covers_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\img\BookCovers'

def normalize_title(title):
    """Normalize title for matching"""
    return re.sub(r'[^\w\s]', '', title).lower().strip()

def get_available_books():
    """Get all available book HTML files and their details"""
    books = {}
    html_files = glob.glob(os.path.join(reviews_dir, '*.html'))
    
    for html_file in html_files:
        filename = os.path.basename(html_file)
        if filename == 'template.html':
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title
        title_match = re.search(r'<h1 class="display-4">(.*?)</h1>', content)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            norm_title = normalize_title(title)
            
            # Find cover image
            img_match = re.search(r'<img class="cover-img[^"]+" src="\.\.\/img\/BookCovers\/([^"]+)"', content)
            image_file = img_match.group(1) if img_match else None
            
            books[norm_title] = {
                'title': title,
                'filename': filename,
                'image': image_file
            }
    
    return books

def find_image_file(book_title):
    """Find the actual image file for a book title"""
    # Try to find matching image in covers directory
    normalized = normalize_title(book_title)
    
    for file in os.listdir(covers_dir):
        file_normalized = normalize_title(os.path.splitext(file)[0])
        if file_normalized == normalized or normalized in file_normalized:
            return file
    
    return None

def update_similar_books_in_file(filepath, available_books):
    """Update similar books section in a single HTML file"""
    filename = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # Find all similar book blocks
    # Pattern: <div class="d-flex mb-1 me-4" ... book title in h6
    pattern = r'(<div class="d-flex mb-1 me-4"[^>]*>)\s*(<a href=")([^"]*)(">)\s*(<img src=")([^"]*)(")[^>]*>\s*</a>\s*<div class="ms-3">.*?<h6 class="mb-1">\s*<a[^>]* href=")([^"]*)(">)([^<]+)(</a>\s*</h6>)'
    
    def replace_book(match):
        div_open = match.group(1)
        a_href_start = match.group(2)
        old_href1 = match.group(3)
        a_href_end = match.group(4)
        img_src_start = match.group(5)
        old_img_src = match.group(6)
        img_src_end = match.group(7)
        title_href_start = match.group(8)
        old_href2 = match.group(9)
        title_href_end = match.group(10)
        book_title = match.group(11)
        title_close = match.group(12)
        
        # Normalize the book title
        norm_title = normalize_title(book_title)
        
        # Check if this book exists in our available books
        if norm_title in available_books:
            book_info = available_books[norm_title]
            new_href = book_info['filename']
            
            # Get image path
            if book_info['image']:
                new_img = f"../img/BookCovers/{book_info['image']}"
            else:
                # Try to find image
                img_file = find_image_file(book_title)
                if img_file:
                    new_img = f"../img/BookCovers/{img_file}"
                else:
                    new_img = old_img_src  # Keep old if we can't find
            
            # Only update if changed
            if old_href1 != new_href or old_img_src != new_img:
                changes_made.append(f"  Updated '{book_title}': {old_href1} -> {new_href}")
                return f"{div_open}{a_href_start}{new_href}{a_href_end}{img_src_start}{new_img}{img_src_end}</a><div class=\"ms-3\">.*?<h6 class=\"mb-1\">{title_href_start}{new_href}{title_href_end}{book_title}{title_close}"
        
        return match.group(0)
    
    # Use a more robust approach - find and replace each book block individually
    # Split by similar books section
    similar_books_start = content.find('<h3 class="h5 mb-4">Similar Books</h3>')
    if similar_books_start == -1:
        return content, []
    
    # Find the end of similar books section
    similar_books_end = content.find('</main>', similar_books_start)
    if similar_books_end == -1:
        return content, []
    
    similar_section = content[similar_books_start:similar_books_end]
    
    # Find all book titles in similar section
    book_blocks = re.finditer(
        r'<div class="d-flex mb-1 me-4"[^>]*>.*?</div>\s*</div>',
        similar_section,
        re.DOTALL
    )
    
    for block_match in book_blocks:
        block = block_match.group(0)
        
        # Extract book title from this block
        title_match = re.search(r'<h6 class="mb-1">.*?<a[^>]*>([^<]+)</a>', block)
        if not title_match:
            continue
            
        book_title = title_match.group(1).strip()
        norm_title = normalize_title(book_title)
        
        if norm_title in available_books:
            book_info = available_books[norm_title]
            new_href = book_info['filename']
            
            # Get image
            if book_info['image']:
                new_img = f"../img/BookCovers/{book_info['image']}"
            else:
                img_file = find_image_file(book_title)
                new_img = f"../img/BookCovers/{img_file}" if img_file else None
            
            # Update href in anchor tags
            new_block = re.sub(r'<a href="[^"]*">', f'<a href="{new_href}">', block)
            
            # Update image src if we have a new image
            if new_img:
                new_block = re.sub(r'<img src="[^"]*"', f'<img src="{new_img}"', new_block)
            
            if new_block != block:
                content = content.replace(block, new_block)
                changes_made.append(f"  Updated '{book_title}' -> {new_href}")
    
    return content, changes_made

def process_all_files():
    """Process all HTML files one by one"""
    print("Getting available books...")
    available_books = get_available_books()
    print(f"Found {len(available_books)} books in library\n")
    
    html_files = sorted(glob.glob(os.path.join(reviews_dir, '*.html')))
    total_files = 0
    total_updates = 0
    
    for html_file in html_files:
        filename = os.path.basename(html_file)
        if filename == 'template.html':
            continue
            
        print(f"Processing {filename}...")
        
        new_content, changes = update_similar_books_in_file(html_file, available_books)
        
        if changes:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ Saved {len(changes)} changes")
            for change in changes:
                print(change)
            total_updates += len(changes)
        else:
            print("  No changes needed")
        
        total_files += 1
    
    print(f"\n{'='*60}")
    print(f"Summary: Processed {total_files} files, made {total_updates} updates")
    print(f"{'='*60}")

if __name__ == "__main__":
    process_all_files()

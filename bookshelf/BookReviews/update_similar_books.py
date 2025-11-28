import os
import re
import glob

# Configuration
reviews_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\BookReviews'
covers_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\img\BookCovers'

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def normalize_title(title):
    return re.sub(r'[^\w\s]', '', title).lower().strip()

def get_book_map():
    book_map = {}
    
    # Scan HTML files to build the map
    html_files = glob.glob(os.path.join(reviews_dir, '*.html'))
    for html_file in html_files:
        filename = os.path.basename(html_file)
        if filename == 'template.html':
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract Title
        title_match = re.search(r'<h1 class="display-4">(.*?)</h1>', content)
        if title_match:
            title = clean_text(title_match.group(1))
            
            # Extract Cover Image
            # Look for the main cover image
            img_match = re.search(r'<img class="cover-img[^"]+" src="([^"]+)"', content)
            image_src = img_match.group(1) if img_match else ""
            
            # If image_src is relative like "../img/BookCovers/...", extract just the filename
            if image_src:
                image_filename = os.path.basename(image_src)
            else:
                # Fallback: try to find an image with the same name as html
                base_name = os.path.splitext(filename)[0]
                # Check extensions
                for ext in ['.jpg', '.png', '.jpeg']:
                    if os.path.exists(os.path.join(covers_dir, base_name + ext)):
                        image_filename = base_name + ext
                        break
                else:
                    image_filename = ""

            book_map[normalize_title(title)] = {
                "title": title,
                "html_file": filename,
                "image_file": image_filename
            }
            
    return book_map

def log(msg):
    with open("update.log", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def debug_map():
    book_map = get_book_map()
    log("Book Map Keys:")
    for k in sorted(book_map.keys()):
        log(f"'{k}': {book_map[k]['html_file']}")

def update_similar_books():
    # Clear log
    with open("update.log", "w", encoding="utf-8") as f:
        f.write("Starting update...\n")
        
    book_map = get_book_map()
    log(f"Found {len(book_map)} books in the library.")
    
    html_files = glob.glob(os.path.join(reviews_dir, '*.html'))
    for html_file in html_files:
        filename = os.path.basename(html_file)
        if filename == 'template.html':
            continue
            
        log(f"Processing {filename}...")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # ... (rest of the function needs to use log instead of print)
        
        # We need to redefine replace_book_block inside here or pass log to it
        # But replace_book_block is inside update_similar_books in previous version
        # Let's just rewrite the whole function for clarity in this tool call
        
        def replace_book_block(match):
            full_block = match.group(0)
            current_href = match.group(1)
            current_img_src = match.group(2)
            book_title = match.group(3)
            
            norm_title = normalize_title(book_title)
            
            if norm_title in book_map:
                book_info = book_map[norm_title]
                new_href = book_info['html_file']
                
                if book_info['image_file']:
                    new_img_src = f"../img/BookCovers/{book_info['image_file']}"
                else:
                    new_img_src = current_img_src
                
                block_with_new_hrefs = re.sub(r'href="([^"]*)"', f'href="{new_href}"', full_block)
                block_with_new_img = re.sub(r'src="([^"]*)"', f'src="{new_img_src}"', block_with_new_hrefs)
                
                log(f"  Updated '{book_title}' -> {new_href}")
                return block_with_new_img
            else:
                return full_block

        pattern = r'(<div class="d-flex mb-1 me-4" style="min-width: 250px;">\s*<a href="([^"]+)">\s*<img src="([^"]+)"[^>]*>\s*</a>\s*<div class="ms-3">.*?<h6 class="mb-1">\s*<a class="reset-anchor text-dark" href="[^"]+">(.*?)</a>\s*</h6>.*?</div>\s*</div>)'
        
        new_content = re.sub(pattern, replace_book_block, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            log(f"Saved changes to {filename}")
        else:
            log(f"No changes for {filename}")

if __name__ == "__main__":
    debug_map() 
    update_similar_books()

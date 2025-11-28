import os
import re
import glob

reviews_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\BookReviews'

def get_available_books():
    """Get all available book HTML files"""
    books = {}
    html_files = glob.glob(os.path.join(reviews_dir, '*.html'))
    
    for html_file in html_files:
        filename = os.path.basename(html_file)
        if filename == 'template.html':
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title
        title_match = re.search(r'<h1 class="display-4">(.*?)</h1>', content, re.DOTALL)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            
            # Find cover image
            img_match = re.search(r'<img class="cover-img[^"]+" src="\.\.\/img\/BookCovers\/([^"]+)"', content)
            image_file = img_match.group(1) if img_match else None
            
            books[title] = {
                'filename': filename,
                'image': image_file
            }
    
    return books

def verify_page_structure(filepath):
    """Verify that a page has correct structure"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check for essential elements
    if '<header-component></header-component>' not in content:
        issues.append("Missing header component")
    
    if 'class="text-gold"' not in content:
        issues.append("Missing gold color styling")
    
    if 'class="drop-cap"' not in content:
        issues.append("Missing drop-cap styling")
    
    if '<h3 class="h5 mb-4">Similar Books</h3>' not in content:
        issues.append("Missing Similar Books section")
    
    if 'Nunito' not in content or 'Abril Fatface' not in content:
        issues.append("Missing required fonts")
    
    if '../css/style.default.css' not in content:
        issues.append("Missing theme stylesheet")
    
    if 'pageheader.js' not in content:
        issues.append("Missing pageheader script")
    
    return issues

def main():
    print("="*70)
    print("BOOK REVIEW PAGES VERIFICATION")
    print("="*70)
    
    available_books = get_available_books()
    print(f"\nTotal books in library: {len(available_books)}")
    print("\nAvailable books:")
    for i, title in enumerate(sorted(available_books.keys()), 1):
        print(f"  {i:2d}. {title}")
    
    print("\n" + "="*70)
    print("VERIFYING PAGE STRUCTURE")
    print("="*70)
    
    html_files = sorted(glob.glob(os.path.join(reviews_dir, '*.html')))
    total_files = 0
    files_with_issues = 0
    
    for html_file in html_files:
        filename = os.path.basename(html_file)
        if filename == 'template.html':
            continue
        
        issues = verify_page_structure(html_file)
        
        if issues:
            print(f"\n❌ {filename}")
            for issue in issues:
                print(f"   - {issue}")
            files_with_issues += 1
        else:
            print(f"✓ {filename}")
        
        total_files += 1
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total files checked: {total_files}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Files OK: {total_files - files_with_issues}")
    
    if files_with_issues == 0:
        print("\n✓ All pages have correct structure!")
    else:
        print(f"\n⚠ {files_with_issues} pages need attention")
    
    print("="*70)

if __name__ == "__main__":
    main()

import os
import re
from pathlib import Path

# Read categories from CSV
def read_categories():
    """Read and parse categories from categories.csv"""
    categories_file = Path(__file__).parent / "categories.csv"
    with open(categories_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        # Split by comma and clean up spaces
        categories = [cat.strip() for cat in content.split(',')]
    return categories

# Analyze book content and match to category
def match_category(html_content, categories):
    """
    Analyze the book review content and match it to the most appropriate category.
    Uses keywords and context from the book description, tags, and metadata.
    """
    
    # Extract relevant content sections
    content_lower = html_content.lower()
    
    # Category keyword mappings
    category_keywords = {
        'Fiction': ['fiction', 'novel', 'story', 'narrative', 'tale'],
        'Mystery & Thriller': ['mystery', 'thriller', 'suspense', 'detective', 'crime', 'murder', 'investigation', 'secret'],
        'Fantasy': ['fantasy', 'magic', 'mythical', 'dragon', 'wizard', 'enchanted', 'realm', 'quest'],
        'Science Fiction': ['sci-fi', 'science fiction', 'future', 'space', 'alien', 'technology', 'dystopian', 'cyberpunk'],

        'Historical': ['historical', 'history', 'ancient', 'medieval', 'war', 'empire', 'century', 'era'],

        'Biography & Memoir': ['biography', 'memoir', 'autobiography', 'life story', 'personal account'],
        'Knowledge & Learning': ['knowledge', 'learning', 'education', 'guide', 'understanding', 'wisdom', 'insight'],
        'Self-Help & Personal Development': ['self-help', 'personal development', 'habits', 'success', 'productivity', 
                                              'motivation', 'mindset', 'growth', 'improvement', 'psychology', 
                                              'emotional', 'mindful', 'meditation', 'stoic', 'philosophy',
                                              'influence', 'persuasion', 'leadership', 'power', 'attitude']
    }
    
    # Score each category
    scores = {}
    for category in categories:
        score = 0
        keywords = category_keywords.get(category, [])
        
        for keyword in keywords:
            # Count occurrences in different sections with different weights
            # Tags section (highest weight)
            tags_match = re.search(r'<div class="p-4 bg-light rounded mb-5">(.*?)</div>', html_content, re.DOTALL)
            if tags_match and keyword in tags_match.group(1).lower():
                score += 10
            
            # Description section (medium weight)
            desc_match = re.search(r'<div class="book-desc mb-5">(.*?)</div>', html_content, re.DOTALL)
            if desc_match and keyword in desc_match.group(1).lower():
                score += 5
            
            # Meta description (medium weight)
            meta_match = re.search(r'<meta name="description"[^>]*content="([^"]*)"', html_content)
            if meta_match and keyword in meta_match.group(1).lower():
                score += 5
            
            # General content (low weight)
            score += content_lower.count(keyword) * 1
        
        scores[category] = score
    
    # Return category with highest score
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    
    # Default to Fiction if no clear match
    return 'Fiction'

# Update category in HTML file
def update_category_in_html(file_path, new_category):
    """
    Update the category in the HTML file at the specified location.
    Preserves all formatting, CSS, and functionality.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the category using regex
    # Pattern: <p class="h6 mb-0 text-uppercase text-primary">OLD_CATEGORY</p>
    pattern = r'(<p class="h6 mb-0 text-uppercase text-primary">)[^<]+(</p>)'
    
    # Check if pattern exists
    if not re.search(pattern, content):
        print(f"  ⚠️  Warning: Category pattern not found in {file_path.name}")
        return False
    
    # Replace with new category
    updated_content = re.sub(pattern, rf'\1{new_category}\2', content)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True

# Main processing function
def process_all_books():
    """Process all book review HTML files and update categories"""
    
    print("=" * 60)
    print("BOOK CATEGORY UPDATE SCRIPT")
    print("=" * 60)
    
    # Read categories
    categories = read_categories()
    print(f"\n📚 Available Categories: {', '.join(categories)}\n")
    
    # Get all HTML files in the BookReviews directory
    book_reviews_dir = Path(__file__).parent
    html_files = sorted([f for f in book_reviews_dir.glob("*.html") 
                        if f.name not in ['template.html']])
    
    print(f"Found {len(html_files)} book review pages to process\n")
    print("-" * 60)
    
    # Process each file
    results = []
    for html_file in html_files:
        print(f"\n📖 Processing: {html_file.name}")
        
        # Read file content
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract current category
        current_match = re.search(r'<p class="h6 mb-0 text-uppercase text-primary">([^<]+)</p>', content)
        current_category = current_match.group(1) if current_match else "Unknown"
        
        # Determine best matching category
        new_category = match_category(content, categories)
        
        # Update the file
        success = update_category_in_html(html_file, new_category)
        
        if success:
            status = "✅" if current_category != new_category else "✓"
            print(f"  {status} Current: '{current_category}' → New: '{new_category}'")
            results.append({
                'file': html_file.name,
                'old': current_category,
                'new': new_category,
                'changed': current_category != new_category
            })
        else:
            print(f"  ❌ Failed to update")
            results.append({
                'file': html_file.name,
                'old': current_category,
                'new': 'ERROR',
                'changed': False
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {len(results)}")
    print(f"Categories changed: {sum(1 for r in results if r['changed'])}")
    print(f"Categories unchanged: {sum(1 for r in results if not r['changed'] and r['new'] != 'ERROR')}")
    print(f"Errors: {sum(1 for r in results if r['new'] == 'ERROR')}")
    
    # Show changes
    changes = [r for r in results if r['changed']]
    if changes:
        print("\n📝 Changed Categories:")
        for change in changes:
            print(f"  • {change['file']}: '{change['old']}' → '{change['new']}'")
    
    print("\n✅ Category update complete!")
    print("=" * 60)

if __name__ == "__main__":
    process_all_books()

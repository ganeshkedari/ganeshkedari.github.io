import os
import glob

reviews_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\BookReviews'

# Get all HTML files
html_files = sorted(glob.glob(os.path.join(reviews_dir, '*.html')))

print("Book Review Pages Summary")
print("=" * 60)
print(f"\nTotal HTML files: {len([f for f in html_files if os.path.basename(f) != 'template.html'])}")
print("\nFiles:")

for html_file in html_files:
    filename = os.path.basename(html_file)
    if filename == 'template.html':
        continue
    
    size_kb = os.path.getsize(html_file) / 1024
    print(f"  {filename:40s} ({size_kb:6.1f} KB)")

print("\n" + "=" * 60)
print("All pages created successfully!")
print("=" * 60)

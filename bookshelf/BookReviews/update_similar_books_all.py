import csv
import os
import re
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
BOOKLIST_CSV = SCRIPT_DIR / "booklist.csv"
BOOKCOVERS_DIR = SCRIPT_DIR.parent / "img" / "BookCovers"
LOG_FILE = SCRIPT_DIR / "similar_books_update.log"

def log_message(message):
    """Log message to both console and file"""
    print(message)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def clear_log():
    """Clear the log file"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write("=== Similar Books Update Log ===\n\n")

def read_booklist():
    """Read the booklist CSV and return a dictionary"""
    books = {}
    with open(BOOKLIST_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            book_name = row['Book Name'].strip()
            books[book_name] = {
                'author': row['Author'].strip(),
                'category': row['Category'].strip(),
                'similar_books': row['Similar Books'].strip() if row['Similar Books'] else ''
            }
    return books

def get_html_filename(book_name):
    """Convert book name to HTML filename"""
    # Manual mappings for exceptions
    mappings = {
        "101 Essays That Will Change the Way You Think": "101Essays.html",
        "101 Essays": "101Essays.html",
        "Asura: Tale of the Vanquished": "Asura.html",
        "Asura": "Asura.html",
        "How to Win Friends and Influence People": "HowToWinFriends.html",
        "How to Win Friends": "HowToWinFriends.html",
        "Mrutyunjay (मृत्युंजय)": "Mrutyunjay.html",
        "Mrutyunjay": "Mrutyunjay.html",
        "Panipat (पानिपत)": "Panipat.html",
        "Panipat": "Panipat.html",
        "Ravana Raja Rakshasancha": "Ravana.html",
        "The 7 Habits of Highly Effective People": "The7Habits.html",
        "The 7 Habits": "The7Habits.html",
        "The Secret of the Nagas": "Secreateofnagas.html",
        "The Subtle Art of Not Giving a F*ck": "TheSubtleArt.html",
        "Yayati (ययाति)": "Yayati.html",
        "Yayati": "Yayati.html",
        "The Laws of Human Nature": "TheLawsOfHumanNature.html",
        "Thinking, Fast and Slow": "ThinkingFastAndSlow.html",
        "Thinking Fast and Slow": "ThinkingFastAndSlow.html",
        "The 5 AM Club": "The5AMClub.html",
        "The Miracle Morning": "TheMiracleMorning.html",
        "Atomic Habits": "AtomicHabits.html",
        "The Power of Habit": "ThePowerOfHabit.html",
        "The Almanack of Naval Ravikant": "TheAlmanackOfNavalRavikant.html",
        "The Psychology of Money": "ThePsychologyOfMoney.html",
        "The Immortals of Meluha": "TheImmortalsOfMeluha.html",
        "The Oath of the Vayuputras": "TheOathOfTheVayuputras.html",
        "Scion of Ikshvaku": "ScionOfIkshvaku.html",
        "The Alchemist": "TheAlchemist.html",
        "Siddhartha": "Siddhartha.html",
        "Jurassic Park": "JurassicPark.html",
        "Congo": "Congo.html",
        "Amazonia": "Amazonia.html",
        "Excavation": "Excavation.html",
        "Subterranean": "Subterranean.html",
        "Ice Hunt": "IceHunt.html",
        "Deep Fathom": "DeepFathom.html",
        "The Last Templar": "TheLastTemplar.html",
        "The Da Vinci Code": "TheDaVinciCode.html",
        "Angels & Demons": "AngelsAndDemons.html",
        "The Lost City": "TheLostCity.html",
        "The Andromeda Strain": "TheAndromedaStrain.html",
        "Arctic Storm Rising": "ArcticStormRising.html",
        "The Great Zoo of China": "TheGreatZooOfChina.html",
        "Altar of Eden": "AltarOfEden.html"
    }
    
    if book_name in mappings:
        return mappings[book_name]

    # Remove special characters and spaces
    filename = book_name.replace(' ', '')
    filename = filename.replace("'", '')
    filename = filename.replace('"', '')
    filename = filename.replace(',', '')
    filename = filename.replace(':', '')
    filename = filename.replace('&', 'And')
    filename = filename.replace('*', '')
    filename = filename.replace('!', '')
    filename = filename.replace('?', '')
    filename = filename.replace('(', '')
    filename = filename.replace(')', '')
    filename = filename.replace('–', '')
    filename = filename.replace('—', '')
    return filename + '.html'

def get_cover_filename(book_name, author):
    """Get the cover image filename - check multiple variations"""
    # Try different naming conventions
    base_name = book_name.replace(' ', '').replace("'", '').replace('"', '').replace(',', '').replace(':', '').replace('&', 'And').replace('*', '').replace('!', '').replace('?', '').replace('(', '').replace(')', '')
    
    variations = [
        base_name + '.jpg',
        base_name.lower() + '.jpg',
        base_name + '.png',
        base_name.lower() + '.png',
    ]
    
    for var in variations:
        if (BOOKCOVERS_DIR / var).exists():
            return var
    
    # If not found, return expected filename
    return base_name + '.jpg'

def parse_similar_books(similar_books_str):
    """Parse the similar books string into a list of (book, author) tuples"""
    if not similar_books_str:
        return []
    
    # Replace newlines with spaces to handle formatting issues in CSV
    cleaned_str = similar_books_str.replace('\n', ' ')
    
    books = []
    # Split by pipe
    entries = cleaned_str.split('|')
    
    for entry in entries:
        entry = entry.strip()
        if ' - ' in entry:
            parts = entry.split(' - ', 1)
            if len(parts) == 2:
                books.append((parts[0].strip(), parts[1].strip()))
    
    return books

def get_category_for_book(book_name, all_books):
    """Get the primary category for a book"""
    if book_name in all_books:
        category = all_books[book_name]['category']
        # Take first category if multiple
        if '&' in category:
            return category.split('&')[0].strip()
        return category
    return "General"

def check_cover_exists(cover_filename):
    """Check if cover image exists"""
    return (BOOKCOVERS_DIR / cover_filename).exists()

def find_similar_books_section(html_content):
    """Find the Similar Books section in HTML"""
    # Look for the Similar Books section
    pattern = r'(<h3 class="h5 mb-4">Similar Books</h3>.*?<div class="d-flex flex-row overflow-auto pb-3">)(.*?)(</div>\s*</div>\s*</div>)'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        return match.start(2), match.end(2), match.group(2)
    return None, None, None

def generate_similar_book_html(book_name, author, category, html_filename, cover_filename):
    """Generate HTML for a single similar book"""
    # Shorten book name if too long
    display_name = book_name
    if len(book_name) > 30:
        display_name = book_name[:27] + '...'
    
    html = f'''
                                <!-- Similar Book -->
                                <div class="d-flex mb-1 me-4" style="min-width: 250px;">
                                    <a href="{html_filename}">
                                        <img src="../img/BookCovers/{cover_filename}" alt="{book_name} Cover"
                                            class="shadow-sm rounded" width="80" height="120" loading="lazy">
                                    </a>
                                    <div class="ms-3">
                                        <p class="small text-primary text-uppercase mb-0">{category}</p>
                                        <h6 class="mb-1">
                                            <a class="reset-anchor text-dark" href="{html_filename}">{display_name}</a>
                                        </h6>
                                        <p class="small text-muted">{author}</p>
                                    </div>
                                </div>
'''
    return html

def update_book_html(book_name, all_books):
    """Update a single book's HTML file with similar books"""
    html_filename = get_html_filename(book_name)
    html_path = SCRIPT_DIR / html_filename
    
    if not html_path.exists():
        log_message(f"❌ SKIP: {book_name} - HTML file not found: {html_filename}")
        return False
    
    log_message(f"\n📖 Processing: {book_name}")
    log_message(f"   File: {html_filename}")
    
    # Get similar books
    similar_books_str = all_books[book_name]['similar_books']
    similar_books = parse_similar_books(similar_books_str)
    
    if not similar_books:
        log_message(f"   ⚠️  No similar books defined in CSV")
        return False
    
    log_message(f"   Found {len(similar_books)} similar books in CSV")
    
    # Read HTML file
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find Similar Books section
    start_pos, end_pos, old_content = find_similar_books_section(html_content)
    
    if start_pos is None:
        log_message(f"   ❌ Similar Books section not found in HTML")
        return False
    
    # Generate new similar books HTML
    new_books_html = ""
    valid_count = 0
    
    for idx, (sim_book, sim_author) in enumerate(similar_books, 1):
        sim_html_filename = get_html_filename(sim_book)
        sim_html_path = SCRIPT_DIR / sim_html_filename
        
        if not sim_html_path.exists():
            log_message(f"   ⚠️  Similar book #{idx} '{sim_book}' - HTML not found, skipping")
            continue
        
        sim_cover_filename = get_cover_filename(sim_book, sim_author)
        cover_exists = check_cover_exists(sim_cover_filename)
        
        if not cover_exists:
            log_message(f"   ⚠️  Similar book #{idx} '{sim_book}' - Cover missing: {sim_cover_filename}")
        
        sim_category = get_category_for_book(sim_book, all_books)
        
        new_books_html += generate_similar_book_html(
            sim_book, sim_author, sim_category, 
            sim_html_filename, sim_cover_filename
        )
        
        valid_count += 1
        log_message(f"   ✅ Similar book #{idx}: {sim_book} by {sim_author}")
    
    if valid_count == 0:
        log_message(f"   ❌ No valid similar books to add")
        return False
    
    # Replace the content
    new_html_content = html_content[:start_pos] + new_books_html + html_content[end_pos:]
    
    # Write back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    
    log_message(f"   ✅ Updated with {valid_count} similar books")
    return True

def main():
    clear_log()
    log_message("Starting Similar Books Update Process\n")
    log_message(f"Working Directory: {SCRIPT_DIR}")
    log_message(f"BookCovers Directory: {BOOKCOVERS_DIR}\n")
    
    # Read booklist
    log_message("Reading booklist.csv...")
    all_books = read_booklist()
    log_message(f"Found {len(all_books)} books in CSV\n")
    
    # Update each book
    success_count = 0
    skip_count = 0
    
    for book_name in all_books.keys():
        if update_book_html(book_name, all_books):
            success_count += 1
        else:
            skip_count += 1
    
    log_message(f"\n{'='*60}")
    log_message(f"SUMMARY:")
    log_message(f"  ✅ Successfully updated: {success_count} books")
    log_message(f"  ⚠️  Skipped: {skip_count} books")
    log_message(f"  📊 Total processed: {len(all_books)} books")
    log_message(f"{'='*60}\n")
    log_message(f"Log saved to: {LOG_FILE}")

if __name__ == "__main__":
    main()

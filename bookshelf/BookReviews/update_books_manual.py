import os
import re
import glob

reviews_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\BookReviews'
covers_dir = r'c:\Learning\Website\PersonalWebsite\ganeshkedari.github.io\bookshelf\img\BookCovers'

def normalize_title(title):
    """Normalize title for matching"""
    # Remove special characters and convert to lowercase
    return re.sub(r'[^\w\s]', '', title).lower().strip()

def get_html_filename(title):
    """Convert book title to expected HTML filename"""
    # Remove special characters, spaces, and create camelCase
    words = re.sub(r'[^\w\s]', '', title).split()
    if not words:
        return None
    return ''.join(word.capitalize() for word in words) + '.html'

def get_image_filename(title):
    """Find the actual image file for a book"""
    # Try various naming conventions
    base_name = ''.join(re.sub(r'[^\w\s]', '', title).split())
    
    # Check for exact match (case insensitive)
    for file in os.listdir(covers_dir):
        if file.lower().startswith(base_name.lower()):
            return file
    
    return None

def update_congo():
    """Update Congo.html with correct links"""
    filepath = os.path.join(reviews_dir, 'Congo.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update Jurassic Park link
    jp_html = get_html_filename('Jurassic Park')
    if jp_html and os.path.exists(os.path.join(reviews_dir, jp_html)):
        content = re.sub(
            r'(<div class="d-flex mb-1 me-4"[^>]*>\s*<a href=")#("\s*>\s*<img src=")https://placehold\.co/80x120\?text=Book(" alt="Jurassic Park Cover")',
            rf'\1{jp_html}\2../img/BookCovers/JurassicPark.jpg\3',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'(<h6 class="mb-1">\s*<a class="reset-anchor text-dark" href=")#("\s*>Jurassic Park</a>)',
            rf'\1{jp_html}\2',
            content
        )
    
    # Update The Andromeda Strain link
    as_html = get_html_filename('The Andromeda Strain')
    if as_html and os.path.exists(os.path.join(reviews_dir, as_html)):
        content = re.sub(
            r'(<div class="d-flex mb-1 me-4"[^>]*>\s*<a href=")#("\s*>\s*<img src=")https://placehold\.co/80x120\?text=Book("\s*alt="The Andromeda Strain Cover")',
            rf'\1{as_html}\2../img/BookCovers/TheAndromedaStrain.jpg\3',
            content,
            flags=re.DOTALL
        )
        content = re.sub(
            r'(<h6 class="mb-1">\s*<a class="reset-anchor text-dark" href=")#("\s*>The Andromeda Strain</a>)',
            rf'\1{as_html}\2',
            content
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated Congo.html")

def update_amazonia():
    """Update Amazonia.html with correct image paths"""
    filepath = os.path.join(reviews_dir, 'Amazonia.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update Jurassic Park image
    content = re.sub(
        r'(<a href="JurassicPark\.html">\s*<img src=")https://placehold\.co/80x120\?text=Jurassic\+Park(")',
        r'\1../img/BookCovers/JurassicPark.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    # Update Congo image
    content = re.sub(
        r'(<a href="Congo\.html">\s*<img src=")https://placehold\.co/80x120\?text=Congo(")',
        r'\1../img/BookCovers/congo.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    # Update Excavation image
    content = re.sub(
        r'(<a href="Excavation\.html">\s*<img src=")https://placehold\.co/80x120\?text=Excavation(")',
        r'\1../img/BookCovers/Excavation.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated Amazonia.html")

def update_angels_and_demons():
    """Update AngelsAndDemons.html with correct links"""
    filepath = os.path.join(reviews_dir, 'AngelsAndDemons.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update The Da Vinci Code
    content = re.sub(
        r'(<a href=")TheDaVinciCode\.html("\s*>\s*<img src=")https://placehold\.co/80x120\?text=The\+Da\+Vinci\+Code(")',
        r'\1TheDaVinciCode.html\2../img/BookCovers/TheDaVinciCode.jpg\3',
        content,
        flags=re.DOTALL
    )
    
    # Update The Last Templar
    content = re.sub(
        r'(<a href=")TheLastTemplar\.html("\s*>\s*<img src=")https://placehold\.co/80x120\?text=The\+Last\+Templar(")',
        r'\1TheLastTemplar.html\2../img/BookCovers/TheLastTemplar.jpg\3',
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated AngelsAndDemons.html")

def update_how_to_win_friends():
    """Update HowToWinFriends.html with correct links"""
    filepath = os.path.join(reviews_dir, 'HowToWinFriends.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update The 7 Habits image
    content = re.sub(
        r'(<a href="The7Habits\.html">\s*<img src=")https://placehold\.co/80x120\?text=The\+7\+Habits(")',
        r'\1../img/BookCovers/The7Habits.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    # Update Influence image
    content = re.sub(
        r'(<a href="Influence\.html">\s*<img src=")https://placehold\.co/80x120\?text=Influence(")',
        r'\1../img/BookCovers/influence.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    # Update Atomic Habits image
    content = re.sub(
        r'(<a href="AtomicHabits\.html">\s*<img src=")https://placehold\.co/80x120\?text=Atomic\+Habits(")',
        r'\1../img/BookCovers/AtomicHabits.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated HowToWinFriends.html")

def update_arctic_storm_rising():
    """Update ArcticStormRising.html with correct links"""
    filepath = os.path.join(reviews_dir, 'ArcticStormRising.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update Ice Hunt image
    content = re.sub(
        r'(<a href="IceHunt\.html">\s*<img src=")https://placehold\.co/80x120\?text=Ice\+Hunt(")',
        r'\1../img/BookCovers/icehunt.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated ArcticStormRising.html")

def update_jurassic_park():
    """Update JurassicPark.html with correct links"""
    filepath = os.path.join(reviews_dir, 'JurassicPark.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update Congo image
    content = re.sub(
        r'(<a href="Congo\.html">\s*<img src=")https://placehold\.co/80x120\?text=Congo(")',
        r'\1../img/BookCovers/congo.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    # Update Amazonia image
    content = re.sub(
        r'(<a href="Amazonia\.html">\s*<img src=")https://placehold\.co/80x120\?text=Amazonia(")',
        r'\1../img/BookCovers/Amazonia.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated JurassicPark.html")

def update_andromeda_strain():
    """Update TheAndromedaStrain.html with correct links"""
    filepath = os.path.join(reviews_dir, 'TheAndromedaStrain.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update Jurassic Park image
    content = re.sub(
        r'(<a href="JurassicPark\.html">\s*<img src=")https://placehold\.co/80x120\?text=Jurassic\+Park(")',
        r'\1../img/BookCovers/JurassicPark.jpg\2',
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated TheAndromedaStrain.html")

if __name__ == "__main__":
    print("Updating book review pages...")
    update_congo()
    update_amazonia()
    update_angels_and_demons()
    update_how_to_win_friends()
    update_arctic_storm_rising()
    update_jurassic_park()
    update_andromeda_strain()
    print("Done!")

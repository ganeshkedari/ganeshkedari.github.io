import os
from bs4 import BeautifulSoup
import urllib.parse

def check_images():
    base_dir = os.path.abspath("BookReviews")
    # img_dir is relative to the workspace root, but we check existence based on resolved paths
    
    print(f"Scanning directory: {base_dir}")
    
    missing_images = []
    
    files = [f for f in os.listdir(base_dir) if f.endswith(".html")]
    
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        # Check Main Cover
        cover_img = soup.find("img", class_="cover-img")
        if cover_img:
            src = cover_img.get("src")
            check_image(filepath, src, "Main Cover", missing_images)
        else:
            missing_images.append(f"File: {filename} - Main Cover img tag not found")

        # Check Similar Books
        # Strategy: Find the "Similar Books" header and look within that section
        similar_header = soup.find(lambda tag: tag.name == "h3" and "Similar Books" in tag.text)
        if similar_header:
            # The images are in the following div
            container = similar_header.find_next("div")
            if container:
                images = container.find_all("img")
                for img in images:
                    src = img.get("src")
                    check_image(filepath, src, "Similar Book", missing_images)
            else:
                 missing_images.append(f"File: {filename} - Similar Books container not found")
        else:
            # Some pages might not have similar books or different structure
            pass

    with open("report_utf8.txt", "w", encoding="utf-8") as f_out:
        f_out.write("--- Report ---\n")
        if not missing_images:
            f_out.write("No missing images found.\n")
        else:
            for item in missing_images:
                f_out.write(item + "\n")
    print("Report written to report_utf8.txt")

def check_image(html_path, src, img_type, report_list):
    if not src:
        report_list.append(f"File: {os.path.basename(html_path)} - {img_type} has empty src")
        return

    if src.startswith("http") or src.startswith("//"):
        # External image, skip or maybe note it if user wants only local
        # User asked for "Images added in page for book coder does not exists in img\BookCovers folder"
        # So if it's external, it's technically not in the folder, but usually that's intended.
        # However, placehold.co images are placeholders and should probably be noted if the user wants real covers.
        if "placehold.co" in src:
             report_list.append(f"File: {os.path.basename(html_path)} - {img_type} is a placeholder: {src}")
        return

    # Resolve relative path
    # html_path is c:\...\BookReviews\File.html
    # src is usually ../img/BookCovers/file.jpg
    
    html_dir = os.path.dirname(html_path)
    image_path = os.path.normpath(os.path.join(html_dir, src))
    
    if not os.path.exists(image_path):
        report_list.append(f"File: {os.path.basename(html_path)} - {img_type} Missing: {src} (Resolved: {image_path})")

if __name__ == "__main__":
    check_images()

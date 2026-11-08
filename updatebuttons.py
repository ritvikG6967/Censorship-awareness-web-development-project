from bs4 import BeautifulSoup

# Load your sitemap HTML file
with open("site map.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Grab all navigation links
nav_links = soup.select("#navMenu a")

# Grab all buttons with class 'button'
buttons = soup.select("button.button")

# Update button text with nav link text
for btn, link in zip(buttons, nav_links):
    btn.string = link.text  # replace button text with nav link text
    # Optional: also update onclick to match nav link href
    btn["onclick"] = f"window.location.href='{link['href']}'"

# Save changes back to file
with open("site map.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from bs4 import BeautifulSoup
NEW_HEADER_TEXT = "Censorship Awareness"

def add_item_action():
    new_item = entry.get().strip()
    if not new_item:
        messagebox.showerror("Error", "Please enter a menu item.")
        return

    folder = filedialog.askdirectory(title="Select Website Folder")
    if not folder:
        return

    template_path = filedialog.askopenfilename(title="Select Template File", filetypes=[("HTML files", "*.html")])
    if not template_path:
        return

    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
    if not html_files:
        messagebox.showerror("Error", "No HTML files found in the selected folder.")
        return

    # Load template nav
    with open(template_path, "r", encoding="utf-8") as f:
        template_soup = BeautifulSoup(f.read(), "html.parser")

    template_nav = template_soup.find("nav")
    if not template_nav:
        messagebox.showerror("Error", "Template file has no <nav>.")
        return

    nav_soup = BeautifulSoup(str(template_nav), "html.parser")
    nav_clone = nav_soup.find("nav")
    ul = nav_clone.find("ul")
    if ul:
        new_li = nav_soup.new_tag("li")
        new_a = nav_soup.new_tag("a", href=f"{new_item.lower()}.html")
        new_a.string = new_item
        new_li.append(new_a)
        ul.append(new_li)

    consistent_nav_html = str(nav_clone)

    updated_files = []
    progress["maximum"] = len(html_files)
    progress["value"] = 0
    status_log.delete(1.0, tk.END)

    for i, filename in enumerate(html_files, start=1):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            page_soup = BeautifulSoup(f.read(), "html.parser")

        page_nav = page_soup.find("nav")
        if page_nav:
            page_nav.replace_with(BeautifulSoup(consistent_nav_html, "html.parser"))

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(page_soup))

        updated_files.append(filename)
        progress["value"] = i
        status_log.insert(tk.END, f"Updated {filename}\n")
        root.update_idletasks()

    # --- Create new page from full template ---
    new_page_path = os.path.join(folder, f"{new_item.lower()}.html")
    if not os.path.exists(new_page_path):
        with open(template_path, "r", encoding="utf-8") as f:
            new_page_soup = BeautifulSoup(f.read(), "html.parser")

        # Update title
        if new_page_soup.title:
            new_page_soup.title.string = new_item

        # Replace <main> with placeholder content
        main = new_page_soup.find("main")
        if main:
            main.clear()
            h1 = new_page_soup.new_tag("h1")
            h1.string = f"Welcome to {new_item}"
            p = new_page_soup.new_tag("p")
            p.string = "This page was generated from the blank template."
            main.extend([h1, p])

        # Replace nav with consistent nav
        new_nav = new_page_soup.find("nav")
        if new_nav:
            new_nav.replace_with(BeautifulSoup(consistent_nav_html, "html.parser"))

        with open(new_page_path, "w", encoding="utf-8") as f:
            f.write(str(new_page_soup))

        status_log.insert(tk.END, f"Created new page: {os.path.basename(new_page_path)}\n")

    messagebox.showinfo("Success", f"Added '{new_item}', updated {len(updated_files)} pages, and created {new_item.lower()}.html.")

def clean_links_action():
    folder = filedialog.askdirectory(title="Select Website Folder")
    if not folder:
        return

    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
    if not html_files:
        messagebox.showerror("Error", "No HTML files found in the selected folder.")
        return

    removed_total = 0
    progress["maximum"] = len(html_files)
    progress["value"] = 0
    status_log.delete(1.0, tk.END)

    for i, filename in enumerate(html_files, start=1):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            page_soup = BeautifulSoup(f.read(), "html.parser")

        page_nav = page_soup.find("nav")
        removed_count = 0
        if page_nav:
            ul = page_nav.find("ul")
            if ul:
                for li in list(ul.find_all("li")):
                    a = li.find("a")
                    if a and a.has_attr("href"):
                        target_file = os.path.join(folder, a["href"])
                        if not os.path.exists(target_file):
                            li.decompose()
                            removed_count += 1

        removed_total += removed_count
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(page_soup))

        progress["value"] = i
        status_log.insert(tk.END, f"Cleaned {filename} (removed {removed_count} broken links)\n")
        root.update_idletasks()

    messagebox.showinfo("Success", f"Removed {removed_total} broken links across {len(html_files)} pages.")

def sync_nav_action():
    folder = filedialog.askdirectory(title="Select Website Folder")
    if not folder:
        return

    template_path = filedialog.askopenfilename(title="Select Template File", filetypes=[("HTML files", "*.html")])
    if not template_path:
        return

    # Load nav from template
    with open(template_path, "r", encoding="utf-8") as f:
        template_soup = BeautifulSoup(f.read(), "html.parser")

    template_nav = template_soup.find("nav", {"id": "main-menu"})
    if not template_nav:
        messagebox.showerror("Error", "Template file has no <nav id='main-menu'>.")
        return

    consistent_nav_html = str(template_nav)

    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
    updated_files = []
    progress["maximum"] = len(html_files)
    progress["value"] = 0
    status_log.delete(1.0, tk.END)

    for i, filename in enumerate(html_files, start=1):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            page_soup = BeautifulSoup(f.read(), "html.parser")

        page_nav = page_soup.find("nav", {"id": "main-menu"})
        if page_nav:
            page_nav.replace_with(BeautifulSoup(consistent_nav_html, "html.parser"))

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(page_soup))

        updated_files.append(filename)
        progress["value"] = i
        status_log.insert(tk.END, f"Synced nav in {filename}\n")
        root.update_idletasks()

    messagebox.showinfo("Success", f"Synced nav from template across {len(updated_files)} pages.")




def update_headers(folder, new_text):
    updated_files = []
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            file_path = os.path.join(folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")

            header_tag = soup.find("header")
            if header_tag:
                h1_tag = header_tag.find("h1")
                if h1_tag:
                    h1_tag.string = new_text  # update only the text
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(str(soup))
                    updated_files.append(filename)

    return updated_files

def run_update():
    folder = filedialog.askdirectory(title="Select Folder with HTML Files")
    if not folder:
        return

    updated = update_headers(folder, NEW_HEADER_TEXT)
    if updated:
        messagebox.showinfo("Success", f"Updated headers in {len(updated)} files:\n" + "\n".join(updated))
    else:
        messagebox.showwarning("No Updates", "No HTML files with headers were found.")

def sync_footer_action():
    folder = filedialog.askdirectory(title="Select Website Folder")
    if not folder:
        return

    template_path = filedialog.askopenfilename(title="Select Template File", filetypes=[("HTML files", "*.html")])
    if not template_path:
        return

    # Load footer from template
    with open(template_path, "r", encoding="utf-8") as f:
        template_soup = BeautifulSoup(f.read(), "html.parser")

    template_footer = template_soup.find("footer")
    if not template_footer:
        messagebox.showerror("Error", "Template file has no <footer>.")
        return

    consistent_footer_html = str(template_footer)

    html_files = [f for f in os.listdir(folder) if f.endswith(".html")]
    updated_files = []
    progress["maximum"] = len(html_files)
    progress["value"] = 0
    status_log.delete(1.0, tk.END)

    for i, filename in enumerate(html_files, start=1):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            page_soup = BeautifulSoup(f.read(), "html.parser")

        page_footer = page_soup.find("footer")
        if page_footer:
            page_footer.replace_with(BeautifulSoup(consistent_footer_html, "html.parser"))
        else:
            if page_soup.body:
                page_soup.body.append(BeautifulSoup(consistent_footer_html, "html.parser"))
            else:
                page_soup.append(BeautifulSoup(consistent_footer_html, "html.parser"))

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(page_soup))

        updated_files.append(filename)
        progress["value"] = i
        status_log.insert(tk.END, f"Synced footer in {filename}\n")
        root.update_idletasks()

    messagebox.showinfo("Success", f"Synced footer from template across {len(updated_files)} pages.")



def cancel_action():
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Website Menu Manager")

tk.Label(root, text="Enter new menu item:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

progress = ttk.Progressbar(root, orient="horizontal", length=320, mode="determinate")
progress.pack(pady=10)

status_log = tk.Text(root, height=12, width=70)
status_log.pack(pady=10)

btns = tk.Frame(root)
btns.pack(pady=10)
tk.Button(btns, text="Add Item (and Create Page)", command=add_item_action).pack(side="left", padx=10)
tk.Button(btns, text="Clean Broken Links", command=clean_links_action).pack(side="left", padx=10)
tk.Button(btns, text="Sync Nav from Template", command=sync_nav_action).pack(side="left", padx=10)
tk.Button(btns, text="Update site header", command=run_update).pack(side="left", padx=10)
tk.Button(btns, text="Sync Footer from Template", command=sync_footer_action).pack(side="left", padx=10)
tk.Button(btns, text="Cancel", command=cancel_action).pack(side="left", padx=10)


root.mainloop()

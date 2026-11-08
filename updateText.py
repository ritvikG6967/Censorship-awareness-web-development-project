import os

folder_path = 'C:\\Users\\Ricky\\Desktop\\Project ITEC 231 - Copy\\Project ITEC 231'

old_tag = '<header style="background-color: rgb(221, 3, 3);">'
new_tag = '<header>'

for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if old_tag in content:
            content = content.replace(old_tag, new_tag)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {filename}")

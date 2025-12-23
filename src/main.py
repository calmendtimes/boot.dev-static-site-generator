import sys
import os
import shutil
import pathlib
import textnode
import blocktype


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public()
    generate_pages_recursive(basepath, "content", "template.html", "docs")


def copy_static_to_public():
    shutil.rmtree("./docs", ignore_errors=True)
    shutil.copytree("./static", "./docs")


def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for f in files:
            file_path = os.path.join(root, f)
            if file_path[-3:] == ".md":
                path = pathlib.Path(file_path)
                dest_path = pathlib.Path(dest_dir_path) / pathlib.Path(*path.parts[1:]).with_suffix(".html")
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                generate_page(base_path, file_path, template_path, dest_path)    


def generate_page(base_path, from_path, template_path, dest_path):
    print("".join([
        f"Generating page", 
        f"    from: \033[1m{from_path}\033[0m",
        f"    to: \033[1m{dest_path}\033[0m",
        f"    using: \033[1m{template_path}\033[0m"]))
    with open(from_path) as f: markdown = f.read()
    with open(template_path) as f: template = f.read()
    html_node = blocktype.markdown_to_html_node(markdown) 
    content = html_node.to_html()
    title = blocktype.extract_title(markdown)
    page = template \
        .replace("{{ Title }}", title) \
        .replace("{{ Content }}", content) \
        .replace("src=\"/", f"src=\"{base_path}") \
        .replace("href=\"/", f"href=\"{base_path}")
    with open(dest_path, 'w') as f: f.write(page)
    


if __name__ == "__main__":
    main()  
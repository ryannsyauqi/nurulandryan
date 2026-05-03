import os
import re

def get_referenced_files(html_file):
    with open(html_file, 'r') as f:
        content = f.read()
    
    # Simple regex to find paths starting with ./assets/ or assets/
    refs = re.findall(r'[\'"](?:\./)?assets/([^?\'"]+)[\'"]', content)
    return set(refs)

def main():
    base_dir = "/Users/ryansyauqi/Documents/Personal/Wedding Invitation 2"
    assets_dir = os.path.join(base_dir, "assets")
    html_file = os.path.join(base_dir, "index.html")
    
    referenced = get_referenced_files(html_file)
    
    # Also include files referenced in ALL css files
    for root, dirs, files in os.walk(assets_dir):
        for name in files:
            if name.endswith(".css"):
                css_file_path = os.path.join(root, name)
                with open(css_file_path, 'r', errors='ignore') as f:
                    css_content = f.read()
                # Find urls, handling various relative path patterns
                css_refs = re.findall(r'url\([\'"]?(?:\.\./assets/|assets/)?([^?\'"\)]+)[\'"]?\)', css_content)
                for r in css_refs:
                    # Clean up path (sometimes they have multiple ../)
                    clean_r = r.replace('../', '').replace('./', '')
                    referenced.add(clean_r)

    all_files = []
    for root, dirs, files in os.walk(assets_dir):
        for name in files:
            rel_path = os.path.relpath(os.path.join(root, name), assets_dir)
            all_files.append(rel_path)
            
    unused = []
    for f in all_files:
        # Check if file or its directory is referenced
        is_used = False
        if f in referenced:
            is_used = True
        else:
            # Check if any parent path is referenced (e.g. if a dir is used by a script)
            parts = f.split(os.sep)
            for i in range(1, len(parts)):
                if os.path.join(*parts[:i]) in referenced:
                    is_used = True
                    break
        
        if not is_used:
            unused.append(f)
            
    print("Unused files found:", len(unused))
    for u in sorted(unused):
        print(u)

if __name__ == "__main__":
    main()

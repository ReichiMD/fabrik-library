import os
import json
import datetime

# Konfiguration
ROOT_DIR = "."
ASSETS_DIR = "assets"
TEMPLATES_DIR = "templates"
OUTPUT_FILE = "library_index.json"

def scan_directory(base_path):
    file_list = []
    if not os.path.exists(base_path):
        return file_list
        
    for root, _, files in os.walk(base_path):
        for file in files:
            # Ignoriere versteckte Dateien
            if file.startswith("."): continue
            
            # Relativen Pfad berechnen (für die App)
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
            
            file_list.append({
                "path": rel_path,
                "name": file,
                "type": "texture" if file.endswith(".png") else "model" if file.endswith(".json") else "file",
                "category": "vanilla" if "vanilla" in rel_path else "custom"
            })
    return file_list

def main():
    print("🔍 Starte Indexierung...")
    
    data = {
        "meta": {
            "last_update": datetime.datetime.now().isoformat(),
            "version": "1.0"
        },
        "content": []
    }
    
    # Assets scannen
    data["content"].extend(scan_directory(ASSETS_DIR))
    
    # Templates scannen
    data["content"].extend(scan_directory(TEMPLATES_DIR))
    
    # Speichern
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"✅ Index erstellt: {len(data['content'])} Einträge.")

if __name__ == "__main__":
    main()
      

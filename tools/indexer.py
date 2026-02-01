### DATEI: tools/indexer.py
import os
import json
import datetime

# Konfiguration
ROOT_DIR = "."
ASSETS_DIR = "assets"
TEMPLATES_DIR = "templates"
OUTPUT_FILE = "library_index.json"

def scan_directory(base_path):
    """Scannt einen Ordner rekursiv und gibt eine Liste für die App zurück"""
    file_list = []
    if not os.path.exists(base_path):
        return file_list
        
    for root, _, files in os.walk(base_path):
        for file in files:
            # Ignoriere versteckte Dateien (starten mit .)
            if file.startswith("."): continue
            
            # Pfade berechnen
            full_path = os.path.join(root, file)
            # Relativer Pfad für die App (z.B. assets/vanilla/textures/items/apple.png)
            rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
            
            # Typ bestimmen
            ftype = "file"
            if file.endswith(".png") or file.endswith(".jpg"): ftype = "texture"
            elif file.endswith(".json") and "models" in rel_path: ftype = "model"
            elif file.endswith(".json") and "animations" in rel_path: ftype = "animation"
            elif file.endswith(".json"): ftype = "json"
            
            # Kategorie bestimmen
            category = "vanilla" if "vanilla" in rel_path else "custom"
            
            file_list.append({
                "path": rel_path,
                "name": file,
                "type": ftype,
                "category": category
            })
    return file_list

def main():
    print("🔍 Starte Indexierung für Fabrik-App...")
    
    data = {
        "meta": {
            "last_update": datetime.datetime.now().isoformat(),
            "generator": "Fabrik-Indexer V1.0"
        },
        "content": []
    }
    
    # 1. Assets scannen (Icons, Modelle, Animationen)
    print(f"   Scanne {ASSETS_DIR}...")
    assets = scan_directory(ASSETS_DIR)
    data["content"].extend(assets)
    print(f"   -> {len(assets)} Assets gefunden.")
    
    # 2. Templates scannen (Vorlagen)
    print(f"   Scanne {TEMPLATES_DIR}...")
    templates = scan_directory(TEMPLATES_DIR)
    data["content"].extend(templates)
    print(f"   -> {len(templates)} Templates gefunden.")
    
    # 3. Speichern
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"✅ Index erfolgreich erstellt: {OUTPUT_FILE} ({len(data['content'])} Einträge)")

if __name__ == "__main__":
    main()
    

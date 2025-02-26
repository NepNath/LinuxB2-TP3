import os
import json
import logging
import argparse
import hashlib
from datetime import datetime


CONFIG_PATH = "/etc/ids/config.json"
LOG_PATH = "/var/log/ids/ids.log"
HASHES_PATH = "/etc/ids/hashes.json"

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        default_config = {
            "watch_files": ["/etc/passwd", "/var/log/auth.log"], #Liste des fichiers à surveiller
            "log_level": "INFO"
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(default_config, f, indent=4)
        logging.info("Fichier de config créé avec les paramètres par défaut.")
    
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def compute_file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None

def load_hashes():
    if os.path.exists(HASHES_PATH):
        with open(HASHES_PATH, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASHES_PATH, "w") as f:
        json.dump(hashes, f, indent=4)

def check_files(config):
    hashes = load_hashes()
    new_hashes = {}
    
    for file in config.get("watch_files", []):
        current_hash = compute_file_hash(file)
        
        if current_hash is None:
            logging.warning(f"Fichier manquant : {file}")
        else:
            new_hashes[file] = current_hash
            if file in hashes and hashes[file] != current_hash:
                logging.error(f"Fichier {file} modifié.")
            else:
                logging.info(f"Aucune modification détectée pour {file}")
    
    save_hashes(new_hashes)

def main():
    parser = argparse.ArgumentParser(description="IDS de zinzibar pour Linux")
    parser.add_argument("--check", action="store_true", help="Vérifie les fichiers surveillés")
    args = parser.parse_args()
    
    config = load_config()
    logging.info("Démarrage de l'IDS")
    
    if args.check:
        check_files(config)
        logging.info("Vérification des fichiers terminée")
    
if __name__ == "__main__":
    main()

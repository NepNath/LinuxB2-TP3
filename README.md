# IDS - Intrusion Detection System

## 📌 Description
Cet IDS permet de surveiller des fichiers sur votre ordinateur (Linux parce que c'est toujours mieux pour ce genre d'outil) et de détecter si des modifications y sont apportées.
---

## 🛠️ Installation

### **Installation du script**
Copiez le script IDS dans `/usr/local/bin/` et rendez exécutable :
```bash
sudo cp ids.py /usr/local/bin/ids.py
sudo chmod +x /usr/local/bin/ids.py
```

### **Installation des fichiers systemd**
Copiez les fichiers de service et timer :
```bash
sudo cp ids.service /etc/systemd/system/
sudo cp ids.timer /etc/systemd/system/
```
Puis rechargez systemd :
```bash
sudo systemctl daemon-reload
```

### **Activer le service**
Activez et démarrez le timer pour exécuter l'IDS toutes les **10 minutes** (temps modifiable dans le fichier ids.timer" :
```bash
sudo systemctl enable --now ids.timer
```

---

## 🛠️ Configuration
la liste de fichiers à surveiller se trouve dans le fichier principal en python, si vous voulez le modifier, trouvez les lignes suivantes : 
```python
  default_config = {
      "watch_files": ["/etc/passwd", "/var/log/auth.log"],
      "log_level": "INFO"

```
et modifiez la liste "watch_files"

Si le fichier ou le dossier `/etc/ids/` n'existe pas, l'IDS le crée au premier lancement.
---

## 🖥️ Utilisation

### 📖 **Afficher l'aide**
```bash
python3 /usr/local/bin/ids.py --help
```

### 🔍 **Lancer une vérification manuelle**
```bash
sudo systemctl start ids.service
```
---

## 🚮 Désinstallation

### **Désactivez à coup de CTRL + C et supprimez tout les fichies installés**
```bash
sudo systemctl stop ids.timer
sudo systemctl disable ids.timer
sudo rm /etc/systemd/system/ids.service /etc/systemd/system/ids.timer
sudo systemctl daemon-reload
```


# Organiseur de fichiers

Application Windows en Python, sans bibliothèque externe. Elle trie les fichiers placés directement dans le dossier source vers des sous-dossiers par catégorie, dans le dossier principal choisi.

## Démarrage

1. Double-clique sur `Demarrer_organiseur.bat` (Python 3 doit être installé).
2. L’outil trie automatiquement au démarrage. Tu peux modifier les dossiers dans la fenêtre et cliquer sur **Lancer le rangement** pour relancer le tri.

Par défaut, le dossier source est `Téléchargements` (nom de dossier `Downloads`) et la destination est `Fichiers organises` dans ton dossier utilisateur. Les dossiers, les fichiers incomplets et les fichiers à l’intérieur de sous-dossiers ne sont pas touchés. Si un nom existe déjà à destination, l’organiseur ajoute un numéro au nouveau fichier au lieu d’écraser l’ancien.

Les catégories incluent images, vidéos, musique, PDF, documents, tableurs, présentations, archives, programmes, code et autres.

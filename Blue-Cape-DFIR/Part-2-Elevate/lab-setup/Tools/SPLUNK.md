# SPLUNK INSTALLATION 
To install and configure Splunk to our need , you need to go to their 
[website](www.splunk.com/en_us/download/splunk-entrprise.html) and create an account . After that the splunk entrprise download should start . Note that the download size is `1.2 GB` .  
After that move to the folder you downloaded the file and start the installation.

### 1- Install the package 
```bash
sudo dpkg -i splunk*.deb
```
[install_package](photos/install-splunk.png)
You can verify it directly.
[splunk](photos/splunk-here.png)

When did well the installer should give right permissions to the file (user splunk). Verify it with 
```bash
ls -la /opt/splunk/
```
but to be completely sure , you can run 
```bash
sudo chown -R splunk:splunk /opt/splunk
```
To give splunk user full ownership of the folder.

### 2- Start 
Start splunk as `splunk` and accept the free license agreement
```
sudo -u splunk /opt/splunk/bin/splunk start --accept-license
```

Now look at the address, and you will see the link to type in your browser to access  the web view.

### 3- Export
Now that everything is in place you can export the csv downloaded earlier , to do so , follow the steps
- On the first page (Bookmarks page) click `Add data`
- Sur la page suivante, cliquez sur la grande case Upload (Téléverser).
- Étape 3 : Configurer le type de source (Source Type)Une fois le fichier chargé, Splunk va afficher un aperçu de vos données.Splunk devrait détecter automatiquement qu'il s'agit d'un fichier CSV. Vérifiez que la table affichée en bas correspond bien aux colonnes de votre fichier.Si les colonnes ne sont pas bien alignées, regardez sur la gauche dans le menu Delimited settings pour ajuster la virgule ou le point-virgule.Cliquez sur Next (Suivant) en haut à droite.
- Étape 4 : Paramètres d'indexation (Input Settings)C'est une étape importante pour retrouver vos données facilement :Host : Laissez la valeur par défaut ou donnez un nom à la machine d'origine de ce CSV.Index : Par défaut, Splunk envoie les données dans l'index main. Pour un lab, c'est suffisant. Astuce : Vous pouvez aussi cliquer sur "Create a new index" et l'appeler lab_dfir pour garder vos analyses bien isolées.Cliquez sur Review (Revoir) puis sur Submit (Soumettre).
- Étape 5 : Lancer l'analyseL'importation est terminée. Cliquez sur le bouton vert Start Searching.Splunk va vous rediriger vers l'interface de recherche avec une commande pré-remplie qui ressemble à ceci :
```splunk
source="votre_fichier.csv" sourcetype="csv"
```


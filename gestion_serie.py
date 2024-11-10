import mysql.connector
import tkinter as tk
from tkinter import END, messagebox,ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Séries")
        self.geometry("1100x900")
        self.resizable(False,False)
        self.configure(background="lightblue")
        # Connexion à la base de données MySQL
        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="famalysene",
                database="serie"
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur de connexion", f"Erreur : {err}")
            self.quit()

        
        self.container = tk.Frame(self) 
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        
        self.frames = {}

        # Création et ajout des pages
        for F in (PageAcceuil, SeriesPage, EpisodesPage, ImagesPage,CaracteresPage,CategoriesPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self, db=self.db)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Afficher la page d'accueil
        self.show_frame("PageAcceuil")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class PageAcceuil(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller

        # Cadre intermédiaire pour centrer les widgets
        acceuil_frame = tk.Frame(self)
        acceuil_frame.pack(expand=True)  # `expand=True` pour centrer dans la fenêtre principale

        # Titre centré
        label = tk.Label(acceuil_frame, text="Gestion des Séries", font=("Arial", 16,"bold"))
        label.pack(pady=10)

        # Boutons de navigation, ajoutés dans le cadre centré
        bouton_series = tk.Button(acceuil_frame, text="Gestion des Séries", command=lambda: controller.show_frame("SeriesPage"), bg="lightblue", fg="black", width=25)
        bouton_series.pack(pady=5)

        bouton_episodes = tk.Button(acceuil_frame, text="Gestion des Épisodes", command=lambda: controller.show_frame("EpisodesPage"), bg="lightblue", fg="black", width=25)
        bouton_episodes.pack(pady=5)

        bouton_images = tk.Button(acceuil_frame, text="Gestion des Images", command=lambda: controller.show_frame("ImagesPage"), bg="lightblue", fg="black", width=25)
        bouton_images.pack(pady=5)

        bouton_categories = tk.Button(acceuil_frame, text="Gestion des Catégories", command=lambda: controller.show_frame("CategoriesPage"), bg="lightblue", fg="black", width=25)
        bouton_categories.pack(pady=5)

        bouton_characters = tk.Button(acceuil_frame, text="Gestion des Caractères", command=lambda: controller.show_frame("CaracteresPage"), bg="lightblue", fg="black", width=25)
        bouton_characters.pack(pady=5)

class SeriesPage(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.cursor = db.cursor()

 
        serie_frame = tk.Frame(self)
        serie_frame.pack(expand=True, padx=20, pady=20)

        label = tk.Label(serie_frame, text="Gestion des Séries", font=("Arial", 16, "bold"))
        label.grid(row=0, column=0, pady=(0, 20))


        tk.Label(serie_frame, text="Titre de la série", font=("Arial", 13)).grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.titre_entry = tk.Entry(serie_frame, width=30)
        self.titre_entry.grid(row=2, column=0, pady=(0, 15), sticky="ew")

        tk.Label(serie_frame, text="Date Publication", font=("Arial", 13)).grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.date_entry = tk.Entry(serie_frame, width=30)
        self.date_entry.grid(row=4, column=0, pady=(0, 15), sticky="ew")

        tk.Label(serie_frame, text="Genre", font=("Arial", 13)).grid(row=5, column=0, sticky="w", pady=(0, 5))
        self.genre_entry = tk.Entry(serie_frame, width=30)
        self.genre_entry.grid(row=6, column=0, pady=(0, 15), sticky="ew")
        
        tk.Label(serie_frame, text="Langue", font=("Arial", 13)).grid(row=7, column=0, sticky="w", pady=(0, 5))
        self.Langue_entry = tk.Entry(serie_frame, width=30)
        self.Langue_entry.grid(row=8, column=0, pady=(0, 15), sticky="ew")

        tk.Label(serie_frame, text="Catégorie de Série", font=("Arial", 13)).grid(row=9, column=0, sticky="w", pady=(0, 5))
        self.cat=tk.StringVar()
        self.categorie_entry = ttk.Combobox(serie_frame, textvariable=self.cat, width=27)
        self.categorie_entry.grid(row=10, column=0, pady=(0, 15), sticky="ew")
        self.chargement_categorie()
        tk.Label(serie_frame, text="Maison de Production", font=("Arial", 13)).grid(row=11, column=0, sticky="w", pady=(0, 5))
        self.Maison_pro_entry = tk.Entry(serie_frame, width=30)
        self.Maison_pro_entry.grid(row=12, column=0, pady=(0, 15), sticky="ew")

        tk.Label(serie_frame, text="Description", font=("Arial", 13)).grid(row=13, column=0, sticky="w", pady=(0, 5))
        self.description_entry = tk.Text(serie_frame, height=3, width=40)
        self.description_entry.grid(row=14, column=0, pady=(0, 30), sticky="ew")

        buttons_frame = tk.Frame(serie_frame)
        buttons_frame.grid(row=15, column=0, pady=(10, 0))

        add_button = tk.Button(buttons_frame, text="Ajouter la série", command=self.ajout_series, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)
        add_button = tk.Button(buttons_frame, text="supprimer serie", command=self.supp_series, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)
        add_button = tk.Button(buttons_frame, text="voir les series", command=self.selectionner_series, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)

        back_button = tk.Button(buttons_frame, text="Retour à l'accueil", command=lambda: controller.show_frame("PageAcceuil"), bg="lightblue", fg="black")
        back_button.pack(side="left", padx=5)

    def selectionner_series(self):
        sql = "SELECT * FROM series"
        self.cursor.execute(sql)
        series = self.cursor.fetchall()
        # Afficher les résultats dans la fenêtre 
        result = "\n".join([f"{serie[0]}: {serie[1]}" for serie in series])
        messagebox.showinfo("Liste des Séries", result)

    def supp_series(self):
        if self.titre_entry.get()=="": 
           messagebox.showerror("Erreur","Entrez d'abord le titre du serie à supprimer",)
        else:
            titre = self.titre_entry.get()
            sql = "DELETE FROM series WHERE titre = %s"
            self.cursor.execute(sql, (titre,))
            self.db.commit()
            messagebox.showinfo("Succès", "Série supprimée avec succès !") 

    def chargement_categorie(self):
        try:
            self.cursor.execute("SELECT categorie FROM series")
            categorie = [row[0] for row in self.cursor.fetchall()]
            self.categorie_entry['values'] = categorie
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur de chargement des categories : {err}")

    def ajout_series(self):
       if self.titre_entry.get()=="" or self.description_entry.get("1.0", "end-1c")=="" or self.date_entry.get()=="" or self.genre_entry.get()=="" or self.Langue_entry.get()=="" or self.categorie_entry.get()=="" or self.Maison_pro_entry.get()=="": 
          messagebox.showerror("Erreur","Remplissez tous les champs")
       else:
            titre = self.titre_entry.get()
            description = self.description_entry.get("1.0", "end-1c")
            date = self.date_entry.get()
            genre = self.genre_entry.get()
            Langue = self.Langue_entry.get()
            categorie = self.categorie_entry.get()
            Maison_pro = self.Maison_pro_entry.get()

            sql = "INSERT INTO series (titre, description_serie, date_publication, langue, genre, categorie, maison_production) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (titre, description, date, Langue, genre, categorie, Maison_pro))
            self.db.commit()
            messagebox.showinfo("Succès", "Série ajoutée avec succès !")
           

class EpisodesPage(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.cursor = db.cursor()

        # Cadre principal pour contenir tous les éléments et les centrer
        epidode_frame = tk.Frame(self)
        epidode_frame.pack(expand=True, padx=30, pady=20)  # `expand=True` permet de centrer le cadre dans la fenêtre

        label = tk.Label(epidode_frame, text="Gestion des Episodes", font=("Arial", 16, "bold"))
        label.grid(row=0, column=0, pady=(0, 20))

        # Nom de la série
        tk.Label(epidode_frame, text="Nom de la série", font=("Arial", 13), bg="#F0F0F0").grid(row=1, column=0, sticky="w", pady=(0, 5))
        self.series_name_var = tk.StringVar()
        self.series_combobox = ttk.Combobox(epidode_frame, textvariable=self.series_name_var, width=27)
        self.series_combobox.grid(row=2, column=0, pady=(0,15), sticky="ew")
        self.chargement_serie()
        tk.Label(epidode_frame, text="Titre de l'épisode", font=("Arial", 13), bg="#F0F0F0").grid(row=3, column=0, sticky="w", pady=(0, 5))
        self.titre_episode = tk.Entry(epidode_frame, width=30)
        self.titre_episode.grid(row=4, column=0, pady=(0, 15), sticky="ew")

        # Saison
        tk.Label(epidode_frame, text="Saison", font=("Arial", 13), bg="#F0F0F0").grid(row=5, column=0, sticky="w", pady=(0, 5))
        self.saison_de_episode = tk.Entry(epidode_frame, width=30)
        self.saison_de_episode.grid(row=6, column=0, pady=(0, 15), sticky="ew")

        # Épisode
        tk.Label(epidode_frame, text="Épisode", font=("Arial", 13), bg="#F0F0F0").grid(row=7, column=0, sticky="w", pady=(0, 5))
        self.episode_entry = tk.Entry(epidode_frame, width=30)
        self.episode_entry.grid(row=8, column=0, pady=(0, 15), sticky="ew")

        # Date de publication
        tk.Label(epidode_frame, text="Date de publication", font=("Arial", 13), bg="#F0F0F0").grid(row=9, column=0, sticky="w", pady=(0, 5))
        self.publication_date_entry = tk.Entry(epidode_frame, width=30)
        self.publication_date_entry.grid(row=10, column=0, pady=(0, 15), sticky="ew")


        # Buttons aligned horizontally
        buttons_frame = tk.Frame(epidode_frame, bg="#F0F0F0")
        buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky="ew")

        add_button = tk.Button(buttons_frame, text="Ajouter l'épisode", command=self.ajout_episode, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)

        delete_button = tk.Button(buttons_frame, text="Supprimer l'épisode", command=self.supp_episode, bg="lightblue", fg="black")
        delete_button.pack(side="left", padx=5)

        view_button = tk.Button(buttons_frame, text="Voir les épisodes", command=self.select_episode, bg="lightblue", fg="black")
        view_button.pack(side="left", padx=5)

        back_button = tk.Button(buttons_frame, text="Retour à l'accueil",command=lambda: controller.show_frame("PageAcceuil"), bg="lightblue", fg="black")
        back_button.pack(side="left", padx=5)

    

    def supp_episode(self):
        if self.titre_episode.get()=="": 
           messagebox.showerror("Erreur","Entrez d'abord le titre de l'Episode à supprimer ou son Id dans le champs Titre episode",)
        else:
          title = self.titre_episode.get()
          sql = "DELETE FROM episodes WHERE titre_episode = %s or id_episode=%s"
          self.cursor.execute(sql, (title,self.titre_episode.get()))
          self.db.commit()
          messagebox.showinfo("Succès", "Épisode supprimé avec succès !")

    def select_episode(self):
        sql = "SELECT * FROM episodes"
        self.cursor.execute(sql)
        episodes = self.cursor.fetchall()
        result = "\n".join([f"{episode[0]}: {episode[2]}" for episode in episodes])
        messagebox.showinfo("Liste des Épisodes", result)  

    def chargement_serie(self):
        try:
            self.cursor.execute("SELECT titre FROM series")
            series_names = [row[0] for row in self.cursor.fetchall()]
            self.series_combobox['values'] = series_names
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur de chargement des séries : {err}")

    def ajout_episode(self):
      if self.titre_episode.get()=="" or self.series_name_var.get()=="" or self.saison_de_episode.get()=="" or self.episode_entry.get()=="" or self.publication_date_entry.get()=="": 
          messagebox.showerror("Erreur","Remplissez tous les champs")
      else:
        series_name = self.series_name_var.get()
        title = self.titre_episode.get()
        saison = self.saison_de_episode.get()
        episode_number = self.episode_entry.get()
        date_diffusion = self.publication_date_entry.get()

        try:
            self.cursor.execute("SELECT id_series FROM series WHERE titre = %s", (series_name,))
            series_id = self.cursor.fetchone()[0]
            self.cursor.execute(
                "INSERT INTO episodes (id_series, titre_episode, season, numero, date_diffusion) "
                "VALUES (%s, %s, %s, %s, %s)",
                (series_id, title, saison, episode_number, date_diffusion)
            )
            self.db.commit()
            messagebox.showinfo("Succès", "Épisode ajouté avec succès.")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'épisode : {err}")
 
    
        
class ImagesPage(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.cursor = db.cursor()

        # Cadre central pour les widgets
        image_frame = tk.Frame(self)
        image_frame.pack(expand=True, padx=30, pady=20)

        label = tk.Label(image_frame, text="Gestion des Images", font=("Arial", 16, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # ID de la série
        tk.Label(image_frame, text="ID de la série", font=("Arial", 13)).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.series_name_var = tk.StringVar()
        self.series_id_entry =  ttk.Combobox(image_frame, textvariable=self.series_name_var, width=30)
        self.series_id_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        self.chargement_serie()
        # URL de l'image
        tk.Label(image_frame, text="URL de l'image", font=("Arial", 13)).grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.image_url_entry = tk.Entry(image_frame, width=30)
        self.image_url_entry.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # Description
        tk.Label(image_frame, text="Description", font=("Arial", 13)).grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.Description_image_entry = tk.Entry(image_frame, width=30)
        self.Description_image_entry.grid(row=6, column=0, columnspan=2, pady=(0, 20))

        # Boutons alignés sur la même ligne
        add_button = tk.Button(image_frame, text="Ajouter l'image", command=self.ajout_image, bg="lightblue", fg="black")
        add_button.grid(row=7, column=0, pady=(10, 0), padx=5)

        select_button = tk.Button(image_frame, text="Sélectionner une image", command=self.selectionner_image, bg="lightblue", fg="black")
        select_button.grid(row=7, column=1, pady=(10, 0), padx=5)

        display_button = tk.Button(image_frame, text="Afficher les images", command=self.display_images, bg="lightblue", fg="black")
        display_button.grid(row=7, column=2, pady=(10, 0), padx=5)

        delete_button = tk.Button(image_frame, text="Supprimer l'image", command=self.sup_image, bg="lightblue", fg="black")
        delete_button.grid(row=7, column=3, pady=(10, 0), padx=5)
        delete_button = tk.Button(image_frame, text="Retour à l'accueil",command=lambda: controller.show_frame("PageAcceuil"), bg="lightblue", fg="black")
        delete_button.grid(row=7, column=4, pady=(10, 0), padx=5)

        # Label pour l'affichage de l'image en dessous des boutons
        self.image_label = tk.Label(image_frame)
        self.image_label.grid(row=8, column=0, columnspan=4, pady=10)
    
    def chargement_serie(self):
        try:
            self.cursor.execute("SELECT titre FROM series")
            series_names = [row[0] for row in self.cursor.fetchall()]
            self.series_id_entry['values'] = series_names
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur de chargement des séries : {err}")

    def ajout_image(self):
        if (self.image_url_entry.get() == "" or self.Description_image_entry.get() == "" or self.series_id_entry.get() == ""):
            messagebox.showerror("Erreur", "Remplissez tous les champs")
        else:
            # Récupérer les valeurs des champs
            image_url = self.image_url_entry.get()
            description = self.Description_image_entry.get()
            series_id = self.series_id_entry.get()

            # Ajouter l'image à la base de données
            try:
                self.cursor.execute("SELECT id_series FROM series WHERE titre = %s", (series_id,))
                series_id = self.cursor.fetchone()[0]
                self.cursor.execute(
                    "INSERT INTO images (id_series, url, descriptions) VALUES (%s, %s, %s)",
                    (series_id, image_url, description)
                )
                self.db.commit()
                messagebox.showinfo("Succès", "Image ajoutée avec succès !")
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'image: {err}")

    def selectionner_image(self):
        # Ouvrir une boîte de dialogue pour sélectionner une image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])

        if file_path:
            # Vérifier si le fichier existe
            if os.path.exists(file_path):
                # Charger l'image avec Pillow
                try:
                    img = Image.open(file_path)
                    img = img.resize((200, 200))  # Redimensionner l'image si nécessaire

                    # Convertir l'image en format compatible avec Tkinter
                    img_tk = ImageTk.PhotoImage(img)

                    # Afficher l'image dans le label
                    self.image_label.config(image=img_tk)
                    self.image_label.image = img_tk  # Garder une référence à l'image pour éviter que l'image disparaisse
                except Exception as e:
                    print(f"Erreur lors du chargement de l'image: {e}")
            else:
                print("Le fichier n'existe pas ou ne peut pas être ouvert.")

    def display_images(self):
        # Récupérer les images associées à la série à partir de la base de données
        series_id = self.series_id_entry.get()

        if series_id:
            try:
                self.cursor.execute("SELECT url FROM images WHERE id_series = %s", (series_id,))
                images = self.cursor.fetchall()

                if images:
                    for image in images:
                        image_url = image[0]
                        self.display_image_from_url(image_url)
                else:
                    messagebox.showerror("Erreur","Aucune image trouvée pour cette série.")
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur",f"Erreur lors de l'affichage des images: {err}")
        else:
            messagebox.showinfo("Succès","Veuillez entrer un ID de série.")

    def display_image_from_url(self, image_url):
        if os.path.exists(image_url):
            try:
                img = Image.open(image_url)
                img = img.resize((200, 200))

                img_tk = ImageTk.PhotoImage(img)
                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk
            except Exception as e:
                messagebox.showerror("Erreur","Erreur lors de l'affichage de l'image: {e}")
        else:
            messagebox.showerror("Erreur","Le fichier n'existe pas ou ne peut pas être ouvert.")

    def sup_image(self):

        series_id = self.series_id_entry.get()
        image_url = self.image_url_entry.get()

        if series_id and image_url:
            try:
                self.cursor.execute("DELETE FROM images WHERE id_series = %s AND url = %s", (series_id, image_url))
                self.db.commit()
                messagebox.showinfo("Succès", "Image supprimée avec succès !")
                self.image_label.config(image="") 
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression de l'image: {err}")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer un ID de série et une URL d'image valide pour supprimer.")
    




class CategoriesPage(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.cursor = db.cursor()

        center_frame = tk.Frame(self)
        center_frame.pack(expand=True, padx=20, pady=20)

        label = tk.Label(center_frame, text="Catégorie de Série", font=("Arial", 16,"bold"))
        label.grid(row=0, column=0, pady=(0, 20))

        tk.Label(center_frame, text="Catégorie", font=("Arial", 13)).grid(row=1, column=0, sticky="w")
        
        self.Categorie_entry = tk.Entry(center_frame, width=30)
        self.Categorie_entry.grid(row=2, column=0, pady=(0, 20), sticky="ew")

        # Boutons alignés horizontalement
        buttons_frame = tk.Frame(center_frame)
        buttons_frame.grid(row=3, column=0, pady=(10, 0))

        add_button = tk.Button(buttons_frame, text="Ajouter Catégorie", command=self.add_categorie, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)
        add_button = tk.Button(buttons_frame, text="Afficher Catégorie", command=self.voir_categorie, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)
        add_button = tk.Button(buttons_frame, text="supprimer Catégorie", command=self.sup_categorie, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)

        back_button = tk.Button(buttons_frame, text="Retour à l'accueil", command=lambda: controller.show_frame("PageAcceuil"), bg="lightblue", fg="black")
        back_button.pack(side="left", padx=5)
    
    

    def add_categorie(self):
        if self.Categorie_entry.get()=="": 
          messagebox.showerror("Erreur","Remplissez tous les champs")
        else:
          Categorie = self.Categorie_entry.get()
          sql = "INSERT INTO categories (categorie) VALUES (%s)"
          self.cursor.execute(sql, (Categorie,))
          self.db.commit()
          messagebox.showinfo("Succès", "Catégorie ajoutée avec succès !")
    def voir_categorie(self):
        # Affiche toutes les catégories de la base de données
        try:
            self.cursor.execute("SELECT categorie FROM categories")
            categories = self.cursor.fetchall()

            if categories:
                categories_text = "\n".join([cat[0] for cat in categories])
                messagebox.showinfo("Catégories", categories_text)
            else:
                messagebox.showinfo("Catégories", "Aucune catégorie trouvée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des catégories: {e}")

    def sup_categorie(self):
        if self.Categorie_entry.get()=="": 
          messagebox.showerror("Erreur","Remplissez tous les champs")
        else:
           categorie = self.Categorie_entry.get()
           if categorie:
               try:
                   sql = "DELETE FROM categories WHERE categorie = %s"
                   self.cursor.execute(sql, (categorie,))
                   self.db.commit()

                   if self.cursor.rowcount > 0:
                       messagebox.showinfo("Succès", "Catégorie supprimée avec succès !")
                   else:
                       messagebox.showinfo("Info", "Catégorie non trouvée.")
               except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression de la catégorie: {e}")
           else:
               messagebox.showerror("Erreur", "Veuillez entrer la catégorie à supprimer.")



class CaracteresPage(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.cursor = db.cursor()

        # Conteneur central pour centrer tous les widgets
        caractere_frame = tk.Frame(self)
        caractere_frame.pack(expand=True, padx=20, pady=20)

        # Titre de la page
        label = tk.Label(caractere_frame, text="Caractères des Personnages", font=("Arial", 16, "bold"))
        label.grid(row=0, column=0, pady=(0, 20))

        # Champs avec labels au-dessus
        tk.Label(caractere_frame, text="ID Série", font=("Arial", 13)).grid(row=1, column=0, sticky="w")
        self.series_name_var = tk.StringVar()
        self.ID_Serie_entry = ttk.Combobox(caractere_frame, textvariable=self.series_name_var, width=30)
        self.ID_Serie_entry.grid(row=2, column=0, pady=(0, 10))
        self.chargement_serie()
        
        tk.Label(caractere_frame, text="Nom Personnage", font=("Arial", 13)).grid(row=3, column=0, sticky="w")
        self.Nom_Perso_entry = tk.Entry(caractere_frame, width=30)
        self.Nom_Perso_entry.grid(row=4, column=0, pady=(0, 10))

        tk.Label(caractere_frame, text="Rôles", font=("Arial", 13)).grid(row=5, column=0, sticky="w")
        self.Roles_entry = tk.Entry(caractere_frame, width=30)
        self.Roles_entry.grid(row=6, column=0, pady=(0, 10))

        tk.Label(caractere_frame, text="Description du Personnage", font=("Arial", 13)).grid(row=7, column=0, sticky="w")
        self.DescriptionPerso_entry = tk.Entry(caractere_frame, width=30)
        self.DescriptionPerso_entry.grid(row=8, column=0, pady=(0, 20))

        # Boutons alignés horizontalement
        buttons_frame = tk.Frame(caractere_frame)
        buttons_frame.grid(row=9, column=0, pady=(10, 0))

        add_button = tk.Button(buttons_frame, text="Ajouter Caractère", command=self.ajout_caractere, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)
        add_button = tk.Button(buttons_frame, text="Afficher Caractère", command=self.voir_caractere, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)
        add_button = tk.Button(buttons_frame, text="supprimer Caractère", command=self.sup_caractere, bg="lightblue", fg="black")
        add_button.pack(side="left", padx=5)

        back_button = tk.Button(buttons_frame, text="Retour à l'accueil", command=lambda: controller.show_frame("PageAcceuil"), bg="lightblue", fg="black")
        back_button.pack(side="left", padx=5)
    
    def chargement_serie(self):
        try:
            self.cursor.execute("SELECT titre FROM series")
            series_names = [row[0] for row in self.cursor.fetchall()]
            self.ID_Serie_entry['values'] = series_names
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur de chargement des séries : {err}")

    def voir_caractere(self):
        id_serie = self.ID_Serie_entry.get()
        
        if id_serie:
            try:
                self.cursor.execute("SELECT id_series FROM series WHERE titre = %s", (id_serie,))
                series_id = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT nom_caractere, roles FROM caractere WHERE id_series = %s", (series_id,))
                personnages = self.cursor.fetchall()

                if personnages:
                    # Formatage des données pour affichage
                    persos_text = "\n".join([f"{nom} - {role}" for nom, role in personnages])
                    messagebox.showinfo("Personnages", persos_text)
                else:
                    messagebox.showinfo("Personnages", "Aucun personnage trouvé pour cette série.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'affichage des personnages: {e}")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer le nom de la série d'abord.")

    def sup_caractere(self):
        nom_personnage = self.Nom_Perso_entry.get()
        
        if nom_personnage:
            try:
                # Supprimer un personnage spécifique
                sql = "DELETE FROM caractere WHERE nom_caractere = %s"
                self.cursor.execute(sql, (nom_personnage,))
                self.db.commit()

                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Succès", "Personnage supprimé avec succès !")
                else:
                    messagebox.showinfo("Info", "Personnage non trouvé.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression du personnage: {e}")
        else:
            messagebox.showerror("Erreur", "Veuillez entrer le nom du personnage à supprimer.") 
    
    

    def ajout_caractere(self):
       if self.ID_Serie_entry.get()=="" or self.Nom_Perso_entry.get()=="" or self.Roles_entry.get()=="" or self.DescriptionPerso_entry.get()=="": 
          messagebox.showerror("Erreur","Remplissez tous les champs")
       else:
            ID_Serie = self.ID_Serie_entry.get()
            Nom_Perso = self.Nom_Perso_entry.get()
            Roles = self.Roles_entry.get()
            DescriptionPerso = self.DescriptionPerso_entry.get()


            try:
                self.cursor.execute("SELECT id_series FROM series WHERE titre = %s", (ID_Serie,))
                series_id = self.cursor.fetchone()[0]
                self.cursor.execute(
                    "INSERT INTO caractere (id_series, nom_caractere, roles, descriptions) VALUES (%s, %s, %s, %s)",
                    (series_id, Nom_Perso, Roles, DescriptionPerso)
                )
                self.db.commit()
                messagebox.showinfo("Succès", "Caractère ajouté avec succès !")
            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de caractere: {err}")
        
                
if __name__ == "__main__":
    app = App()
    app.mainloop()

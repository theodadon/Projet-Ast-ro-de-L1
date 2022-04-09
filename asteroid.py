# %%

import pygame
import random
import p_vaisseau
from os import path
import fenetre
import p_asteroide



# variables

image_path = path.join(path.dirname(__file__), 'img')
IPS = fenetre.IPS

# couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# initialisation de pygame
pygame.init()
display = fenetre.display
pygame.display.set_caption("Jeu asteroide!")



# on enleve les touches remanentes
pygame.key.set_repeat(10, 10)

# chargement des images
background = pygame.image.load(path.join(image_path, 'fond.jpeg')).convert()
background_rectangle = background.get_rect()
background_victory = pygame.image.load(path.join(image_path, 'victory.jpeg')).convert()
background_victory_rectangle = background.get_rect()
background_fin = pygame.image.load(path.join(image_path, 'fin.jpeg')).convert()
background_fin_rectangle = background.get_rect()

joueur_image = pygame.image.load(path.join(image_path, 'joueur.png')).convert()
asteroide_image = pygame.image.load(
    path.join(image_path, 'asteroide.png')).convert()
mini_asteroide_image = pygame.image.load(
    path.join(image_path, 'miniasteroide.png')).convert()

asteroide_image.set_colorkey(NOIR)
joueur_image.set_colorkey(NOIR)
mini_asteroide_image.set_colorkey(NOIR)

# on change la taille des images
joueur_scaled = pygame.transform.scale(joueur_image, (50, 50))
nb_de_vie = pygame.transform.scale(joueur_image, (15, 15))
asteroide_scaled = pygame.transform.scale(asteroide_image, (50, 50))
mini_asteroide_scaled = pygame.transform.scale(mini_asteroide_image, (50, 50))


fenetre.background = background
fenetre.background_rect = background_rectangle
fenetre.background_fin = background_fin
fenetre.background_fin_rect = background_fin_rectangle
fenetre.background_victory = background_victory
fenetre.background_victory_rect = background_victory_rectangle


en_cours = None
Player = None


def nouvelle_partie():
    global en_cours
    global Player
    fenetre.clock = pygame.time.Clock()

    en_cours = True
    Player = p_vaisseau.vaisseau(
        joueur_scaled, 2, 1.1, fenetre.LARGEUR / 2, fenetre.HAUTEUR / 2)

    fenetre.liste_projectiles = []
    fenetre.liste_asteroides = []
    fenetre.last_projectile = 0
    fenetre.kills = 0
    credits()




def afficher_texte(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, BLANC)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def credits():
    fenetre.changer_etat("credits")
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    fenetre.display.fill(NOIR)
    fenetre.display.blit(background, background_rectangle)
    afficher_texte(fenetre.display, "Jeu Asteroide!", 64,
              fenetre.LARGEUR / 2, fenetre.HAUTEUR / 4)
    afficher_texte(fenetre.display, "Un jeu incroyable par Theo & Sacha",
              22, fenetre.LARGEUR / 2, fenetre.HAUTEUR / 2)
    afficher_texte(fenetre.display, "Appuie sur une touche pour jouer",
              18, fenetre.LARGEUR / 2, fenetre.HAUTEUR * 3 / 4)


def commencer_jeu():
    if (fenetre.etat_du_jeu() == "credits"):
        fenetre.changer_etat("en_jeu")
        fenetre.display.fill(NOIR)
        fenetre.display.blit(background, background_rectangle)


def afficher_asteroide(randomnb):
    if (randomnb == 1):
        
        playerx = Player.vPosX
        playery = Player.vPosY

        # generation de l'asteroide sur une des 4 faces de la fenetre
        randomfaces = random.randint(1, 4)
        if (randomfaces == 1):
            # HAUT
            randomx = random.randint(0, fenetre.LARGEUR)
            randomy = 0
        elif (randomfaces == 2):
            # GAUCHE
            randomx = 0
            randomy = random.randint(0, fenetre.HAUTEUR)
        elif (randomfaces == 3):
            # DROITE
            randomx = fenetre.LARGEUR
            randomy = random.randint(0, fenetre.HAUTEUR)
        elif (randomfaces == 4):
            # BAS
            randomx = random.randint(0, fenetre.LARGEUR)
            randomy = fenetre.HAUTEUR

        if (playerx - 50 < randomx < playerx + 50 and playery - 50 < randomy < playery + 50):
            # si l'asteroide est dans la zone du joueur on fait une reccurence
            afficher_asteroide(randomnb)
            return

        # creation de l'asteroide
        Asteroide = p_asteroide.asteroide(
            asteroide_scaled, mini_asteroide_scaled, 2, 1, randomx, randomy, random.randint(0, 360))
        fenetre.liste_asteroides.append(Asteroide)


nouvelle_partie()

while en_cours:
    fenetre.clock.tick(fenetre.IPS)

    for event in pygame.event.get():

        # on permet de changer la taille de fenetre
        if event.type == pygame.VIDEORESIZE:
            fenetre.LARGEUR = event.w
            fenetre.HAUTEUR = event.h
            fenetre.display = pygame.display.set_mode(
                (fenetre.LARGEUR, fenetre.HAUTEUR), pygame.RESIZABLE)
            background = pygame.transform.scale(
                background, (fenetre.LARGEUR, fenetre.HAUTEUR))
            background_rectangle = background.get_rect()
            

            background_fin = pygame.transform.scale(
                background_fin, (fenetre.LARGEUR, fenetre.HAUTEUR))
            background_fin_rectangle = background_fin.get_rect()

            background_victory = pygame.transform.scale(
                background_victory, (fenetre.LARGEUR, fenetre.HAUTEUR))
            background_victory_rectangle = background_victory.get_rect()





            fenetre.background = background
            fenetre.background_rect = background_rectangle
            
            fenetre.background_victory = background_victory
            fenetre.background_victory_rect = background_victory_rectangle

            fenetre.background_fin = background_fin
            fenetre.background_fin_rect = background_fin_rectangle

        # on permet de quitter le jeu
        if event.type == pygame.QUIT:
            en_cours = False

        # vérification des touches pressées
        liste_touches = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if liste_touches[pygame.K_ESCAPE]:
                en_cours = False

            if fenetre.etat_du_jeu() == "credits":
                if not liste_touches[pygame.K_ESCAPE]:
                    commencer_jeu()

            if fenetre.etat_du_jeu() == "en_jeu":
                Player.keybinds(liste_touches)
            if fenetre.etat_du_jeu() == "fin" or fenetre.etat_du_jeu() == "victoire":
                if liste_touches[pygame.K_r]:
                    nouvelle_partie()

    if fenetre.etat_du_jeu() == "en_jeu":
        # on genere un nombre aleatoire pour verifier si on doit afficher un asteroide
        randomnb = random.randint(1, 300)
        afficher_asteroide(randomnb)

        # on verifie si le joueur a perdu donc si il colle un asteroide
        for asteroide in fenetre.liste_asteroides:
            if Player.rect.colliderect(asteroide.rect):
                fenetre.liste_asteroides.remove(asteroide)
                Player.die()

        fenetre.display.fill(NOIR)
        fenetre.display.blit(background, background_rectangle)
        Player.update()

        # on verifie si un projectile touche un asteroide
        for i in fenetre.liste_projectiles:
            i.update()

            for j in fenetre.liste_asteroides:
                if i.rect.colliderect(j.rect):
                    if (fenetre.liste_projectiles.__contains__(i)):
                        fenetre.liste_projectiles.remove(i)
                        if (fenetre.liste_asteroides.__contains__(j)):
                            j.die()
        for j in fenetre.liste_asteroides:
            j.update()

        # on afiche le score et le nombre de vies
        for r in range(Player.sante + 1):
            fenetre.display.blit(
                nb_de_vie, ((fenetre.LARGEUR - 30) - (20*r), 5))
            score = "Score: {}".format(fenetre.kills)
            afficher_texte(fenetre.display, score, 18, fenetre.LARGEUR /
                      2, fenetre.HAUTEUR - 20)

    elif fenetre.etat_du_jeu() == "fin":
        fenetre.endgame()
    elif fenetre.etat_du_jeu() == "victoire":
        fenetre.win()
    elif fenetre.etat_du_jeu() == "credits":
        credits()
    pygame.display.flip()
pygame.quit()

# %%

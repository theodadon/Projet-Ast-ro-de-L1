# %%
import pygame
from pygame.locals import *

# Initialisation de la fenêtre
clock = pygame.time.Clock()
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
background = 0
background_rect = 0
background_fin = 0
background_fin_rect = 0
background_victory = 0
background_victory_rect = 0
LARGEUR = 880
HAUTEUR = 500
display = pygame.display.set_mode((LARGEUR, HAUTEUR), RESIZABLE)
IPS = 10

# Initialise les listes qui contiennent les projectiles et les asteroïdes
liste_projectiles = []
liste_asteroides = []
last_projectile = 0
kills = 0
status = "credits"


# retourne le statuss
def etat_du_jeu():
    return status

# change le status
def changer_etat(param):
    global status
    global IPS

    if (param == status):
        return
    if (param == "credits" or param == "fin" or param == "victoire"):
        IPS = 10
    elif (param == "en_jeu"):
        IPS = 60
    status = param

# Affiche du texte
def draw_text(surf, text, size, x, y):

    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, BLANC)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)

    surf.blit(text_surface, text_rect)



# Gère l'évènement de la fin du jeu
def endgame():
    changer_etat("fin")
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    display.fill(NOIR)
    display.blit(background_fin, background_fin_rect)
    score = "Votre score: {}".format(kills)
    draw_text(display, "Game Over!", 64, LARGEUR / 2, HAUTEUR / 4)
    draw_text(display, "Vous avez perdu! :( dommage",
              22, LARGEUR / 2, HAUTEUR / 2)
    draw_text(display, "Pour relancer une partie : [R]",
              22, LARGEUR / 2, HAUTEUR / 2 + 50)
    draw_text(display, score, 18, LARGEUR / 2, HAUTEUR * 3 / 4)

# Gère la victoire du joueur en affichant un texte par dessus la fenêtre
def win():
    changer_etat("victoire")
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    display.fill(NOIR)
    display.blit(background_victory, background_victory_rect)
    score = "Votre score final: {}".format(kills)
    draw_text(display, "Bravo!", 64, LARGEUR / 2, HAUTEUR / 4)
    draw_text(display, "Vous avez gagné! :)", 22, LARGEUR / 2, HAUTEUR / 2)
    draw_text(display, "Pour relancer une partie : [R]",
              22, LARGEUR / 2, HAUTEUR / 2 + 50)
    draw_text(display, score, 18, LARGEUR / 2, HAUTEUR * 3 / 4)

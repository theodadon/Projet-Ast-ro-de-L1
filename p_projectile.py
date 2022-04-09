# %%
import pygame
import random
from pygame.locals import *
from os import path
import fenetre
import math


class projectile:
    # Initialisation de la classe
    def __init__(self, vPosX, vPosY, angle, speed=1):
        self.vPosX = vPosX
        self.vPosY = vPosY
        self.speed = speed
        self.angle = angle
        self.rect = pygame.Rect(self.vPosX, self.vPosY, 5, 5)

        fenetre.last_projectile = fenetre.clock.get_time()
    
    # Met à jour la position du projectile
    def update(self):

        angle = (self.angle - 90) / 180 * math.pi
        self.vPosX -= 1 * math.cos(angle) * 15
        self.vPosY += 1 * math.sin(angle) * 15
        

        # Met les projectiles en rouge
        self.rect.center = (self.vPosX, self.vPosY)
        pygame.draw.rect(fenetre.display, (255, 0, 0), self.rect)

        # Détruit les projectiles qui sortent de l'écran
        if self.vPosX > fenetre.LARGEUR:
            self.vPosX = fenetre.LARGEUR
            if fenetre.liste_projectiles.__contains__(self):
                fenetre.liste_projectiles.remove(self)
        if self.vPosX < 0:
            self.vPosX = 0
            if fenetre.liste_projectiles.__contains__(self):
                fenetre.liste_projectiles.remove(self)
        if self.vPosY > fenetre.HAUTEUR:
            self.vPosY = fenetre.HAUTEUR
            if fenetre.liste_projectiles.__contains__(self):
                fenetre.liste_projectiles.remove(self)
        if self.vPosY < 0:
            self.vPosY = 0
            if fenetre.liste_projectiles.__contains__(self):
                fenetre.liste_projectiles.remove(self)

    # def mouvement()

# %%
from audioop import mul
from re import S
import pygame
import p_projectile
import random
from pygame.locals import *
from os import path
import math
import fenetre


class vaisseau:

    def __init__(self, image, sante, vitesse, vPosX, vPosY):
        self.image = image
        self.sante = sante
        self.speed = vitesse
        self.vitesse = vitesse
        self.vPosX = vPosX
        self.vPosY = vPosY

        #Initialiser valeurs
        self.image_avec_langle = image
        self.angle = 0
        self.axe = 0
        self.derniertir = 0
        self.rect = self.image.get_rect()
        self.rect.center = (self.vPosX, self.vPosY)
        self.peut_avancer = False
        self.peut_tirer = True

    def tourner(self, axe):
        self.axe += axe * (2.2)
        # Empecher l'erreur out of memory
        if self.axe > 360:
            self.axe = 0
        if self.axe < 0:
            self.axe = 360

    def die(self):
        if self.sante <= 0:
            self.sante = 0
            self.peut_tirer = False
            fenetre.endgame()
        else:
            self.sante -= 1
            self.vPosX = fenetre.LARGEUR / 2
            self.vPosY = fenetre.HAUTEUR / 2
            self.angle = 0
            self.speed = self.vitesse

    def shoot(self):
        # attente entre 2 tirs
        if self.peut_tirer:
            self.peut_tirer = False
            self.derniertir = pygame.time.get_ticks()
            p = p_projectile.projectile(
                self.vPosX, self.vPosY, self.axe, self.speed)
            fenetre.liste_projectiles.append(p)

    def accelerer(self, z=True):

        if self.peut_avancer == False:
            return
        angle = (self.angle - 90) / 180 * math.pi

        
        self.vPosX -= 1 * math.cos(angle) * self.speed
        self.vPosY += 1 * math.sin(angle) * self.speed


        if self.vPosX > fenetre.LARGEUR:
            # DROITE
            self.vPosX = 0
        if self.vPosX < 0:
            # GAUCHE
            self.vPosX = fenetre.LARGEUR
        if self.vPosY > fenetre.HAUTEUR:
            # BAS
            self.vPosY = 0
        if self.vPosY < 0:
            # HAUT
            self.vPosY = fenetre.HAUTEUR

        self.speed = self.vitesse

    def keybinds(self, liste_touches):
        if liste_touches[K_SPACE]:
            self.shoot()
        if liste_touches[K_q]:
            self.tourner(1)
        if liste_touches[K_d]:
            self.tourner(-1)
        if liste_touches[K_z]:
            self.angle = self.axe
            self.peut_avancer = True
            if (self.speed < 5):
                self.speed = 1.6
            self.accelerer()
        if liste_touches[K_s]:
            self.speed = self.vitesse

    def update(self):

        # verification de la recharge de tir
        if pygame.time.get_ticks() - self.derniertir > 180:
            self.peut_tirer = True

        if self.speed >= 1:
            self.accelerer()
   
        
        self.image_avec_langle = self.image
        self.image_avec_langle = pygame.transform.rotate(self.image_avec_langle, self.axe)
        self.rect = self.image_avec_langle.get_rect()
        self.rect.center = (self.vPosX, self.vPosY)

        fenetre.display.blit(self.image_avec_langle, self.rect)

# %%
import fenetre
import random
import math


class asteroide:
    # Initialise la classe
    def __init__(self, image, miniimage, sante, vitesse, vPosX, vPosY, angle):
        self.image = image
        self.sante = sante
        self.miniimage = miniimage
        self.speed = 1
        self.vitesse = vitesse
        self.vPosX = vPosX
        self.vPosY = vPosY
        self.angle = angle
        self.rect = self.image.get_rect()
        self.canAdvance = False
        self.rect.center = (self.vPosX, self.vPosY)

    # Gère la mort de l'asteroïde
    def die(self):
        if (self.sante == 0):
            if fenetre.liste_asteroides.__contains__(self):
                fenetre.liste_asteroides.remove(self)
                fenetre.kills += 1
                if fenetre.kills >= 10:
                    fenetre.win()
        elif (self.sante > 1):
            if fenetre.liste_asteroides.__contains__(self):
                fenetre.liste_asteroides.remove(self)

                nouvel_asteroide = asteroide(
                    self.miniimage, self.miniimage, 0, 1, self.vPosX, self.vPosY, random.randint(0, 360))

                nouvel_asteroide1 = asteroide(
                    self.miniimage, self.miniimage, 0, 1, self.vPosX, self.vPosY, random.randint(0, 360))

                fenetre.liste_asteroides.append(nouvel_asteroide)
                fenetre.liste_asteroides.append(nouvel_asteroide1)

    # Met a jour la position de l'asteroïde
    def update(self):
        angle = (self.angle - 90) / 180 * math.pi
        self.vPosX -= 1 * math.cos(angle) * self.speed
        self.vPosY += 1 * math.sin(angle) * self.speed
        self.rect.center = (self.vPosX, self.vPosY)
        fenetre.display.blit(self.image, self.rect)

        if self.vPosX > fenetre.LARGEUR:
            self.vPosX = 0
        if self.vPosX < 0:
            self.vPosX = fenetre.LARGEUR
        if self.vPosY > fenetre.HAUTEUR:
            self.vPosY = 0
        if self.vPosY < 0:
            self.vPosY = fenetre.HAUTEUR

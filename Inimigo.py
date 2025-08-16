import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Classe para representar um único alienígena na frota"""

    def __init__(self, ai_game):
        """Inicializa o alienígena e sua posição inicial"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carrega a imagem do alienígena e define seu atributo com rect
        self.image = pygame.image.load("assets/Nave_Inimiga.bmp")
        self.rect = self.image.get_rect()

        # Inicializa cada alien novo perto do canto superior esquerdo tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Armazena a posição horizontal exata do alienígena
        self.x = float(self.rect.x)

    def update(self):
        """Move o alienígena para a direita ou para a esquerda"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Retorna True se o alienígena estiver na borda da tela"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

import pygame
class Ship:
    """Classe para tratar da espaçonave"""

    def __init__(self, ai_game):
        """Inicializa a espaçonave e define a posição inicial"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Sobe a imagem da espaçonave e obtém o react
        self.image = pygame.image.load("Imagens/Jogador.bmp")
        self.rect = self.image.get_rect()

        # Começa cada espaçonave nova no centro inferior da tela
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Desenha a espaçonave em sua localização atual"""
        self.screen.blit(self.image, self.rect)


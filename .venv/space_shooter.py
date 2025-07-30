import sys
import pygame
from settings import Settings
class SpaceShooter:
    """Classe geral para gerenciar ativos e comportamentos do jogo"""

    def __init__(self):
        """ Inicializa o jogo e cria recursos do jogo"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))git
        pygame.display.set_caption('Space Shooter')


        # Define a cor do backgroud.
        self.bg_color = (230, 230, 230)
    def run_game(self):
        """Inicia o loop principal do jogo"""

        while True:
            # Observa eventos de teclhado e mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redesenha a tela durante cada passagem pelo loop.
            self.screen.fill(self.settings.bg_color)

            # Deixa a linha desehada  mais recente visível
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    # Cria a instancia do jogo e executa o jogo
    ai = SpaceShooter()
    ai.run_game()
import sys
import pygame
from settings import Settings
from ship import Ship


class SpaceShooter:
    """Classe geral para gerenciar ativos e comportamentos do jogo"""

    def __init__(self):
        """ Inicializa o jogo e cria recursos do jogo"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Space Shooter')
        self.ship = Ship(self)

        # Define a cor do backgroud.
        self.bg_color = (230, 230, 230)
    def run_game(self):
        """Inicia o loop principal do jogo"""

        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Observa eventos de teclhado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Move a espaçonave para a direita
                    self.ship.rect.x += 1

    def _update_screen(self):
        # Redesenha a tela durante cada passagem pelo loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Deixa a linha desehada  mais recente visível
        pygame.display.flip()

if __name__ == '__main__':
    # Cria a instancia do jogo e executa o jogo
    ai = SpaceShooter()
    ai.run_game()
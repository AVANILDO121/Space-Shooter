import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class SpaceShooter:
    """Classe geral para gerenciar ativos e comportamentos do jogo"""

    def __init__(self):
        """ Inicializa o jogo e cria recursos do jogo"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Space Shooter')
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Define a cor do backgroud.
        self.bg_color = (230, 230, 230)
    def run_game(self):
        """Inicia o loop principal do jogo"""

        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Observa eventos de teclhado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Responde as teclas pressionadas"""
        if event.key == pygame.K_RIGHT:
            # Move a espaçonave para a direita
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Cria um novo projétil e adiciona ao grupo de projéteis"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):

        # Redesenha a tela durante cada passagem pelo loop.
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        # Deixa a linha desehada  mais recente visível
        pygame.display.flip()

if __name__ == '__main__':

    # Cria a instancia do jogo e executa o jogo
    ai = SpaceShooter()
    ai.run_game()
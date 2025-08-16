import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import Game_stats
from ship import Ship
from bullet import Bullet
from Inimigo import Alien
from button import Button

class SpaceShooter:
    """Classe geral para gerenciar ativos e comportamentos do jogo"""

    def __init__(self):
        """ Inicializa o jogo e cria recursos do jogo"""
        pygame.init()

        # Inicia Space Shooter em estado inativo
        self.game_active = False

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Space Shooter')

        # Cria uma instância para armazenar estatísticas do jogo
        self.stats = Game_stats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Define a cor do background.
        self.bg_color = (230, 230, 230)

        # Inicializa Space Shooter em um estado ativo
        #self.game_active = True

        # Cria o botão play
        self.play_button = Button(self, "iniciar")

    def run_game(self):
        """Inicia o loop principal do jogo"""

        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Observa eventos de teclado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Inicia um jogo novo quando o jogador clica em play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Redefine as estatísticas do jogo
            self.stats.reset_stats()
            self.game_active = True

            # Descarta quaisquer projéteis e alienígenas restantes
            self.bullets.empty()
            self.aliens.empty()

            # Cria uma frota nova e centraliza a espaçonave
            self._create_fleet()
            self.ship.center_ship()

            #  Oculta o cursor do mouse
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Responde às teclas pressionadas"""
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
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):

        # Redesenha a tela durante cada passagem pelo loop.
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Desenha o botão play se o jogo estiver inativo
        if not self.game_active:
            self.play_button.draw_button()

        # Deixa a linha desenhada mais recente visível
        pygame.display.flip()

    def _update_bullets(self):
        """Atualiza a posição dos projetéis e descarta os projéteis antigos"""
        # Atualiza as posições dos projéteis
        self.bullets.update()

        # Descartam os projetéis que desaparecem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        """Responde a colisões alienígenas"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Verifica se algum projétil atingiu um alienígena
        # Se sim, descarta o projétil e o alienígena
        if not self.aliens:
            # Destroi todos os projéteis existentes e cria uma nova frota
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Cria a frota de alienígenas"""
        # Cria um alienígena e continua adicionando alienígenas
        # até que não haja mais espaço
        # O distanciamento entre alienígenas é de uma largura
        # de alienígena e uma altura de alienígena
        alien = Alien(self)
        alien_widht, alien_height = alien.rect.size

        currect_x, currect_y = alien_widht, alien_height
        while currect_y < (self.settings.screen_height - 3 * alien_height):
            while currect_x < (self.settings.screen_width - 2 * alien_widht):
                self._create_alien(currect_x, currect_y)
                currect_x += 2 * alien_widht

            # Termina uma fileira; define o valor de x, e incrementa o valor de y
            currect_x = alien_widht
            currect_y += 2 * alien_height



    def _create_alien(self, x_position, y_position):
        """Cria um alienígena e o posiciona a fileira"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Atualiza as posições de todos os alienígenas na frota"""
        self._check_fleet_edges()
        self.aliens.update()

        # Detecta colisões entre alienígenas e espaçonaves
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Procura por alienígenas se chocando contra a parte inferior da tela
        self._check_aliens_botton()

    def _check_fleet_edges(self):
        """Responde apropriadamente se algum alienígena alcançou uma borda"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Faz toda a frota descer e mudar de direção"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Responda à espaçonave sendo abatida por um alienígena"""
        if self.stats.ships_left > 0:

            # Decrementa ships_left
            self.stats.ships_left -= 1

            # Descarta quaisquer projéteis e alienígenas restantes
            self.bullets.empty()
            self.aliens.empty()

            # Cria uma nova frota e centraliza a espaçonave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa quando a nave é explodida
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_botton(self):
        """Verifica se algum alienígena chegou a parte inferior da tela"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Trata isso como se a espaçonave tivesse sido abatida
                self._ship_hit()
                break


if __name__ == '__main__':

    # Cria a instância do jogo e executa o jogo
    ai = SpaceShooter()
    ai.run_game()
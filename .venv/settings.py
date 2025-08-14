class Settings:
    """Classe para armazenar as configurações do jogo"""

    def __init__(self):
        """Inicializa as configurações do jogo"""

        # Configurações de tela
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # Configurações da espaçonave
        self.ship_speed = 1.5

        # Configurações do projetil
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_collor = ((30, 30, 30))
        self.bullet_allowed = 3

        # Configuração da nave alienígena
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction de 1 representa a direita; -1 representa a esquerda
        self.fleet_direction = 1


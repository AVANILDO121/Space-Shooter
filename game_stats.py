class Game_stats:
    """Rastreia as estatísticas de Space Shooter"""

    def __init__(self, ai_game):
        """Inicializa as estatísticas"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Pontuação máxima nunca deve ser redefinida
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """Inicializa as estatísticas que podem mudar durante o jogo"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
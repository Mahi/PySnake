"""Module for the Menu scene."""

import ezpygame
import pygame

from . import game


class Menu(ezpygame.Scene):
    """The menu scene for managing high scores and starting a game."""
    update_rate = 10

    def __init__(self, high_scores, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.high_scores = high_scores
        self.username = username
        self._play_button = None

    def on_enter(self, previous_scene):
        """Re-render the play button and update high scores."""
        super().on_enter(previous_scene)
        font = pygame.font.Font(None, 56)
        self._play_button = font.render('Play', 0, pygame.Color('white'))
        if isinstance(previous_scene, game.Game):
            self._update_high_scores(previous_scene.score)

    def draw(self, screen):
        screen.fill(pygame.Color('black'))
        screenw, screenh = self.application.resolution
        x = (screenw - self._play_button.get_width()) // 2
        y = 20
        screen.blit(self._play_button, (x, y))

        if not self.high_scores:
            return

        font = pygame.font.Font(None, 24)
        hs_text = font.render('High scores:', 0, pygame.Color('white'))

        x = (screenw - hs_text.get_width()) // 2
        y += self._play_button.get_height() + 20
        screen.blit(hs_text, (x, y))

        y += hs_text.get_height() + 10
        for name, score in self.high_scores:
            text = font.render(f'{name}: {score}', 0, pygame.Color('white'))
            x = (screenw - text.get_width()) // 2
            screen.blit(text, (x, y))
            y += text.get_height() + 10

    def handle_event(self, event):
        """Start a new game if the play button was clicked."""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            screenw, screenh = self.application.resolution
            left = (screenw - self._play_button.get_width()) // 2
            right = screenw - left
            top = 20
            bottom = top + self._play_button.get_height()
            if left <= event.pos[0] <= right and top <= event.pos[1] <= bottom:
                game_scene = game.Game()
                self.application.change_scene(game_scene)

    def _update_high_scores(self, score):
        """Add a new score and keep the top 10 high scores."""
        self.high_scores.append((self.username, score))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        self.high_scores = self.high_scores[:10]

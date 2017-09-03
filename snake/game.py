import collections
import enum
import random

import ezpygame
import pygame


class Direction(enum.Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def opposite_directions(d1, d2):
    if d1 == d2:
        return False
    horizontal = {Direction.UP, Direction.DOWN}
    vertical = {Direction.LEFT, Direction.RIGHT}
    return (
        (d1 in horizontal and d2 in horizontal)
        or (d1 in vertical and d2 in vertical)
    )


_key_to_direction_map = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
}


class Snake(collections.deque):

    def __init__(self, *args, direction=Direction.RIGHT, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction = direction
        self.extend = False

    @property
    def head(self):
        return self[-1]

    def move(self):
        x, y = self.head
        if self.direction == Direction.UP:
            y -= 1
        elif self.direction == Direction.DOWN:
            y += 1
        elif self.direction == Direction.LEFT:
            x -= 1
        elif self.direction == Direction.RIGHT:
            x += 1
        self.append((x, y))
        if not self.extend:
            self.popleft()
        else:
            self.extend = False


class Game(ezpygame.Scene):
    update_rate = 10

    def __init__(self, speed=5, size=(12, 9), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snake = Snake(((0, 0), (0, 1), (1, 1)))
        self.apple = size[0] // 2, size[1] // 2
        self.speed = speed
        self.size = size
        self.score = 0
        self._timer = 0
        self._move_dir_queue = collections.deque()

    def on_enter(self, previous_scene):
        super().on_enter(previous_scene)
        self.previous_scene = previous_scene

    def draw(self, screen):
        screen.fill(pygame.Color('black'))

        screenw, screenh = self.application.resolution
        blockw, blockh = screenw // self.size[0], screenh // self.size[1]
        for x, y in self.snake:
            rect = (x * blockw + 1, y * blockh + 1, blockw - 2, blockh - 2)
            pygame.draw.rect(screen, pygame.Color('green'), rect)

        apple_rect = (
            self.apple[0] * blockw + 1, self.apple[1] * blockh + 1,
            blockw - 2, blockh - 2,
        )
        pygame.draw.rect(screen, pygame.Color('red'), apple_rect)

        font = pygame.font.Font(None, 18)
        score_text = font.render(f'Score: {self.score}', 0, pygame.Color('white'))
        screen.blit(score_text, (3, 3))

    def update(self, dt):
        self._timer += dt
        ms_until_move = 1 / self.speed * 1000
        if self._timer >= ms_until_move:
            self._timer -= ms_until_move
            if self._move_dir_queue:
                direction = self._move_dir_queue.popleft()
                if not opposite_directions(direction, self.snake.direction):
                    self.snake.direction = direction
            self.snake.move()
            self._check_apple()
            self._check_collision()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            direction = _key_to_direction_map.get(event.key)
            if direction is not None:
                self._move_dir_queue.append(direction)

    def _place_apple(self):
        viable_places = [
            (x, y)
            for x in range(self.size[0])
            for y in range(self.size[1])
            if (x, y) not in self.snake
        ]
        self.apple = random.choice(viable_places)

    def _check_apple(self):
        if self.snake.head == self.apple:
            self.score += 1
            self._place_apple()
            self.snake.extend = True

    def _check_collision(self):
        x, y = self.snake.head
        if x < 0 or x >= self.size[0]:
            self.application.change_scene(self.previous_scene)
        elif y < 0 or y >= self.size[1]:
            self.application.change_scene(self.previous_scene)
        elif len(self.snake) != len(set(self.snake)):
            self.application.change_scene(self.previous_scene)

import random

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
MIDDLE_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона, ячейки, яблока, змеи:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
COMMON_COLOR = (0, 0, 255)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс для формирования объектов игры."""

    def __init__(self, body_color=COMMON_COLOR):
        self.position = MIDDLE_SCREEN
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта базового класса."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс объекта яблоко."""

    def __init__(self, body_color=COMMON_COLOR, prohibition=None):
        if prohibition is None:
            prohibition = [MIDDLE_SCREEN]
        super().__init__(body_color)
        self.randomize_position(prohibition)

    def randomize_position(self, prohibition):
        """Определяет текущую позицию яблока."""
        while self.position in prohibition:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self):
        """Отрисовка объекта яблоко."""
        super().draw()


class Snake(GameObject):
    """Класс объекта змейка."""

    def __init__(self, body_color=COMMON_COLOR):
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [MIDDLE_SCREEN]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Проверяет и изменяет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки: добавляет новую голову в начало списка."""
        head_x, head_y = self.get_head_position()
        # Вычисляем новые координаты головы в зависимости от направления
        head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        # Добавляем новую голову
        new_head = (head_x, head_y)
        self.positions.insert(0, new_head)

        # Определяем координату хвоста змейки и удаляем после передвижения
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка объекта змейки."""
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)


def main():
    """Создание основного тела игры."""
    # Инициализация PyGame:
    pg.init()
    apple = Apple(APPLE_COLOR)

    snake = Snake(SNAKE_COLOR)

    while True:
        # Бесконечный цикл игры
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        pg.display.update()
        apple.draw()
        snake.draw()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()

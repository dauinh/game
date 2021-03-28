import sys, pygame, random, time

# -------- Universal constants -----------
SIZE = WIDTH, HEIGHT = (300, 300)
directions = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

score = 0
appleSpawned = True

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Snake')

FPS = 10
clock = pygame.time.Clock()

# -------- Classes & Functions -----------
class Snake:
    def __init__(self):
        self.size = 10
        self.dir = random.choice([(-1, 0), (1, 0), (0, 1), (0, -1)])
        self.body = [(150 + i * self.size, 150) for i in range(3)]

    def advanceSnake(self):
        self.body.insert(0, (self.body[0][0] + self.size * self.dir[0],
                             self.body[0][1] + self.size * self.dir[1]))
        self.body.pop()

    def grow(self):
        self.body.append((self.body[-1][0] + self.size * self.dir[0],
                          self.body[-1][1] + self.size * self.dir[1]))

    def draw(self):
        for cell in self.body:
            pygame.draw.rect(screen, Color.white, (cell[0], cell[1], self.size, self.size))

class Food:
    def __init__(self):
        self.size = 5
        self.x = random.randint(self.size * 2, WIDTH - self.size * 2)
        self.y = random.randint(self.size * 2, HEIGHT - self.size * 2)

    def draw(self):
        pygame.draw.rect(screen, Color.red, (self.x, self.y, self.size, self.size))

class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (220, 220, 220)
    red = (255, 0, 0)

def messageDisplay(text):
    font = pygame.font.SysFont('arial', 50)
    textSurf = font.render(text, True, Color.grey)
    textRect = textSurf.get_rect()
    textRect.center = WIDTH/2, HEIGHT/2
    screen.blit(textSurf, textRect)

    pygame.display.update()

    time.sleep(3)
    pygame.quit()
    sys.exit()

def gameOver():
    messageDisplay('Game Over')

def scoreDisplay():
    font = pygame.font.SysFont('arial', 20)
    scoreSurf = font.render('Score: ' + str(score), True, Color.grey)
    scoreRect = scoreSurf.get_rect()
    scoreRect.center = 40, 10
    screen.blit(scoreSurf, scoreRect)

# -------- Creating instances -----------
snake = Snake()
apple = Food()

# -------- Main Program Loop -----------

running = True

while running:
    # ---- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #  Game logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.dir != directions['R']:
                snake.dir = directions['L']

            if event.key == pygame.K_RIGHT and snake.dir != directions['L']:
                snake.dir = directions['R']

            if event.key == pygame.K_UP and snake.dir != directions['D']:
                snake.dir = directions['U']

            if event.key == pygame.K_DOWN and snake.dir != directions['U']:
                snake.dir = directions['D']

    # ---- Change direction
    if snake.dir == directions['L']:    snake.advanceSnake()
    if snake.dir == directions['R']:    snake.advanceSnake()
    if snake.dir == directions['U']:    snake.advanceSnake()
    if snake.dir == directions['D']:    snake.advanceSnake()

    # -------- Game Over -----------
    # ---- Getting out of bounds
    if snake.body[0][0] < 0 or snake.body[0][0] > WIDTH - snake.size \
            or snake.body[0][1] < 0 or snake.body[0][1] > HEIGHT - snake.size:
        screen.fill(Color.black)
        gameOver()

    # ---- Touching snake body
    for cell in snake.body[1:]:
        if snake.body[0][0] == cell[0] and snake.body[0][1] == cell[1]:
            gameOver()

    # ---- Collision
    if (apple.x + snake.size > snake.body[0][0]
            and apple.x < snake.body[0][0] + snake.size
            and apple.y + snake.size > snake.body[0][1]
            and apple.y < snake.body[0][1] + snake.size):
        score += 1
        snake.grow()
        appleSpawned = False

    # ---- Drawing code
    screen.fill(Color.black)
    if not appleSpawned:    # apple is eaten, spawn another
        apple = Food()
        appleSpawned = True
    apple.draw()
    snake.draw()
    scoreDisplay()

    # ---- Refresh game
    pygame.display.update()
    # ---- Refresh rate
    clock.tick(FPS)
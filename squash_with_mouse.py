import random
import pygame, pymunk, sys

pygame.init()
myfont = pygame.font.SysFont("comicsans", 30)
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 500
space = pymunk.Space()
space.gravity = (0, 100)
l_thick = screen.get_width()//20  #  line thickness
ball_size = screen.get_width()//100
set_of_collisions =set()
points = 0

class Ball():
    def __init__(self):
        self.body = pymunk.Body()
        self.body.position = screen.get_width()//2, l_thick + 10
        self.body.velocity = 0,100
        self.shape = pymunk.Circle(self.body, ball_size)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        self.shape.collision_type = 1
        self.lives = 3

    def draw(self):
        pygame.draw.circle(screen, 'white', self.body.position, ball_size)

    def ball_reset(self):
        if self.body.position.x >= screen.get_width() + 500 or int(self.body.velocity.x) == 0 and int(self.body.velocity.y) == 0:
            self.body.position = screen.get_width()//2, l_thick+10
            self.body.velocity = 0, 10
            self.lives -=1


class Wall():
    def __init__(self, p1, p2,  collision_number = None):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, l_thick//2)
        self.shape.elasticity = 0.95
        space.add(self.body, self.shape)
        self.colour = 'grey'
        self.shape.collision_type = collision_number

    def draw(self):
        pygame.draw.line(screen, self.colour, self.shape.a, self.shape.b, l_thick)

    def change_colour(self, arbiter, space, data):
        self.colour = 'green'
        set_of_collisions.add(self.shape.collision_type)

    def flicker(self, r1, r2, r3):
            self.colour = (r1, r2, r3)


class Player():
    def __init__(self, colour):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = 600, 600
        self.shape = pymunk.Circle(self.body, ball_size*3)
        self.shape.elasticity = 1.1
        space.add(self.body, self.shape)
        self.colour = colour

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.body.position, ball_size*3)

    def move(self):
        self.body.position = pygame.mouse.get_pos()


def game_over():
    screen.fill('black')
    label = myfont.render(f"Game over", True, (255, 255, 0))
    rectangle = label.get_width()
    print(rectangle)
    screen.blit(label, (screen.get_width()//2 - rectangle//2, l_thick * 2))
    print(screen.get_width()//2)
    label1 = myfont.render(f"Your score: {points}", True, (255, 255, 0))
    rectangle1 = label1.get_width()
    screen.blit(label1, (screen.get_width()//2 - rectangle1//2, l_thick * 4))
    pygame.display.update()

    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


def game():

    global points
    ball = Ball()
    player = Player('white')
    walls = []
    handlers = []

    dimensions = [([0,0], [0, screen.get_height()]),
                  ([0, screen.get_height()], [screen.get_width(), screen.get_height()]),
                  ([0, 0], [screen.get_width(), 0])]
    for i in range(3):   # to create 3 walls with different collision numbers
        i_d = dimensions[i]
        p1 = i_d[0]
        p2 = i_d[1]
        wall = Wall(p1, p2, collision_number=i+2)
        walls.append(wall)

    for num in range(0, 3):  # to create 3 handlers with different collision types
        handler = space.add_collision_handler(1, 2+num)
        handlers.append(handler)
    for i, handler in enumerate(handlers):  # to set a handler to a wall
        handler.separate = walls[i].change_colour

    while True:  # game loop
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.shape.elasticity = 2
                player.colour = 'red'
            elif event.type == pygame.MOUSEBUTTONUP:
                player.shape.elasticity = 1
                player.colour = 'white'

        space.step(1 / FPS)
        screen.fill('black')
        label = myfont.render(f"Score: {points}", True, (255, 255, 0))
        rectangle = label.get_width()
        screen.blit(label, (screen.get_width() - l_thick*2 - rectangle, l_thick*2))
        label = myfont.render(f"Lives: {ball.lives}", True, (255, 255, 0))
        rectangle = label.get_width()
        screen.blit(label, (screen.get_width() - l_thick*2 - rectangle, l_thick*4))

        for wall in walls:
            wall.draw()
        ball.draw()
        ball.ball_reset()
        if ball.body.position.x >= screen.get_width():
            set_of_collisions.clear()
            for wall in walls:
                wall.colour = 'grey'
        player.draw()
        player.move()
        pygame.display.update()

        if set_of_collisions == {2, 3, 4}: # if ball collides with all walls
            amount = int(ball.body.velocity[1]//10) + int(ball.body.velocity[0]//10)# points to add
            if amount > 0:
                amount = amount
            elif amount < 0:
                amount *= -1
            points += amount
            set_of_collisions.clear()
            r1 = random.randint(0,255)
            r2= random.randint(0, 255)
            r3 = random.randint(0, 255)
            for wall in walls:
                wall.flicker(r1, r2, r3)

        if ball.lives ==0:
            game_over()
        clock.tick(FPS)

game()
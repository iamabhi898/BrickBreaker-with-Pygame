import pygame
import random
from button import Button

pygame.init()

scr_width = 800
scr_height = 600

screen = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption("Brick Breaker")

# COLORS IN GAME
bkgrd_color = (200, 200, 200)
ball_color = (50, 40, 255)
paddle_color = (80, 50, 30)
brick_color = [(200, 50, 80), (45, 80, 240), (46, 235, 70),
               (150, 50, 180), (230, 170, 80), (60, 230, 220), (180, 210, 80)]


class Bricks():

    global screen
    global scr_width
    global scr_height
    global brick_color

    def __init__(self):
        self.rows = 7
        self.rows_bricks = 9
        self.length = int(scr_width*0.8)//self.rows_bricks
        self.width = 40
        self.spacing = 4
        self.cordinates = []
        self.random_color = []
        for i in range(10, self.rows*(self.width), self.width):
            for j in range(int(scr_width*0.1), int(scr_width*0.9 - self.length)+1, self.length):
                self.cordinates.append([j, i])
                self.random_color.append(random.choice(brick_color))

    def show(self):
        num = 1
        color_index = 1
        for item in self.cordinates:
            pygame.draw.rect(screen, brick_color[color_index-1], ((
                item[0], item[1]), (self.length-self.spacing, self.width-self.spacing)))
            num += 1
            if num > color_index * self.rows_bricks:
                color_index += 1

        # self.random_color[num]

    def clone(self):
        brick_list = []
        for item in self.cordinates:
            brick_list.append(item)
        return brick_list

    def update(self, cordinate):
        pygame.draw.rect(screen, bkgrd_color, (cordinate,
                                               (self.length-self.spacing, self.width-self.spacing)))


class Paddle():

    global screen
    global scr_height
    global scr_width
    global paddle_color

    def __init__(self, paddleX):
        self.paddleX = paddleX
        self.paddleY = int(scr_height*0.95)
        self.length = 120

    def show(self):
        thickness = 10
        pygame.draw.rect(screen, paddle_color, ((
            self.paddleX, self.paddleY), (self.length, thickness)))

    def move_left(self):
        self.velocity = 15
        self.paddleX += -self.velocity

    def move_right(self):
        self.velocity = 15
        self.paddleX += self.velocity

    def stop(self):
        self.velocity = 0

    def boundries(self):
        if self.paddleX >= (scr_width - self.length):
            self.paddleX = scr_width - self.length
        elif self.paddleX <= 0:
            self.paddleX = 0


# have to initial here because there is a reference of paddle in Ball object
paddle = Paddle(int(scr_width*0.45))


class Ball():

    global screen
    global ball_color
    global paddle

    def __init__(self, ballX, ballY):
        self.ballX = ballX
        self.ballY = ballY
        self.x_vel = 8
        self.y_vel = -8
        self.ball_radius = 10
        self.max_x_vel = 10

    def show(self):

        pygame.draw.circle(screen, ball_color,
                           (self.ballX, self.ballY), self.ball_radius)

    def move(self):

        self.ballX += self.x_vel
        self.ballY += self.y_vel

    def collision_change(self):

        center = paddle.paddleX + paddle.length//2
        left_end = paddle.paddleX
        right_end = paddle.paddleX + paddle.length
        self.y_vel = -self.y_vel
        if left_end < self.ballX < center:
            ratio = (center - self.ballX)//(paddle.length//2)
            self.x_vel += -self.max_x_vel * ratio
        elif center < self.ballX < right_end:
            ratio = (self.ballX - center)//(paddle.length//2)
            self.x_vel += self.max_x_vel * ratio

    def boundries(self):

        if self.ballY <= (0 + self.ball_radius):
            self.y_vel = -self.y_vel
        if self.ballX <= (0 + self.ball_radius):
            self.x_vel = -self.x_vel
        if self.ballX >= (scr_width - self.ball_radius):
            self.x_vel = -self.x_vel

    def limit_vel(self):

        if -self.max_x_vel > self.x_vel:
            self.x_vel = -self.max_x_vel
        elif self.x_vel > self.max_x_vel:
            self.x_vel = self.max_x_vel


def brick_collision(brick, brick_list, brick_breaked, ball):
    for item in brick_list:
        x = item[0]
        y = item[1]
        index = brick_list.index(item)
        if x < ball.ballX and ball.ballX < (x + brick.length) and (ball.ballY + ball.ball_radius) > y and ball.ballY < y:
            ball.y_vel = -ball.y_vel
            brick_breaked.append(item)
            brick_list.pop(index)
        elif y < ball.ballY and ball.ballY < (y + brick.width) and (ball.ballX + ball.ball_radius) > x and ball.ballX < x:
            ball.x_vel = -ball.x_vel
            brick_breaked.append(item)
            brick_list.pop(index)
        elif y < ball.ballY and ball.ballY < (y + brick.width) and (ball.ballX - ball.ball_radius) < (x + brick.length) and ball.ballX > (x + brick.length):
            ball.x_vel = -ball.x_vel
            brick_breaked.append(item)
            brick_list.pop(index)
        elif x < ball.ballX and ball.ballX < (x + brick.length) and (ball.ballY - ball.ball_radius) < (y + brick.width) and ball.ballY > (y + brick.width):
            ball.y_vel = -ball.y_vel
            brick_breaked.append(item)
            brick_list.pop(index)


def show_gameover():
    global scr_height
    global scr_width
    text = pygame.font.Font("freesansbold.ttf", int(scr_height*0.1))
    gameover = text.render("GAME OVER", True, (255, 23, 20))
    screen.blit(gameover, (int(scr_width*0.25), int(scr_height*0.4)))


clock = pygame.time.Clock()

while True:

    # initial positions

    ball = Ball(int(scr_width/2), int(scr_height*0.8))
    brick = Bricks()
    brick_list = brick.clone()
    brick_breaked = []
    over = False
    clicked_replay = False

    # paddle movement switches
    key_left = False
    key_right = False

    while True:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_left = True
                if event.key == pygame.K_RIGHT:
                    key_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    paddle.stop()
                    key_left = False
                if event.key == pygame.K_RIGHT:
                    paddle.stop()
                    key_right = False

        # GAME LOGIC

        # paddle movement switches
        if key_left == True:
            paddle.move_left()
        if key_right == True:
            paddle.move_right()

        # ball machanics
        ball.move()
        ball.boundries()
        ball.limit_vel()
        #  must review code in the first inquality statement 
        if paddle.paddleY + 10 > (ball.ballY + ball.ball_radius) > paddle.paddleY and ball.ballX > paddle.paddleX and ball.ballX < (paddle.paddleX + paddle.length):
            ball.collision_change()
        # brick collision
        brick_collision(brick, brick_list, brick_breaked, ball)

        # paddle boundries
        paddle.boundries()
        if ball.ballY > scr_height:
            show_gameover()
            over = True
            # REPLAY BUTTON
            b = Button(screen, (80, 45, 200), (200, 250, 255),
                       (260, 350), (150, 60), "REPLAY", 30)
            state = 'original'
            while True:
                b.show()
                for event in pygame.event.get():
                    if b.isOverMouse() == True:
                        if event.type == pygame.MOUSEBUTTONUP:
                            clicked_replay = True
                        state = 'changed'
                    elif b.isOverMouse() == False:
                        state = 'original'
                    if event.type == pygame.QUIT:
                        pygame.quit()
                if state == 'changed':
                    b.changeColor((80, 240, 80), (14, 37, 100))
                if clicked_replay == True:
                    break
                pygame.display.update()

        # DISPLAY THINGS

        screen.fill(bkgrd_color)
        paddle.show()
        brick.show()
        for brk in brick_breaked:
            brick.update(brk)
        # brick_collision(brick, brick_list, ball)
        ball.show()
        if over == True:
            break

        pygame.display.update()

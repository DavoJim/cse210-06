import random

from casting.actor import Actor
from casting.artifact import Artifact
from casting.cast import Cast

from directing.stardust_game import StardustGame

from service.keyboard_service import KeyboardService
from service.video_service import VideoService

from shared.color import Color
from shared.point import Point



FRAME_RATE = 25
MAX_X = 900
MAX_Y = 600
CELL_SIZE = 15
FONT_SIZE = 17
COLS = 60
ROWS = 40
CAPTION = "Project Stardust"
WHITE = Color(255, 255, 255)
DEFAULT_ROCKS = 90
DEFAULT_GEMS = 60


def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(FONT_SIZE)
    banner.set_color(WHITE)
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the robot
    x = int(MAX_X / 2)
    y = int(MAX_Y - 30)
    position = Point(x, y)

    robot = Actor()
    robot.set_text(">")
    robot.set_font_size(FONT_SIZE)
    robot.set_color(WHITE)
    robot.set_position(position)
    cast.add_actor("robots", robot)
    
    # create the artifacts
    for _ in range(DEFAULT_ROCKS):
        
        score = -50
        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        rocks = Artifact()
        rocks.set_text("O")
        rocks.set_font_size(FONT_SIZE)
        rocks.set_color(color)
        rocks.set_position(position)
        rocks.set_score(score)
        cast.add_actor("rocks", rocks)
    
    for _ in range(DEFAULT_GEMS):
        
        score = 10
        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        gems = Artifact()
        gems.set_text("*")
        gems.set_font_size(FONT_SIZE)
        gems.set_color(color)
        gems.set_position(position)      
        gems.set_score(score)
        cast.add_actor("gems", gems)
    
    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = StardustGame(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()
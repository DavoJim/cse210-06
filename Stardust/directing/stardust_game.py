from shared.point import Point
import time



class StardustGame:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._INIT_SCORE = 600
        self._TOTAL_SCORE = self._INIT_SCORE
        self._is_gameover = False
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open() and self._TOTAL_SCORE > 0:
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._is_gameover = True    
        self._do_updates(cast)
        self._do_outputs(cast)
        time.sleep(2)

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        rocks = cast.get_actors("rocks")
        gems = cast.get_actors("gems")

        if self._is_gameover == True:
            banner.set_text("Game Over")
        else:
            banner.set_text(f"Score : {self._TOTAL_SCORE}")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)

        # This Point represents the velocity of the elements
        x1 = 0
        y1 = 0
        velocity = Point(x1, y1)
                
        for rock in rocks:
            rock.set_velocity(Point(x1, y1 + 1))
            rock.move_next(max_x,max_y)
            if robot.get_position().equals(rock.get_position()):
                score = rock.get_score()
                self._TOTAL_SCORE += score
                banner.set_text(f"Score : {self._TOTAL_SCORE}")
                cast.remove_actor("rocks", rock)
                break


        for gem in gems:
            gem.set_velocity(Point(x1 - 1, y1))
            gem.move_next(max_x,max_y)
            if robot.get_position().equals(gem.get_position()):
                score = gem.get_score()
                self._TOTAL_SCORE += score
                banner.set_text(f"Score : {self._TOTAL_SCORE}")
                cast.remove_actor("gems", gem)
                break

        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()
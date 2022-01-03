# Author: Luke Wismer
# Pygame Memory game, allowing user to race the timer

import pygame, random

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((525, 425))
   # set the title of the display window
   pygame.display.set_caption('A template for graphical games with two moving dots')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit()

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.FPS = 60
        self.score = 0
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        self.images = self.create_game_list()
        self.unrevealed_img = pygame.image.load('tiles/image0.bmp')

        self.number_flips = 0

        self.completed_tiles = []
        
        # === game specific objects
        self.tile1 = Tile(self.surface, self.unrevealed_img, self.images[0], (100,100), (5,5))
        self.tile2 = Tile(self.surface, self.unrevealed_img, self.images[1], (100,100), (110,5))
        self.tile3 = Tile(self.surface, self.unrevealed_img, self.images[2], (100,100), (215,5))
        self.tile4 = Tile(self.surface, self.unrevealed_img, self.images[3], (100,100), (320,5))

        self.tile5 = Tile(self.surface, self.unrevealed_img, self.images[4], (100,100), (5,110))
        self.tile6 = Tile(self.surface, self.unrevealed_img, self.images[5], (100,100), (110,110))
        self.tile7 = Tile(self.surface, self.unrevealed_img, self.images[6], (100,100), (215,110))
        self.tile8 = Tile(self.surface, self.unrevealed_img, self.images[7], (100,100), (320,110))

        self.tile9 = Tile(self.surface, self.unrevealed_img, self.images[8], (100,100), (5,215))
        self.tile10 = Tile(self.surface, self.unrevealed_img, self.images[9], (100,100), (110,215))
        self.tile11 = Tile(self.surface, self.unrevealed_img, self.images[10], (100,100), (215,215))
        self.tile12 = Tile(self.surface, self.unrevealed_img, self.images[11], (100,100), (320,215))

        self.tile13 = Tile(self.surface, self.unrevealed_img, self.images[12], (100,100), (5,320))
        self.tile14 = Tile(self.surface, self.unrevealed_img, self.images[13], (100,100), (110,320))
        self.tile15 = Tile(self.surface, self.unrevealed_img, self.images[14], (100,100), (215,320))
        self.tile16 = Tile(self.surface, self.unrevealed_img, self.images[15], (100,100), (320,320))

        self.tiles = [self.tile1, self.tile2, self.tile3, self.tile4, self.tile5, self.tile6, self.tile7, self.tile8, self.tile9,
                        self.tile10, self.tile11, self.tile12, self.tile13, self.tile14, self.tile15, self.tile16]

        self.frame_counter = 0

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            
            pygame.time.wait(150) # Delay for user to see the flipped card

            if self.number_flips % 2 == 0 and self.number_flips != 0:
                # If number of flips is even and not zero hide all unsucessful flips
                self.hide_tiles()
                self.draw()
                if self.continue_game:
                    self.update()
                    self.decide_continue()

            self.number_flips = 0 # Reset flip counter

            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            # Control all pygame events
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event.pos)

    def draw(self):
        # Draw all game objects.
        self.surface.fill(self.bg_color) # clear the display surface first
        for tile in self.tiles:
            tile.draw()
        self.draw_score()
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        self.score = pygame.time.get_ticks() //1000

    def decide_continue(self):
        # Check and remember if the game should continue
        num_tiles_revealed = 0 # Counter for how many of the 16 tiles are revealed
        for tile in self.tiles:
            # Loop to count all revealed tiles
            if tile.is_revealed():
                num_tiles_revealed += 1
        
        if num_tiles_revealed == 16:
            # If all tiles are revealed, stop game
            self.continue_game = False

    def handle_mouse_up(self, pos):
        # Handles the actions when the mouse is released
        for tile in self.tiles:
            if tile.is_clicked(pos): # Returns a bool if it was clicked or not (based on position)
                self.number_flips += 1
        
        if self.number_flips % 2 == 0 and self.number_flips != 0:
            # If number of flips is even and not 0 then check for matches
            self.handle_matching()

    def handle_matching(self):
        # Handles all matching for flipped tiles
        flipped_tiles = []

        for tile in self.tiles:
            if (tile.is_revealed() == True) and (tile.is_complete() == False):
                # Adds all newly flipped tiles to a list
                flipped_tiles.append(tile)

        if len(flipped_tiles) == 2:
            if flipped_tiles[0].get_image() == flipped_tiles[1].get_image():
                # If the images of newly flipped tiles are the same, they are completed
                flipped_tiles[0].set_complete(True)
                flipped_tiles[1].set_complete(True)

        pygame.time.wait(150)

    def hide_tiles(self):
        # Hides all non completed tiles
        for tile in self.tiles:
            if tile.is_complete() == False:
                tile.set_revealed(False)
    
    def draw_score(self):
      score_string = str(self.score)
      # step 1 create a font object
      font_size = 80
      fg_color = pygame.Color('white')
      font = pygame.font.SysFont('',font_size)
      # step 2 render the font
      text_box = font.render(score_string, True,fg_color,self.bg_color)
      # step 3  compute the location 
      location = (445,0)
      self.surface.blit(text_box,location)

    def create_game_list(self):
        # Creates a game list with all of the images
        self.images = []
        for i in range(1,9):
            self.images.append(pygame.image.load(f'tiles/image{i}.bmp'))
        self.images += self.images # Concatenate to double the images
        random.shuffle(self.images)
        return self.images

class Tile:
    # An object represents one tile

    def __init__(self, surface, unrevealed_img, revealed_img, dimensions, coords):
        # Tile specific variables
        self.surface = surface
        self.unrevealed_img = unrevealed_img
        self.revealed_img = revealed_img
        self.revealed = False
        self.dimensions = dimensions
        self.coords = coords
        self.rect = pygame.Rect(coords, dimensions)

        self.complete = False
    
    def draw(self):
        # Draws the tile's image if revealed or not
        if self.revealed == False:
            self.surface.blit(self.unrevealed_img, self.coords)

        elif self.revealed == True:
            self.surface.blit(self.revealed_img, self.coords)

    def is_clicked(self, position):
        # Checks to see if the position of the click is on the image
        if self.rect.collidepoint(position):
            self.revealed = True
        return self.revealed

    def is_revealed(self):
        # Getter method to see if revealed or not
        return self.revealed

    def set_revealed(self, setting):
        # Setter method to set a new reveal stage
        self.revealed = setting

    def get_image(self):
        # Getter method to see image
        return self.revealed_img

    def get_coords(self):
        # Getter method to see coordinates
        return self.coords

    def is_complete(self):
        # Getter method to see if complete or not
        return self.complete

    def set_complete(self, setting):
        # Setter method to set a new complete stage
        self.complete = setting

main()
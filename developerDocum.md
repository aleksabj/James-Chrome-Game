                                                            #Developer Documentation#


                                                            #Architecture Overview: #    
The game is structured into several key classes and functions that handle everything from character animation to obstacle movement and collision detection.


                                                    
                                                    #Main Classes and Their Roles:#
1) PixarCloud: Handles the background cloud animation, moving across the screen to give the appearance of movement.
2) James: Represents the player character with methods to handle running, jumping, and ducking animations, user input, and game state updates.
3) Obstacles: A 'superclass' used as a template for specific obstacles.
(i) Randall, Roz, Art, Fly: Subclasses of Obstacles represent different types of obstacles James must avoid.
4) Socks: Represents collectible items that increase the player's score.



                                                                #Key Functions:#
1) spawn_socks(): Handles the logic for spawning socks on the screen.
2) menu(): Shows the main menu and restart menu after the game is over.
3) main(): Contains the main game loop, handling game state, background, and foreground movement, event processing, and collision detection.
4) Score(): Captures and updates the score as the game progresses.
5) Background(): Manages the background scrolling effect. (the ground)
6) Foreground(): Manages the foreground scrolling effect, which moves at the same speed as the background for consistency. (the houses)



                                                            #Game Mechanics:#
1) The game difficulty increases with the player's score.
2) Obstacles are randomly spawned with defined intervals to challenge the player.
3) Player character collision with any obstacle results in 'game over'.
4) Socks are spawned less frequently and provide an opportunity for extra points.



                                                            #Collision Detection:#
1) The game utilizes the Pygame library's colliderect() method for collision detection between James and obstacles and socks.



                                                    #Game Speed and Display Management:#
The game speed is controlled by a global variable. (game_speed = 15)
1) pygame.time.Clock() is used to control the frame rate, ensuring the game runs consistently on different hardware.
2) The Pygame update() method is called within the game loop to refresh the screen and display updates to the player.




                                                    #Graphics and Animation Handling:#
The game utilizes static images loaded from a dedicated images directory, which are used to create animations for different game states:
1) The James class switches between images for running, jumping, and ducking based on the user's input and current game state.
2) For obstacle classes (Randall, Roz, Art, Fly), each has an update method to handle their entry and exit from the screen.



                                                    #Background and Foreground Rendering:#    
(i) Backgrounds and foregrounds are treated as separate entities, each scrolling at the game speed to create a parallax effect.
(ii) Backdrops loop infinitely by checking if the image has moved past the left edge of the screen and then resetting its position to create seamless scrolling.


                                                                #Event Loop:#
Within the main function, the event loop calls pygame.event.get() to listen for events like key presses and the window close event:
1) The pygame.QUIT event triggers when the player closes the game window, immediately exiting the game loop and ending the game.
2) The pygame.KEYDOWN event checks for player inputs (up and down arrow keys) to control the character's actions.



                                                                #Game Loop:#
The main game loop in the main function runs as long as the running variable is True. It controls the sequence of gameplay logic:
1) Process user inputs and update game character- James.
2) Move and redraw the background and foreground.
3) Handle obstacle and socks spawning, updating, and rendering.
4) Detect collisions.
5) Update the score.
6) Refresh the game display at a consistent frame rate (of 30 frames per second).
7) Return to the menu when the game is over.



                                            #Scoring System and Difficulty Progression:#
The Score() function updates the display of the current score and checks if it is time to increase the game's speed.
As the player reaches designated score benchmarks, the game's challenge level escalates through enhancements to the 'game_speed' variable. This progressive difficulty curve maintains an engaging and constantly evolving challenge for the player.



                                                            #Asset Management:#
(i) Images and other assets are managed via an organized filesystem. Each type of asset (e.g., character sprites, obstacles, collectibles) has its dedicated folder within the images directory.
(ii) Pygame's image.load() method is used to load visual assets as needed, and os.path.join() ensures the correct file paths are utilized, making the asset management system robust and easily expandable.






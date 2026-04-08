snake.py as made by me

You will need:
- Python (duh)
- Pygame package (a version that works for your python version)
- Random package, Time package (these might come with .py standardly)
NB: There’s a couple .png image files used. You’re gonna need these. In theory you could replace them but it will likely make stuff look like ass

cmd.exe --> python (downloads pip) --> python -m pip install pygame-ce
or py -m pip install pygame
whichever works depends on your setup, python version etc. search engines are your friend

This was done as a school project where the goal was to make some kind of application or game, for which I chose the classic game Snake, in python. This is funny, because a python is a kind of snake.

Features include:
- Snake game
- Difficulty settings
- Customisation options (font, dark/light mode, snake color)
- High score
- 2-player versus mode
- Obstacles that spawn randomly

Tutorial:
You are a snake (green, initially). You must eat fruits to grow larger (blue) and increase your score.
You will die if you touch the walls, obstacles (grey) or yourself.
In vs. mode, player two is the brown snake. Win by getting them snagged on yourself, or by outlasting them.
A head on collision means the game will tie. Eat fruits to grow larger, so that it's easier to entrap the other player.

Potential to do list for the future:
- Make a tutorial or some such thing
- Optimise the code, ie load music/images as variables as opposed to loading them every loop
- Fix rainbow
- Reduce redunancy in code? coop booleans and such
- Add more audio stuff (gameover, starman, etc)
- Add fonts as files to reduce headache for ppl who don't have Windows fonts / better portability
- Add a cap to the amount of rocks or implement Dijkstra's alg for not getting softlocked
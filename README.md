# Breakout Neural Network
This project was inspired by one of Deepmind's early presentations: an AI 
capable of mastering breakout through Deep Q-Learning. The game itself was built 
using the [pygame](https://www.pygame.org/docs/) library. The AI is built using 
[NEAT](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf), an algorithm 
made for implementing a neural network. The documentation for the NEAT python 
package can be found 
[here](https://neat-python.readthedocs.io/en/latest/neat_overview.html). The 
specific configuration of NEAT in this project is similar to that of a [Flappy
Bird AI tutorial by Tech with Tim](https://www.youtube.com/playlist?list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2)

## Generation 10
![Generation 10](https://raw.githubusercontent.com/AtlasMons/DM-Breakout/master/Gen%2010.gif)
Movements are almost completely random at this stage. The members that survive
the longest are the ones which move right as the ball first descends.

## Generation 100
![Generation 100](https://raw.githubusercontent.com/AtlasMons/DM-Breakout/master/Gen%20100.gif)
Failed mutations are still very common at this stage. Although, many more 
members of the population now successfully track the ball, and will follow it 
as it goes from left to right.
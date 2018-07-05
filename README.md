# Boids

This artificial life program simulates the flocking behavior of animals. Using the [`pygame`](https://pygame.org/), `math`, and `random` libraries, an object is created (a bat in this case) that will be attracted to the other objects in the sim. As they fly around, they eventually maintain a minimum distance between each other and approach their neighbors' velocities until they all reach a regulated velocity. The user can interact with the simulation by clicking to generate more bats.

There are three editable constants: `ECCENTRICITY`, `CONFORMITY`, and `SHYNESS` (modifiable in `simulation.py`) which control the behavior of the animals. The degree of random fluctuation in the bats' movements is the eccentricity factor. The shyness is how inclined the bats are to repel their neighbors, while conformity is the factor that determines their tendency to change their velocity to gather and align with the bats around them.

**Inspiration:** [Boids - Wikipedia, the free encyclopedia](https://en.wikipedia.org/wiki/Boids)

### Getting Started

    pip install -r requirements.txt
    ./simulation.py

Press the spacebar to ready the simulation, and again to start it. Click to place boids.

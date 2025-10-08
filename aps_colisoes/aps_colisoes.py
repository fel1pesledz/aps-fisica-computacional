import curses
import numpy as np
import random
import math
import time

# Function to initialize particles
def initialize_particles(num_particles):
    particles = np.zeros(num_particles, dtype=[
        ('x', float), ('y', float),
        ('vx', float), ('vy', float),
        ('mass', float), ('color', int)
    ])

    for particle in particles:
        particle['x'] = random.uniform(1, 83)
        particle['y'] = random.uniform(1, 59)
        particle['vx'] = random.uniform(-1, 1) / 5
        particle['vy'] = random.uniform(-1, 1) / 5
        particle['mass'] = random.uniform(10, 20)
        particle['color'] = random.randint(1, 15)

    return particles

# Function to draw particles
def draw_particles(stdscr, particles):
    for particle in particles:
        x, y = int(particle['x']), int(particle['y'])
        radius = int(particle['mass'] // 10)
        char = 'O' if radius < 2 else '0'
        try:
            stdscr.addch(y, x, char, curses.color_pair(particle['color']))
        except curses.error:
            pass

# Main simulation function
def simulate(stdscr, num_particles):
    curses.curs_set(0)
    stdscr.nodelay(1)

    particles = initialize_particles(num_particles)

    delay = 0.05

    while True:
        stdscr.clear()

        draw_particles(stdscr, particles)
        stdscr.refresh()

        for particle in particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']

            # Boundary collision
            if particle['x'] <= 1 and particle['vx'] < 0: particle['vx'] = -particle['vx']
            if particle['y'] <= 1 and particle['vy'] < 0: particle['vy'] = -particle['vy']
            if particle['x'] >= 83 and particle['vx'] > 0: particle['vx'] = -particle['vx']
            if particle['y'] >= 59 and particle['vy'] > 0: particle['vy'] = -particle['vy']

        # Particle collisions
        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                dist = math.hypot(particles[j]['x'] - particles[i]['x'], particles[j]['y'] - particles[i]['y'])
                if dist < 2:
                    angle = math.atan2(particles[j]['y'] - particles[i]['y'], particles[j]['x'] - particles[i]['x'])
                    speed1 = math.hypot(particles[i]['vx'], particles[i]['vy'])
                    speed2 = math.hypot(particles[j]['vx'], particles[j]['vy'])

                    mass1 = particles[i]['mass']
                    mass2 = particles[j]['mass']

                    new_vx1 = (speed1 * math.cos(angle) * (mass1 - mass2) + 2 * mass2 * speed2 * math.cos(angle)) / (mass1 + mass2)
                    new_vy1 = (speed1 * math.sin(angle) * (mass1 - mass2) + 2 * mass2 * speed2 * math.sin(angle)) / (mass1 + mass2)
                    new_vx2 = (speed2 * math.cos(angle) * (mass2 - mass1) + 2 * mass1 * speed1 * math.cos(angle)) / (mass1 + mass2)
                    new_vy2 = (speed2 * math.sin(angle) * (mass2 - mass1) + 2 * mass1 * speed1 * math.sin(angle)) / (mass1 + mass2)

                    particles[i]['vx'] = new_vx1
                    particles[i]['vy'] = new_vy1
                    particles[j]['vx'] = new_vx2
                    particles[j]['vy'] = new_vy2

        time.sleep(delay)
        if stdscr.getch() == ord(' '):
            break

# Setup curses and start simulation
def main():
    num_particles = int(input("DIGITE O NUMERO DE PARTICULAS: "))
    curses.wrapper(simulate, num_particles)

if __name__ == "__main__":
    main()

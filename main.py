import pyglet
import engine as e
import interface as i
from pyglet.window import key
from random import choice
from math import sqrt

def main():
    screen = i.Interface()
    screen.start_menu()
    pyglet.clock.schedule(screen.update)
    pyglet.app.run()

if __name__ == "__main__":
    main()
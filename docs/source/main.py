import pyglet
from modules import interface as i

def main():
    """Starts the program"""

    screen = i.Interface()
    screen.start_menu()
    pyglet.clock.schedule(screen.update)
    pyglet.app.run()

if __name__ == "__main__":
    main()

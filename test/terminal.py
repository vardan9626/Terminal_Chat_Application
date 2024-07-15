import os
import pty
import pygame
import pyte
import select
import sys

# Screen and process setup
screen = pyte.Screen(80, 24)
stream = pyte.ByteStream(screen)

# Create a pseudo-terminal pair
master_fd, slave_fd = pty.openpty()

# Fork a child process
pid = os.fork()
if pid == 0:  # Child process
    os.setsid()
    os.dup2(slave_fd, sys.stdin.fileno())
    os.dup2(slave_fd, sys.stdout.fileno())
    os.dup2(slave_fd, sys.stderr.fileno())
    os.execvp("/bin/bash", ["/bin/bash"])  # Replace bash with your preferred shell
else:  # Parent process
    os.close(slave_fd)

# Pygame window setup
pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 15)
window_size = (640, 480)
screen_surface = pygame.display.set_mode(window_size)
pygame.display.set_caption("Python Terminal")

running = True
while running:
    # Check for input from the terminal
    # Check for input from the terminal
    r, w, e = select.select([master_fd], [], [], 0)
    if master_fd in r:
        data = os.read(master_fd, 1024)
        # Ensure data is properly decoded before feeding
        if data:
            stream.feed(data)


    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                os.write(master_fd, event.unicode.encode())

    # Render terminal output
    screen_surface.fill((0, 0, 0))  # Black background
    for i, line in enumerate(screen.display):
        surface = font.render(line, True, (255, 255, 255))
        screen_surface.blit(surface, (0, i * 15))
    pygame.display.flip()

pygame.quit()

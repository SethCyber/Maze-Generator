import pygame
import random

pygame.init()
screen = pygame.display.set_mode((430*2 + 10, 430*2 + 10))
pygame.display.set_caption('Maze Generator (Hunt and Kill)')
clock = pygame.time.Clock()
screen.fill((255, 255, 255))

nodes = {}
width_and_height = 21


for row in range(width_and_height):
    first_index = 30 + 40 * row
    for col in range(width_and_height):
        second_index = 30 + 40 * col
        nodes[(first_index, second_index)] = True


def randomize(upper_limit: int) -> int:
    """Randomized number returned between and including 0 to upper_limit"""
    return random.randint(0, upper_limit)


start_pos = randomize(len(nodes) - 1)
coordinates = list(nodes)
current_point: tuple = list(nodes)[start_pos]
points_touched: list = list(nodes.values())
for point in range(len(points_touched)):
    points_touched[point] = False


def any_neighbors(coordinate: tuple) -> list:
    """Views points next to current point and returns point in of neighbor found"""
    available_spaces: list = []
    if (coordinate[0] + 40, coordinate[1]) in coordinates and not points_touched[coordinates.index((coordinate[0] + 40, coordinate[1]))]:
        available_spaces.append((coordinate[0] + 40, coordinate[1]))
        print('Right Appended')
    if (coordinate[0] - 40, coordinate[1]) in coordinates and not points_touched[coordinates.index((coordinate[0] - 40, coordinate[1]))]:
        available_spaces.append((coordinate[0] - 40, coordinate[1]))
        print('Left Appended')
    if (coordinate[0], coordinate[1] + 40) in coordinates and not points_touched[coordinates.index((coordinate[0], coordinate[1] + 40))]:
        available_spaces.append((coordinate[0], coordinate[1] + 40))
        print('Down Appended')
    if (coordinate[0], coordinate[1] - 40) in coordinates and not points_touched[coordinates.index((coordinate[0], coordinate[1] - 40))]:
        available_spaces.append((coordinate[0], coordinate[1] - 40))
        print('Up Appended')
    return available_spaces


def branch(coordinate: tuple) -> None:
    global current_point
    x_incrementer = -1
    y_incrementer = 1
    "Draw and extend line over to a random available neighbor"
    spaces = any_neighbors(coordinate)
    print(spaces)
    if len(spaces) == 0:
        hunt_kill()
        pass
    else:
        next_space = random.choice(spaces)
        if next_space == (coordinate[0] + 40, coordinate[1]):    # Right
            pygame.draw.line(screen, (255, 255, 255), (coordinate[0] + y_incrementer, coordinate[1] + 4 - x_incrementer), (coordinate[0] + 40 + y_incrementer, coordinate[1] + 4 - x_incrementer), 30)
            points_touched[coordinates.index(current_point)] = True
            points_touched[coordinates.index((coordinate[0] + 40, coordinate[1]))] = True
            current_point = (coordinate[0] + 40, coordinate[1])
        elif next_space == (coordinate[0] - 40, coordinate[1]):  # Left
            pygame.draw.line(screen, (255, 255, 255), (coordinate[0] + y_incrementer, coordinate[1] + 4 - x_incrementer), (coordinate[0] - 40 + y_incrementer, coordinate[1] + 4 - x_incrementer), 30)
            points_touched[coordinates.index(current_point)] = True
            points_touched[coordinates.index((coordinate[0] - 40, coordinate[1]))] = True
            current_point = (coordinate[0] - 40, coordinate[1])
        elif next_space == (coordinate[0], coordinate[1] + 40):  # Down
            pygame.draw.line(screen, (255, 255, 255), (coordinate[0] + 4 + y_incrementer, coordinate[1] - x_incrementer), (coordinate[0] + 4 + y_incrementer, coordinate[1] + 40 - x_incrementer), 30)
            points_touched[coordinates.index(current_point)] = True
            points_touched[coordinates.index((coordinate[0], coordinate[1] + 40))] = True
            current_point = (coordinate[0], coordinate[1] + 40)
        elif next_space == (coordinate[0], coordinate[1] - 40):  # Up
            pygame.draw.line(screen, (255, 255, 255), (coordinate[0] + 4 + y_incrementer, coordinate[1] - x_incrementer), (coordinate[0] + 4 + y_incrementer, coordinate[1] - 40 - x_incrementer), 30)
            points_touched[coordinates.index(current_point)] = True
            points_touched[coordinates.index((coordinate[0], coordinate[1] - 40))] = True
            current_point = (coordinate[0], coordinate[1] - 40)
        print('branched')


def hunt_kill():
    global current_point
    for i in range(len(nodes)):
        if len(any_neighbors(coordinates[i])) != 0 and points_touched[i]:
            current_point = coordinates[i]
            break
        else:
            pass


for node in nodes:
    pygame.draw.line(screen, (0, 0, 0), (node[0] - 15, node[1] - 15), (node[0] + 25, node[1] - 15), 10)
    pygame.draw.line(screen, (0, 0, 0), (node[0] - 15, node[1] + 25), (node[0] + 25, node[1] + 25), 10)
    pygame.draw.line(screen, (0, 0, 0), (node[0] - 15, node[1] - 15 - 4), (node[0] - 15, node[1] + 25+5), 10)
    pygame.draw.line(screen, (0, 0, 0), (node[0] + 25, node[1] - 15 - 4), (node[0] + 25, node[1] + 25+5), 10)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    all_points_touched = True
    for ui in range(len(nodes)):
        if points_touched[ui]:
            pass
        else:
            all_points_touched = False
    if all_points_touched:
        print('All touched')
        sides = randomize(0)
        if sides == 0:
            opening = randomize(width_and_height - 1)
            closing = randomize(width_and_height - 1)
            if opening == -1:
                opening = 0
            if closing == -1:
                closing = 0
            pygame.draw.line(screen, (255, 255, 255), (21 + 40 * opening, 15), (20 + 40 * opening + 30, 15), 10)
            pygame.draw.line(screen, (255, 255, 255), (21 + 40 * closing, coordinates[-1][1]+25), (20 + 40 * closing + 30, coordinates[-1][1]+25), 10)
            pygame.display.update()
        if sides == 1:
            pass
        input()
    else:
        branch(current_point)
    pygame.display.update()
    clock.tick(60)

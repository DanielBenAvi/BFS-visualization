import collections
from Arrow import draw_arrow
import pygame
import colordict
from networkx.generators.random_graphs import erdos_renyi_graph
import random

pygame.init()

'''
    Program Variables
'''
CLOCK = pygame.time.Clock()
FPS = 2
RADIUS = 15
WIDTH = 750
HEIGHT = 750
NODES_NUMBER = 10
NODES_PROBABILITY = 0.3
SPACING = WIDTH // (NODES_NUMBER + 1)  # spacing that the nodes won't go outside the window
COLORS = colordict.ColorDict()  # Dictionary with all the colors
g = erdos_renyi_graph(NODES_NUMBER, NODES_PROBABILITY, directed=True)  # random graph generator
EDGES = [e for e in g.edges]
NODES = [n for n in g.nodes]
FONT = pygame.font.Font('freesansbold.ttf', 16)
new_lines = []
new_nodes = []
root = '0'

'''
    Start pygame
'''
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BFS Algorithm')
run = False


def add_text_center(win, text, font, y, x, color):
    txt = font.render(text, True, color)
    txt_rect = txt.get_rect()
    txt_rect.center = (y, x)
    win.blit(txt, txt_rect)


def add_text_left(win, text, font, y, x, color):
    txt = font.render(text, True, color)
    txt_rect = txt.get_rect()
    txt_rect.topleft = (y, x)
    win.blit(txt, txt_rect)


'''
    Node class
'''


class Node:
    def __init__(self, y_value, x_value, text: str, font: pygame.font, neighbors: list):
        self.y = y_value
        self.x = x_value
        self.radius = RADIUS
        self.circle_width = 0
        self.text = text
        self.font = font
        self.neighbors = neighbors

    def draw_node(self, win: pygame.display, color: set):
        # Draw circle
        pygame.draw.circle(win, color, (self.y, self.x), self.radius, self.circle_width)

        # Draw text in the middle of the circle
        add_text_center(win, self.text, self.font, self.y, self.x, COLORS['black'])


'''
    Node class
'''


class Arrow:
    def __init__(self, start, end, line_width, start_node_name, end_node_name):
        self.start_node_name = start_node_name
        self.end_node_name = end_node_name
        self.start = start
        self.end = end
        self.line_width = line_width

    def draw_line(self, win: pygame.display, color: set):
        start = pygame.Vector2(self.start)
        end = pygame.Vector2(self.end)
        draw_arrow(win, start, end, color, self.line_width)


def n_to_d(nodes, edges) -> dict:
    dct = {}
    for nd in nodes:
        lst = [str(x[1]) if x[0] == nd else None for x in edges]
        lst = list(filter(lambda x: x is not None, lst))
        dct[str(nd)] = lst
    return dct


def create_dict_of_places(nodes, num_of_nodes, spacing, ) -> dict:
    tmp_dict = {}
    for index in range(len(nodes)):
        y = (index + 1) * spacing
        x = SPACING * random.randint(1, num_of_nodes)
        node_name = str(list(nodes)[index])
        tmp_dict[node_name] = (y, x)
    return tmp_dict


def create_list_of_lines_and_nodes_objects(nodes_and_place, nodes, edges):
    for ln in edges:
        start_pos = nodes_and_place.get(str(ln[0]))
        end_pos = nodes_and_place.get(str(ln[1]))
        new_lines.append(Arrow(start_pos, end_pos, 2, str(ln[0]), str(ln[1])))

    for index in range(len(nodes)):
        y, x = nodes_and_place[str(index)]
        new_nodes.append(Node(y, x, str(index), FONT, n_to_d(nodes, edges)[str(index)]))


def draw(base: str, visit_set: set, queue_lst: collections.deque[str]):
    line_color = COLORS['teal']
    start_color = COLORS['green']
    visit_color = COLORS['yellow']
    queue_color = COLORS['blue']
    regular_color = COLORS['white']
    for line in new_lines:
        line.draw_line(window, queue_color if (
                line.start_node_name in queue_lst and line.end_node_name in queue_lst) else visit_color if (
                line.start_node_name in visit_set and line.end_node_name in visit_set) else line_color)

    for count, node in enumerate(new_nodes):
        node.draw_node(window, start_color if str(count) == base else queue_color if str(
            count) in queue_lst else visit_color if str(count) in visit_set else regular_color)


# Dictionary to store all nodes names and center
dict_of_nodes_and_place = create_dict_of_places(NODES, NODES_NUMBER, SPACING)
create_list_of_lines_and_nodes_objects(dict_of_nodes_and_place, NODES, EDGES)

'''
    game loop
'''
graph = n_to_d(NODES, EDGES)  # the main graph we are working on
visited = set()  # empty set
queue = collections.deque([root])  # creates a root with the root inside
visited.add(root)  # add the root to visited
algorithm = False
order_text = 'Order: '

while not run:
    CLOCK.tick(FPS)
    window.fill(COLORS['black'])
    add_text_left(window, 'Press SPACE to start', FONT, 25, 25, COLORS['white'])
    '''
        BNF Start
    '''
    if algorithm:
        if queue:  # if queue in not empty
            vertex = queue.popleft()
            order_text = order_text + str(vertex) + " "

            for neighbour in graph[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
    '''
        BNF End
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                algorithm = True

            if event.key == pygame.K_ESCAPE:
                run = True

    draw(root, visited, queue)
    add_text_left(window, order_text, FONT, 25, 50, COLORS['white'])
    pygame.display.update()

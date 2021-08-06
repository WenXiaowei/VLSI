import numpy as np
import matplotlib.pyplot as plt
import cv2
import matplotlib.patches as mpatches



def read_instance_text(f):
    print(f)
    file = open(f)
    width = int(file.readline())
    # print("width ", width)
    n_piece = int(file.readline())
    pieces = []
    for i in range(n_piece):
        piece = file.readline()
        split_piece = piece.strip().split(" ")
        pieces.append(int(split_piece[0]))
        pieces.append(int(split_piece[1]))
    # print(pieces)
    return width, pieces


def write_dzn(width, pieces, out_path="./file.dzn"):
    file = open(out_path, mode="w")
    file.write(f"width = {width};\n")
    n_circuits = int(len(pieces) / 2)
    file.write(f"n_circuits = {n_circuits};\n")
    file.write(f"dims = [|")
    for i in range(n_circuits):
            file.write(f" {pieces[2*i]},{pieces[2*i+1]}|")
    file.write("];")
    file.close()


def read_solution_parameters(f):
    file = open(f)
    line = file.readline()
    hw = line.strip().split(" ")
    dim = (int(hw[0]), int(hw[1]))
    n_circuits = int(file.readline())
    coordinates = []
    for i in range(n_circuits):
        line = file.readline()
        split_line = line.replace("\n", "").split(" ")
        if len(split_line) == 4:
            coordinates.append(tuple(map(int, split_line)))

    # print(coordinates)
    return dim, n_circuits, coordinates


def show_shape(s, title, n_circuits):
    """
    create a image with s as image and title as title of the graph
    :param s:
    :param title:
    :param n_circuits:
    :return:
    """
    s = cv2.merge([s])
    img = plt.imshow(s)

    values, counts = np.unique(s, return_counts=True)
    # print(counts)
    colors = [img.cmap(img.norm(value)) for value in values]
    labels = []
    starting = 0
    if n_circuits + 1 == len(counts):
        starting = 1
        labels.append("Background")
    for i in range(starting, len(counts)):
        labels.append(f"Piece {i + 1}")
    patches = [mpatches.Patch(color=colors[i], label=labels[i]) for i in range(len(counts))]
    plt.title(title)
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(list(range(0, s.shape[1] + 1)))
    yticks = list(range(0, s.shape[0]))
    # yticks.reverse()
    plt.yticks(yticks)
    plt.ylim(top=s.shape[0])
    plt.ylim(bottom=-0.5)
    plt.xlim(left=-0.5)
    plt.xlim(right=s.shape[1])
    plt.gca().invert_yaxis()
    # plt.grid(b=True)
    plt.savefig(f"{title}")

    # plt.show()


def draw_solution(sol_shape, pieces):
    arr = np.zeros(sol_shape)
    count = 1
    area = 0
    for x_t, y_t, x, y in pieces:
        # if x == 1:
        #     x = 0
        # if y == 1:
        #     y = 0
        area += x_t * y_t
        # print(x_t, y_t, x, y)
        arr[x:x + x_t, y:y + y_t] = abs(count) * (250 / len(pieces))
        count += 1
        # print(arr)
    print(area)
    arr = arr / np.max(arr)
    return np.rot90(arr)
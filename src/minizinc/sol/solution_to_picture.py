import os
import re
from utilities.tools import *
import sys

if __name__ == "__main__":
    in_path = "./"
    out_path = "./"
    if len(sys.argv) >= 2:
        in_path = sys.argv[1]
    if len(sys.argv) == 3:
        out_path = sys.argv[2]
    # files = os.listdir(in_path)
    heights = {}
    # sol_n = 1
    # files = [f"sol-{sol_n}.txt" for sol_n in range(33,35)]
    files = os.listdir()
    for f in files:
        obj = re.search("^sol-[0-9]+.txt", f)
        if obj is not None:
            print(f)
            dim, n_circuits, shapes = read_solution_parameters(f)
            heights[f] = dim[1]
            solution, area = draw_solution(dim, shapes)
            # print(solution)
            new_f = f.replace("txt", "png")
            # show_shape(solution, new_f, n_circuits,shapes)
            print(f"found area == circuits area sum: {dim[0]*dim[1] == area}")
    print(heights)
else:
    print("Error")

Created by James Prial,

USAGE: to launch, type “python3 Driver.py” in a terminal within the directory containing the source code.
From there, the program will prompt you with instructions, first if you want to generate grids, then the path to
The grid being searched over, and finally the type of search to perform. The path will be written out in the terminal, and a visual representation will pop up to display the path. When the popup is closed out, the program will loop back to the beginning



A* implementation: In order to get A* to work, the first thing that was necessary to implement was an adequate representation of the grid and its vertices. This was implemented using two 2-D arrays, one corresponding to the cells and whether they were blocked or not, the other the vertices. Next, for actually implementing the search algorithm, the key was designing the priority queue. Initializing the g(x) and h(x) values was fairly trivial, so what was essential was a proper implementation of the queue to ensure the neighbor with the best f value is selected. With that implemented, the rest was largely similar to the given psuedocode for A*.
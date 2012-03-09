import Image,ImageDraw
import random
import array
import copy
import numpy
import Tkinter as tk
    
def drawmaze(maze):
    w = len(maze);
    h = len(maze[1]);
    img = Image.new("RGB", [w*4,h*4], 'white')
    draw = ImageDraw.Draw(img)

    for i in range(w):
        for j in range(h):
            for k in range(4):
                # Wall
                if maze[i][j] == 1:
                    draw.line([((4*i)+k,(4*j)),((4*i)+k,(4*j)+3)], fill=('black'));
                # Visited, used in reverse backtracker
                if maze[i][j] == 0.5:
                    draw.line([((4*i)+k,(4*j)),((4*i)+k,(4*j)+3)], fill=('white'));
                # Exit cell
                if maze[i][j] == 2:
                    draw.line([((4*i)+k,(4*j)),((4*i)+k,(4*j)+3)], fill=('red'));
                # Entrance cell
                if maze[i][j] == 3:
                    draw.line([((4*i)+k,(4*j)),((4*i)+k,(4*j)+3)], fill=('green'));
                # Solution path - first cross
                if maze[i][j] == -1:
                    draw.line([((4*i)+k,(4*j)),((4*i)+k,(4*j)+3)], fill=('yellow'));
                # Solution path - second cross
                if maze[i][j] == -2:
                    draw.line([((4*i)+k,(4*j)),((4*i)+k,(4*j)+3)], fill=('orange'));
    img.save("maze.png","PNG")

def cleanmaze(maze):
    h = len(maze[0])
    w = len(maze)

    for i in range(0,w):
        for j in range(0,h):
            if maze[i][j] == 0.5:
                maze[i][j] = 0
            if maze[i][j] == 0.1:
                maze[i][j] = 0
            if maze[i][j] > 3:
                maze[i][j] = 0

    return maze

def mazegen_blank(h,w):
    wall = []
    for i in range(0,(h*2)+1):
        wall.append(1);
    maze = [0]*((2*w)+1)
    maze[0] = wall;
    tilewall = []
    for i in range(0,h):
        tilewall.append(1);
        tilewall.append(0);
    tilewall.append(1);
    for i in range(1,w+1):
        newwall = tilewall[:]
        newblock = wall[:]
        maze[(2*i)-1] = newwall;
        maze[(2*i)] = newblock;
    return maze;

def randomexitcell(maze,h,w,val):
    wall = random.randint(1,4)
    if wall==1:
        exitcell = [(random.randint(1,w)*2)-1,1]
        maze[exitcell[0]][0] = val
    if wall==2:
        exitcell = [(w*2)-1,(random.randint(1,h)*2)-1]
        maze[w*2][exitcell[1]] = val
    if wall==3:
        exitcell = [(random.randint(1,w)*2)-1,(h*2)-1]
        maze[exitcell[0]][h*2] = val
    if wall==4:
        exitcell = [1,(random.randint(1,h)*2)-1]
        maze[0][exitcell[1]] = val

    return exitcell,maze

def goodencell(maze,h,w,val,exitcell):
    encell = []
    if (exitcell[0] == 1):
        encell = [(w*2)-1,(random.randint(1,h)*2) - 1]
        maze[(w*2)][encell[1]] = val
    if (exitcell[0] == (2*w)-1):
        encell = [1,(random.randint(1,h)*2) - 1]
        maze[0][encell[1]] = val
    if (exitcell[1] == 1):
        encell = [(random.randint(1,w)*2) - 1,(h*2)-1]
        maze[encell[0]][(h*2)] = val
    if (exitcell[1] == (2*h)-1):
        encell = [(random.randint(1,w)*2) - 1,1]
        maze[encell[0]][0] = val

    return encell,maze

def mazegen_rb(h,w):
    maze = mazegen_blank(h,w)
    exitcell,maze = randomexitcell(maze,h,w,2)
    stack = []
    x = exitcell[0]
    y = exitcell[1]
    first = 1
    visited = maze[:]
    visited[x][y] = 0.5
    coords = []
    print exitcell

    while ((len(stack)>0)&(coords!=exitcell))|(first == 1):
        coords,stack = rb_addtostack(maze,stack,visited,x,y,h,w)
        # if (coords[0]==x)|(coords[1]==y):
            # maze[(coords[0]+x)/2][(coords[1]+y)/2] = 0
        x = coords[0]
        y = coords[1]

        visited[x][y] = 0.5
        first = 0

    encell,maze = goodencell(maze,h,w,3,exitcell)
    print encell

    return maze

def rb_addtostack(maze,stack,visited,x,y,h,w):
    possible = []
    # North
    if (maze[x][y-1] == 1)&(y>1):
        if (visited[x][y-2]!=0.5):
            possible.append([x,y-2])
    # West
    if (maze[x-1][y] == 1)&(x>1):
        if (visited[x-2][y]!=0.5):
            possible.append([x-2,y])
    # South
    if (maze[x][y+1] == 1)&(y<(h*2)-1):
        if (visited[x][y+2]!=0.5):
            possible.append([x,y+2])
    # East
    if (maze[x+1][y] == 1)&(x<(w*2)-1):
        if (visited[x+2][y]!=0.5):
            possible.append([x+2,y])

    # Choose a random possibility
    num = len(possible)
    if (num>0):
        chosen = possible[random.randint(0,num-1)]
        stack.append(chosen)
        maze[(chosen[0]+x)/2][(chosen[1]+y)/2] = 0
        return chosen,stack
    else:
        old = stack.pop()
        return old,stack

def mazegen_kruskal(h,w):
    maze = mazegen_blank(h,w)
    exitcell,maze = randomexitcell(maze,h,w,2)
    print exitcell

    # Unique ID generator
    ids = numpy.zeros(h*w,int)
    for i in range(0,len(ids)):
        ids[i] = i+1

    # Wall list generator
    numwalls = (w*(h-1))+(h*(w-1))
    walls = list()

    # Unique wall ID generator
    wids = numpy.zeros(numwalls,int)
    for i in range(0,len(wids)):
        wids[i] = i

    for j in range(1,w+1):
        for k in range(1,h+1):
            done = 0
            while (done == 0):
                num = random.randint(0, len(ids)-1)
                if (ids[num] != 0):
                    maze[(j*2)-1][(k*2)-1] = ids[num] + 3
                    ids[num] = 0
                    done = 1

    row = 1
    col = 2
    for l in range(1,numwalls+1):
        walls.append([row,col])
        if (col >= (2*w)-2):
            row = row + 1
            if (row%2 == 0):
                col = 1
            else:
                col = 2
        else:
            col = col + 2

    # Start the process

    on = 1
    while (on <= numwalls*10):
        # Choose a random wall ID from wids
        done = 0
        while (done == 0):
            wallid = random.randint(0, len(wids)-1)
            if (wallid != 0):
                wids[wallid] = 0
                done = 1

        # Compare adjacent cells, odd rows are vertical
        x = walls[wallid][0]
        y = walls[wallid][1]

        if (y%2 == 0):
            c1 = [x,y-1]
            c2 = [x,y+1]
        else:
            c1 = [x-1,y]
            c2 = [x+1,y]

        if (maze[c1[0]][c1[1]] != maze[c2[0]][c2[1]]):
            maze[x][y] = 0
            val = maze[c1[0]][c1[1]]
            x = c2[0]
            y = c2[1]

            kruskal_changer(maze,x,y,h,w,val)

        on = on + 1
          
    encell,maze = goodencell(maze,h,w,3,exitcell)
    print encell

    return maze

def kruskal_changer(maze,x,y,h,w,val):
    maze[x][y] = val
    # North
    if (maze[x][y-1] == 0)&(y>1):
        if (maze[x][y-2] != val):
            kruskal_changer(maze,x,y-2,h,w,val)
    # West
    if (maze[x-1][y] == 0)&(x>1):
        if (maze[x-2][y] != val):
            kruskal_changer(maze,x-2,y,h,w,val)
    # South
    if (maze[x][y+1] == 0)&(y<(h*2)-1):
        if (maze[x][y+2] != val):
            kruskal_changer(maze,x,y+2,h,w,val)
    # East
    if (maze[x+1][y] == 0)&(x<(w*2)-1):
        if (maze[x+2][y] != val):
            kruskal_changer(maze,x+2,y,h,w,val)

def mazegen_prim(h,w):
    maze = mazegen_blank(h,w)
    exitcell,maze = randomexitcell(maze,h,w,2)
    print exitcell

    # 0-Out, 0.1-Frontier, 0.5-In

    x = exitcell[0]
    y = exitcell[1]

    maze[x][y] = 0.5

    frontier = []
    maze,frontier = prim_frontier(maze,frontier,x,y,h,w)

    while(len(frontier) > 0):
        rint = random.randint(0,len(frontier)-1)
        cell = frontier.pop(rint)
        x=cell[0]
        y=cell[1]
        maze = prim_remove(maze,x,y,h,w)
        maze[x][y] = 0.5
        
        maze,frontier = prim_frontier(maze,frontier,x,y,h,w)

    

    encell,maze = goodencell(maze,h,w,3,exitcell)
    print encell

    return maze

def prim_frontier(maze,frontier,x,y,h,w):
    maze[x][y] = 0.5
    # North
    if (maze[x][y-1] == 1)&(y>1):
        if maze[x][y-2] == 0:
            frontier.append([x,y-2])
            maze[x][y-2] = 0.1
    # West
    if (maze[x-1][y] == 1)&(x>1):
        if maze[x-2][y] == 0:
            frontier.append([x-2,y])
            maze[x-2][y] = 0.1
    # South
    if (maze[x][y+1] == 1)&(y<(h*2)-1):
        if maze[x][y+2] == 0:
            frontier.append([x,y+2])
            maze[x][y+2] = 0.1
    # East
    if (maze[x+1][y] == 1)&(x<(w*2)-1):
        if maze[x+2][y] == 0:
            frontier.append([x+2,y])
            maze[x+2][y] = 0.1

    return maze,frontier

def prim_remove(maze,x,y,h,w):
    possible = []
    # North
    if (maze[x][y-1] == 1)&(y>1):
        if maze[x][y-2] == 0.5:
            possible.append([x,y-2])
    # West
    if (maze[x-1][y] == 1)&(x>1):
        if maze[x-2][y] == 0.5:
            possible.append([x-2,y])
    # South
    if (maze[x][y+1] == 1)&(y<(h*2)-1):
        if maze[x][y+2] == 0.5:
            possible.append([x,y+2])
    # East
    if (maze[x+1][y] == 1)&(x<(w*2)-1):
        if maze[x+2][y] == 0.5:
            possible.append([x+2,y])

    if len(possible) > 0:
        rint = random.randint(0,len(possible)-1)
        cell = possible[rint]
        cx = cell[0]
        cy = cell[1]

        maze[(x+cx)/2][(y+cy)/2] = 0

    return maze    

def mazesolve_follow(maze,encell,exitcell):
    x = encell[0]
    y = encell[1]

    cell = encell

    h = (len(maze[0])-1)/2
    w = (len(maze)-1)/2

    # 0 N 1 E 2 S 3 W
    d = 0
    if (y==2*h):
        d = 0
    if (x==1):
        d = 1
    if (y==1):
        d = 2
    if (x==2*w):
        d = 3
    
    while cell!=exitcell:
        x,y,d = mazesolve_follow_recurse(maze,h,w,x,y,d)
        if (maze[x][y] == -1):
            maze[x][y] = -2
        else:
            maze[x][y] = -1
        if d==0:
            if maze[x][y+1] != -1:
                maze[x][y+1] = -1
            else:
                maze[x][y+1] = -2
        if d==1:
            if maze[x-1][y] != -1:
                maze[x-1][y] = -1
            else:
                maze[x-1][y] = -2
        if d==2:
            if maze[x][y-1] != -1:
                maze[x][y-1] = -1
            else:
                maze[x][y-1] = -2
        if d==3:
            if maze[x+1][y] != -1:
                maze[x+1][y] = -1
            else:
                maze[x+1][y] = -2
        cell = [x,y]
        # drawmaze(maze)

    return maze

def mazesolve_follow_recurse(maze,h,w,x,y,d):
    possible = []
    # North
    if (maze[x][y-1]<=0)&(y>1):
        possible.append([x,y-2,0])
    # West
    if (maze[x-1][y] <= 0)&(x>1):
        possible.append([x-2,y,3])
    # South
    if (maze[x][y+1] <= 0)&(y<(h*2)-1):
        possible.append([x,y+2,2])
    # East
    if (maze[x+1][y] <= 0)&(x<(w*2)-1):
        possible.append([x+2,y,1])

    if d==3:
        turnd = 0
    else:
        turnd = d+1

    if len(possible) == 1:
        x = possible[0][0]
        y = possible[0][1]
        d = possible[0][2]

    if len(possible) == 2:
        if (possible[0][2]==turnd):
            x = possible[0][0]
            y = possible[0][1]
            d = possible[0][2]
        elif (possible[1][2]==turnd):
            x = possible[1][0]
            y = possible[1][1]
            d = possible[1][2]
        elif (possible[0][2]==d+2)|(possible[0][2]==d-2):
            x = possible[1][0]
            y = possible[1][1]
            d = possible[1][2]
        else:
            x = possible[0][0]
            y = possible[0][1]
            d = possible[0][2]

    else:
        setbest = 0
        for i in range(0,len(possible)):
            if possible[i][2] == turnd:
                x = possible[i][0]
                y = possible[i][1]
                d = possible[i][2]
                setbest = 1

        if setbest == 0:
            for i in range(0,len(possible)):
                if possible[i][2] == d:
                    x = possible[i][0]
                    y = possible[i][1]

    return x,y,d

if __name__ == "__main__":
    print "nothing";

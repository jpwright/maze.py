#Boa:Frame:mainframe

import wx
import wx.lib.flatnotebook
import wx.media
from wx.lib.anchors import LayoutAnchors
import wx.lib.buttons
from myro import *
import Image,ImageDraw
import random
import array
import copy
import numpy
import Tkinter as tk
import results
import socket


# MAZE ALGORITHM STUFF

def calculate(dec):
        print 'Directional command given, direction is %d' % dec
        global n
        global m
        global pos
        global prev
        global pd
        
        x = pos[0]
        y = pos[1]
        px = prev[0]
        py = prev[1]
        
        global en
        ex = en[0]
        ey = en[1]
        
        print 'Current cell is %d,%d' % (x,y)
        print 'Previous cell is %d,%d' % (px,py)
        print 'Previous direction is %d' % pd
        if (pd == -1):
            pd = dec
        else:            
            nx = x
            ny = y
            if(dec == 0):
                ny = y-2
            elif(dec == 1):
                nx = x+2
            elif(dec == 2):
                ny = y+2
            elif(dec == 3):
                nx = x-2
                
            if(pd==0):
                wf = m[x+1][y]
                wb = m[x-1][y]
                wl = m[x][y-1]
                wr = m[x][y+1]
            if(pd==1):
                wr = m[x][y+1]
                wl = m[x][y-1]
                wf = m[x+1][y]
                wb = m[x-1][y]
            if(pd==2):
                wr = m[x-1][y]
                wl = m[x+1][y]
                wf = m[x][y+1]
                wb = m[x][y-1]
            if(pd==3):
                wr = m[x][y-1]
                wl = m[x][y+1]
                wf = m[x-1][y]
                wb = m[x+1][y]
            
            # right following
            global right
            v = 0
            right_num = right * n
            if (wr != 1):
                if ((dec == (pd+1)) | ((dec == 0)&(pd==3))):
                    v = 1
            if (wr & (wf != 1)):
                if (dec == pd):
                    v = 1
            if (wr & (wf & (wl != 1))):
                if ((dec == (pd-1)) | ((dec == 3)&(pd==0))):
                    v = 1
            if (wr & wf & wl):
                v = 1
            
            print 'Right-follow algorithm? %d' % v
            #print 'number of correct so far: $d' % right_num
            right_num = right_num + v

            #other stuff
            n = n+1
            print 'number of trials: %d' % n
            right = float(right_num)/float(n)
            print 'accuracy: %d' % right

def drawmaze(maze):
    w = len(maze);
    h = len(maze[1]);
    img = Image.new("RGB", [w*16,h*16], 'white')
    draw = ImageDraw.Draw(img)

    for i in range(w):
        for j in range(h):
            for k in range(16):
                # Wall
                if maze[i][j] == 1:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('black'));
                # Visited, used in reverse backtracker
                if maze[i][j] == 0.5:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('white'));
                # Exit cell
                if maze[i][j] == 2:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('red'));
                # Entrance cell
                if maze[i][j] == 3:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('green'));
                # Solution path - first cross
                if maze[i][j] == -1:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('yellow'));
                # Solution path - second cross
                if maze[i][j] == -2:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('orange'));
                # Position
                if maze[i][j] == -3:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('blue'));
                # Visited path
                if maze[i][j] == -4:
                    draw.line([((16*i)+k,(16*j)),((16*i)+k,(16*j)+15)], fill=('dodgerblue'));
    img.save("C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png","PNG")

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
    global ex
    ex = exitcell

    while ((len(stack)>0)&(coords!=exitcell))|(first == 1):
        coords,stack = rb_addtostack(maze,stack,visited,x,y,h,w)
        # if (coords[0]==x)|(coords[1]==y):
            # maze[(coords[0]+x)/2][(coords[1]+y)/2] = 0
        x = coords[0]
        y = coords[1]

        visited[x][y] = 0.5
        first = 0

    encell,maze = goodencell(maze,h,w,3,exitcell)
    global en
    en = encell

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
    global ex
    ex = exitcell

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
    global en
    en = encell

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
    global ex
    ex = exitcell

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
    global en
    en = encell

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

def mazesolve_follow(maze):

    h = (len(maze[0])-1)/2
    w = (len(maze)-1)/2
    
    encell = en
    exitcell = ex
                
    x = encell[0]
    y = encell[1]

    cell = encell

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

def create(parent):
    return mainframe(parent)

[wxID_MAINFRAME, wxID_MAINFRAMEAUTOBUTTON, wxID_MAINFRAMEAUTOLABEL, 
 wxID_MAINFRAMEBATTERY, wxID_MAINFRAMEBATTERYLABEL, wxID_MAINFRAMEEXECUTE, 
 wxID_MAINFRAMEGETPEN, wxID_MAINFRAMEHEADER, wxID_MAINFRAMEHEIGHT, 
 wxID_MAINFRAMEIMG, wxID_MAINFRAMEIMGCHOICE, wxID_MAINFRAMEIMGLABEL, 
 wxID_MAINFRAMEIMGTAKER, wxID_MAINFRAMEIMGTYPELABEL, wxID_MAINFRAMEINIT, 
 wxID_MAINFRAMEIR1, wxID_MAINFRAMEIR1LABEL, wxID_MAINFRAMEIR2, 
 wxID_MAINFRAMEIR2LABEL, wxID_MAINFRAMEIRLABEL, wxID_MAINFRAMELIGHT1, 
 wxID_MAINFRAMELIGHT1LABEL, wxID_MAINFRAMELIGHT2, wxID_MAINFRAMELIGHT2LABEL, 
 wxID_MAINFRAMELIGHT3, wxID_MAINFRAMELIGHT3LABEL, wxID_MAINFRAMELIGHTLABEL, 
 wxID_MAINFRAMEMAZE, wxID_MAINFRAMEMAZEGEN, wxID_MAINFRAMEMAZEGENCHOICE, 
 wxID_MAINFRAMEMAZEGENHEIGHTLABEL, wxID_MAINFRAMEMAZEGENLABEL, 
 wxID_MAINFRAMEMAZEGENWIDTHLABEL, wxID_MAINFRAMEMAZELABEL, 
 wxID_MAINFRAMEMAZESOLVELABEL, wxID_MAINFRAMEMOTIONDOWN, 
 wxID_MAINFRAMEMOTIONGAMEPAD, wxID_MAINFRAMEMOTIONJOYSTICK, 
 wxID_MAINFRAMEMOTIONLABEL, wxID_MAINFRAMEMOTIONLEFT, 
 wxID_MAINFRAMEMOTIONRIGHT, wxID_MAINFRAMEMOTIONUP, wxID_MAINFRAMEMS_DOWN, 
 wxID_MAINFRAMEMS_LEFT, wxID_MAINFRAMEMS_RIGHT, wxID_MAINFRAMEMS_UP, 
 wxID_MAINFRAMEPANEL1, wxID_MAINFRAMEREAD, wxID_MAINFRAMEREALLYMOVE, 
 wxID_MAINFRAMERESULTS, wxID_MAINFRAMEROBOTSETTINGSHEADER, 
 wxID_MAINFRAMESENSORLABEL, wxID_MAINFRAMESERVERCONNECT, wxID_MAINFRAMESOLVE, 
 wxID_MAINFRAMESTALL, wxID_MAINFRAMESTALLLABEL, wxID_MAINFRAMETEACHINGBUTTON, 
 wxID_MAINFRAMETEACHINGLABEL, wxID_MAINFRAMETEACHINGSOURCE, 
 wxID_MAINFRAMEUSEPEN, wxID_MAINFRAMEWIDTH, 
] = [wx.NewId() for _init_ctrls in range(61)]

class mainframe(wx.Frame):
    
    dir = 0
    

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name='mainframe',
              parent=prnt, pos=wx.Point(296, 4), size=wx.Size(953, 976),
              style=wx.DEFAULT_FRAME_STYLE, title='Maze')
        self.SetClientSize(wx.Size(945, 942))
        self.Enable(True)

        self.panel1 = wx.Panel(id=wxID_MAINFRAMEPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(945, 942),
              style=wx.TAB_TRAVERSAL)

        self.img = wx.StaticBitmap(bitmap=wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/camera.jpg',
              wx.BITMAP_TYPE_JPEG), id=wxID_MAINFRAMEIMG, name='img',
              parent=self.panel1, pos=wx.Point(16, 72), size=wx.Size(256, 192),
              style=0)
        self.img.SetMinSize(wx.Size(256, 192))
        self.img.SetToolTipString('img')

        self.header = wx.StaticText(id=wxID_MAINFRAMEHEADER,
              label='Scribbler Maze Interface', name='header',
              parent=self.panel1, pos=wx.Point(16, 16), size=wx.Size(233, 23),
              style=0)
        self.header.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.imgLabel = wx.StaticText(id=wxID_MAINFRAMEIMGLABEL,
              label='IPRE Fluke Camera', name='imgLabel', parent=self.panel1,
              pos=wx.Point(16, 56), size=wx.Size(106, 13), style=0)
        self.imgLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.imgChoice = wx.Choice(choices=["Color", "Grayscale", "Blob"],
              id=wxID_MAINFRAMEIMGCHOICE, name='imgChoice', parent=self.panel1,
              pos=wx.Point(16, 296), size=wx.Size(130, 21), style=0)
        self.imgChoice.SetSelection(0)

        self.imgTypeLabel = wx.StaticText(id=wxID_MAINFRAMEIMGTYPELABEL,
              label='Image Type', name='imgTypeLabel', parent=self.panel1,
              pos=wx.Point(24, 272), size=wx.Size(57, 13), style=0)

        self.imgTaker = wx.Button(id=wxID_MAINFRAMEIMGTAKER,
              label='Take Picture', name='imgTaker', parent=self.panel1,
              pos=wx.Point(160, 288), size=wx.Size(107, 32), style=0)
        self.imgTaker.Enable(False)
        self.imgTaker.Bind(wx.EVT_LEFT_UP, self.OnImgTakerLeftUp)

        self.init = wx.Button(id=wxID_MAINFRAMEINIT, label='Initialize Robot',
              name='init', parent=self.panel1, pos=wx.Point(304, 80),
              size=wx.Size(128, 32), style=0)
        self.init.Bind(wx.EVT_LEFT_UP, self.OnInitLeftUp)

        self.robotSettingsHeader = wx.StaticText(id=wxID_MAINFRAMEROBOTSETTINGSHEADER,
              label='Robot Settings', name='robotSettingsHeader',
              parent=self.panel1, pos=wx.Point(304, 56), size=wx.Size(84, 13),
              style=0)
        self.robotSettingsHeader.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.BOLD, False, 'Tahoma'))

        self.motionLabel = wx.StaticText(id=wxID_MAINFRAMEMOTIONLABEL,
              label='Motion', name='motionLabel', parent=self.panel1,
              pos=wx.Point(24, 352), size=wx.Size(39, 13), style=0)
        self.motionLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.motionJoystick = wx.Button(id=wxID_MAINFRAMEMOTIONJOYSTICK,
              label='Open Joystick Control', name='motionJoystick',
              parent=self.panel1, pos=wx.Point(24, 376), size=wx.Size(128, 23),
              style=0)
        self.motionJoystick.Enable(False)
        self.motionJoystick.Bind(wx.EVT_LEFT_UP, self.OnMotionJoystickLeftUp)

        self.motionGamepad = wx.Button(id=wxID_MAINFRAMEMOTIONGAMEPAD,
              label='Open Gamepad Control', name='motionGamepad',
              parent=self.panel1, pos=wx.Point(160, 376), size=wx.Size(128, 23),
              style=0)
        self.motionGamepad.Enable(False)
        self.motionGamepad.Bind(wx.EVT_LEFT_UP, self.OnMotionGamepadLeftUp)

        self.motionUp = wx.Button(id=wxID_MAINFRAMEMOTIONUP, label='p',
              name='motionUp', parent=self.panel1, pos=wx.Point(128, 416),
              size=wx.Size(56, 48), style=0)
        self.motionUp.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Wingdings 3'))
        self.motionUp.Enable(False)
        self.motionUp.Bind(wx.EVT_LEFT_UP, self.OnMotionUpLeftUp)

        self.motionDown = wx.Button(id=wxID_MAINFRAMEMOTIONDOWN, label='q',
              name='motionDown', parent=self.panel1, pos=wx.Point(128, 464),
              size=wx.Size(56, 48), style=0)
        self.motionDown.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Wingdings 3'))
        self.motionDown.Enable(False)
        self.motionDown.Bind(wx.EVT_LEFT_UP, self.OnMotionDownLeftUp)

        self.motionLeft = wx.Button(id=wxID_MAINFRAMEMOTIONLEFT, label='t',
              name='motionLeft', parent=self.panel1, pos=wx.Point(72, 440),
              size=wx.Size(56, 48), style=0)
        self.motionLeft.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Wingdings 3'))
        self.motionLeft.Enable(False)
        self.motionLeft.Bind(wx.EVT_LEFT_UP, self.OnMotionLeftLeftUp)

        self.motionRight = wx.Button(id=wxID_MAINFRAMEMOTIONRIGHT, label='u',
              name='motionRight', parent=self.panel1, pos=wx.Point(184, 440),
              size=wx.Size(56, 48), style=0)
        self.motionRight.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Wingdings 3'))
        self.motionRight.Enable(False)
        self.motionRight.Bind(wx.EVT_LEFT_UP, self.OnMotionRightLeftUp)

        self.sensorLabel = wx.StaticText(id=wxID_MAINFRAMESENSORLABEL,
              label='Sensors', name='sensorLabel', parent=self.panel1,
              pos=wx.Point(16, 536), size=wx.Size(45, 13), style=0)
        self.sensorLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.read = wx.Button(id=wxID_MAINFRAMEREAD, label='Read Sensors',
              name='read', parent=self.panel1, pos=wx.Point(96, 800),
              size=wx.Size(123, 39), style=0)
        self.read.Enable(False)
        self.read.Bind(wx.EVT_LEFT_UP, self.OnReadLeftUp)

        self.light1 = wx.Gauge(id=wxID_MAINFRAMELIGHT1, name='light1',
              parent=self.panel1, pos=wx.Point(64, 584), range=30000,
              size=wx.Size(72, 16), style=wx.GA_HORIZONTAL)

        self.light1Label = wx.StaticText(id=wxID_MAINFRAMELIGHT1LABEL,
              label='Left', name='light1Label', parent=self.panel1,
              pos=wx.Point(16, 584), size=wx.Size(19, 13), style=0)

        self.lightLabel = wx.StaticText(id=wxID_MAINFRAMELIGHTLABEL,
              label='Light', name='lightLabel', parent=self.panel1,
              pos=wx.Point(64, 560), size=wx.Size(24, 13), style=0)
        self.lightLabel.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.light2Label = wx.StaticText(id=wxID_MAINFRAMELIGHT2LABEL,
              label='Middle', name='light2Label', parent=self.panel1,
              pos=wx.Point(16, 608), size=wx.Size(30, 13), style=0)

        self.light2 = wx.Gauge(id=wxID_MAINFRAMELIGHT2, name='light2',
              parent=self.panel1, pos=wx.Point(64, 608), range=30000,
              size=wx.Size(72, 16), style=wx.GA_HORIZONTAL)

        self.light3Label = wx.StaticText(id=wxID_MAINFRAMELIGHT3LABEL,
              label='Right', name='light3Label', parent=self.panel1,
              pos=wx.Point(16, 632), size=wx.Size(25, 13), style=0)

        self.light3 = wx.Gauge(id=wxID_MAINFRAMELIGHT3, name='light3',
              parent=self.panel1, pos=wx.Point(64, 632), range=30000,
              size=wx.Size(72, 16), style=wx.GA_HORIZONTAL)

        self.irLabel = wx.StaticText(id=wxID_MAINFRAMEIRLABEL, label='IR',
              name='irLabel', parent=self.panel1, pos=wx.Point(72, 672),
              size=wx.Size(11, 13), style=0)
        self.irLabel.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL, False,
              'Tahoma'))

        self.ir1Label = wx.StaticText(id=wxID_MAINFRAMEIR1LABEL, label='Left',
              name='ir1Label', parent=self.panel1, pos=wx.Point(16, 704),
              size=wx.Size(19, 13), style=0)

        self.ir1 = wx.StaticText(id=wxID_MAINFRAMEIR1, label='Off', name='ir1',
              parent=self.panel1, pos=wx.Point(72, 704), size=wx.Size(16, 13),
              style=0)
        self.ir1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.ir2Label = wx.StaticText(id=wxID_MAINFRAMEIR2LABEL, label='Right',
              name='ir2Label', parent=self.panel1, pos=wx.Point(16, 736),
              size=wx.Size(25, 13), style=0)

        self.ir2 = wx.StaticText(id=wxID_MAINFRAMEIR2, label='Off', name='ir2',
              parent=self.panel1, pos=wx.Point(72, 736), size=wx.Size(16, 13),
              style=0)
        self.ir2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.stallLabel = wx.StaticText(id=wxID_MAINFRAMESTALLLABEL,
              label='Stall', name='stallLabel', parent=self.panel1,
              pos=wx.Point(216, 560), size=wx.Size(22, 13), style=0)
        self.stallLabel.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.stall = wx.StaticText(id=wxID_MAINFRAMESTALL, label='Not Stalled',
              name='stall', parent=self.panel1, pos=wx.Point(200, 592),
              size=wx.Size(61, 13), style=0)
        self.stall.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.batteryLabel = wx.StaticText(id=wxID_MAINFRAMEBATTERYLABEL,
              label='Battery', name='batteryLabel', parent=self.panel1,
              pos=wx.Point(208, 640), size=wx.Size(37, 13), style=0)
        self.batteryLabel.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.battery = wx.Gauge(id=wxID_MAINFRAMEBATTERY, name='battery',
              parent=self.panel1, pos=wx.Point(176, 672), range=30,
              size=wx.Size(100, 28), style=wx.GA_HORIZONTAL)

        self.mazeLabel = wx.StaticText(id=wxID_MAINFRAMEMAZELABEL,
              label='Maze Environment', name='mazeLabel', parent=self.panel1,
              pos=wx.Point(304, 176), size=wx.Size(105, 13), style=0)
        self.mazeLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.mazegen = wx.Button(id=wxID_MAINFRAMEMAZEGEN, label='Generate',
              name='mazegen', parent=self.panel1, pos=wx.Point(320, 784),
              size=wx.Size(96, 40), style=0)
        self.mazegen.Bind(wx.EVT_LEFT_UP, self.OnMazegenLeftUp)

        self.mazegenLabel = wx.StaticText(id=wxID_MAINFRAMEMAZEGENLABEL,
              label='Maze Generation', name='mazegenLabel', parent=self.panel1,
              pos=wx.Point(304, 664), size=wx.Size(96, 13), style=0)
        self.mazegenLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.mazegenChoice = wx.Choice(choices=["RB", "Kruskal", "Prim",
              "Custom"], id=wxID_MAINFRAMEMAZEGENCHOICE, name='mazegenChoice',
              parent=self.panel1, pos=wx.Point(304, 688), size=wx.Size(136, 21),
              style=0)
        self.mazegenChoice.SetSelection(0)

        self.height = wx.Slider(id=wxID_MAINFRAMEHEIGHT, maxValue=11,
              minValue=3, name='height', parent=self.panel1, pos=wx.Point(352,
              720), size=wx.Size(100, 24), style=wx.SL_HORIZONTAL, value=10)
        self.height.SetLabel('')

        self.width = wx.Slider(id=wxID_MAINFRAMEWIDTH, maxValue=18, minValue=3,
              name='width', parent=self.panel1, pos=wx.Point(352, 752),
              size=wx.Size(100, 24), style=wx.SL_HORIZONTAL, value=10)
        self.width.SetLabel('')

        self.mazegenHeightLabel = wx.StaticText(id=wxID_MAINFRAMEMAZEGENHEIGHTLABEL,
              label='Height', name='mazegenHeightLabel', parent=self.panel1,
              pos=wx.Point(304, 720), size=wx.Size(32, 13), style=0)

        self.mazegenWidthLabel = wx.StaticText(id=wxID_MAINFRAMEMAZEGENWIDTHLABEL,
              label='Width', name='mazegenWidthLabel', parent=self.panel1,
              pos=wx.Point(304, 752), size=wx.Size(28, 13), style=0)

        self.maze = wx.lib.buttons.GenBitmapButton(bitmap=wx.Bitmap(u'C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG), id=wxID_MAINFRAMEMAZE, name='maze',
              parent=self.panel1, pos=wx.Point(304, 200), size=wx.Size(592,
              448), style=0)
        self.maze.SetBezelWidth(1)
        self.maze.Enable(False)
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
        self.maze.Bind(wx.EVT_BUTTON, self.OnMazeButton, id=wxID_MAINFRAMEMAZE)

        self.mazesolveLabel = wx.StaticText(id=wxID_MAINFRAMEMAZESOLVELABEL,
              label='Maze Solving', name='mazesolveLabel', parent=self.panel1,
              pos=wx.Point(472, 664), size=wx.Size(74, 13), style=0)
        self.mazesolveLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.solve = wx.Button(id=wxID_MAINFRAMESOLVE, label='Draw Solution',
              name='solve', parent=self.panel1, pos=wx.Point(472, 688),
              size=wx.Size(128, 40), style=0)
        self.solve.Bind(wx.EVT_LEFT_UP, self.OnSolveLeftUp)

        self.teachingLabel = wx.StaticText(id=wxID_MAINFRAMETEACHINGLABEL,
              label='Teaching', name='teachingLabel', parent=self.panel1,
              pos=wx.Point(616, 664), size=wx.Size(51, 13), style=0)
        self.teachingLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.teachingButton = wx.Button(id=wxID_MAINFRAMETEACHINGBUTTON,
              label='Start', name='teachingButton', parent=self.panel1,
              pos=wx.Point(616, 688), size=wx.Size(136, 40), style=0)
        self.teachingButton.Enable(False)
        self.teachingButton.Bind(wx.EVT_LEFT_UP, self.OnTeachingButtonLeftUp)

        self.teachingSource = wx.Button(id=wxID_MAINFRAMETEACHINGSOURCE,
              label='Edit Generated Source', name='teachingSource',
              parent=self.panel1, pos=wx.Point(616, 736), size=wx.Size(136, 48),
              style=0)

        self.autoLabel = wx.StaticText(id=wxID_MAINFRAMEAUTOLABEL,
              label='Autonomous Mode', name='autoLabel', parent=self.panel1,
              pos=wx.Point(760, 664), size=wx.Size(107, 13), style=0)
        self.autoLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.autoButton = wx.Button(id=wxID_MAINFRAMEAUTOBUTTON, label='Start',
              name='autoButton', parent=self.panel1, pos=wx.Point(760, 688),
              size=wx.Size(128, 40), style=0)
        self.autoButton.Enable(False)
        self.autoButton.Bind(wx.EVT_LEFT_UP, self.OnAutoButtonLeftUp)

        self.ms_up = wx.Button(id=wxID_MAINFRAMEMS_UP, label='p', name='ms_up',
              parent=self.panel1, pos=wx.Point(512, 736), size=wx.Size(40, 32),
              style=0)
        self.ms_up.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Wingdings 3'))
        self.ms_up.Bind(wx.EVT_LEFT_UP, self.OnMs_upLeftUp)

        self.ms_down = wx.Button(id=wxID_MAINFRAMEMS_DOWN, label='q',
              name='ms_down', parent=self.panel1, pos=wx.Point(512, 768),
              size=wx.Size(40, 32), style=0)
        self.ms_down.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Wingdings 3'))
        self.ms_down.Bind(wx.EVT_LEFT_UP, self.OnMs_downLeftUp)

        self.ms_left = wx.Button(id=wxID_MAINFRAMEMS_LEFT, label='t',
              name='ms_left', parent=self.panel1, pos=wx.Point(472, 752),
              size=wx.Size(40, 32), style=0)
        self.ms_left.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Wingdings 3'))
        self.ms_left.Bind(wx.EVT_LEFT_UP, self.OnMs_leftLeftUp)

        self.ms_right = wx.Button(id=wxID_MAINFRAMEMS_RIGHT, label='u',
              name='ms_right', parent=self.panel1, pos=wx.Point(552, 752),
              size=wx.Size(40, 32), style=0)
        self.ms_right.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Wingdings 3'))
        self.ms_right.Bind(wx.EVT_LEFT_UP, self.OnMs_rightLeftUp)

        self.results = wx.Button(id=wxID_MAINFRAMERESULTS, label='View Results',
              name='results', parent=self.panel1, pos=wx.Point(472, 808),
              size=wx.Size(120, 32), style=0)
        self.results.Bind(wx.EVT_LEFT_UP, self.OnResultsLeftUp)

        self.execute = wx.Button(id=wxID_MAINFRAMEEXECUTE,
              label='Execute Solution', name='execute', parent=self.panel1,
              pos=wx.Point(472, 848), size=wx.Size(120, 31), style=0)
        self.execute.Bind(wx.EVT_LEFT_UP, self.OnExecLeftUp)

        self.reallyMove = wx.CheckBox(id=wxID_MAINFRAMEREALLYMOVE,
              label='Actually Move', name='reallyMove', parent=self.panel1,
              pos=wx.Point(480, 888), size=wx.Size(112, 21), style=0)
        self.reallyMove.SetValue(False)

        self.getPen = wx.Button(id=wxID_MAINFRAMEGETPEN, label='Get Pen Data',
              name='getPen', parent=self.panel1, pos=wx.Point(96, 856),
              size=wx.Size(120, 40), style=0)
        self.getPen.Bind(wx.EVT_LEFT_UP, self.OnGetPenLeftUp)

        self.serverConnect = wx.Button(id=wxID_MAINFRAMESERVERCONNECT,
              label='Connect to Server', name='serverConnect',
              parent=self.panel1, pos=wx.Point(304, 120), size=wx.Size(128, 31),
              style=0)
        self.serverConnect.Bind(wx.EVT_LEFT_UP, self.OnServerConnectLeftUp)

        self.usePen = wx.CheckBox(id=wxID_MAINFRAMEUSEPEN, label='Use Pen',
              name='usePen', parent=self.panel1, pos=wx.Point(480, 912),
              size=wx.Size(88, 16), style=0)
        self.usePen.SetValue(False)

    def __init__(self, parent):
        self._init_ctrls(parent)
        # duplicates the mazegen button, should probably find a more elegant way to do this.
        global m # maze
        global pd # previous direction
        global dir # current direction
        global s # socket
        
        pd = 3
        h = self.height.GetValue()
        w = self.width.GetValue()
        if (self.mazegenChoice.GetCurrentSelection() == 0):
            m = mazegen_rb(h,w)
        elif (self.mazegenChoice.GetCurrentSelection() == 1):
            m = mazegen_kruskal(h,w)
        elif (self.mazegenChoice.GetCurrentSelection() == 2):
            m = mazegen_prim(h,w)
        elif (self.mazegenChoice.GetCurrentSelection() == 3):
            m = [[1,1,1,2,1,1,1,1,1],[1,0,0,0,1,0,0,0,1],[1,0,1,1,1,1,1,0,1],[1,0,0,0,0,0,1,0,1],[1,1,1,1,1,0,1,0,1],[1,0,0,0,1,0,0,0,1],[1,0,1,1,1,1,1,0,1],[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,3,1,1,1]];
            dir = 3
        global pos
        pos = en
        pos_x = pos[0]
        pos_y = pos[1]
        m[pos_x][pos_y] = -3
        drawmaze(m)
        
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
              
        global n
        n = 0
        
        global right
        right = 1
        
        global sln
        sln = [2,3,0,3,0,0,3,2]

    def OnExitLeftUp(self, event):
        event.Skip()

    def OnImgTakerLeftUp(self, event):
        mTakePicture(self)
        event.Skip()

    def OnInitLeftUp(self, event):
        init()
        self.imgTaker.Enable(True)
        self.motionJoystick.Enable(True)
        self.motionGamepad.Enable(True)
        self.motionUp.Enable(True)
        self.motionLeft.Enable(True)
        self.motionRight.Enable(True)
        self.motionDown.Enable(True)
        self.read.Enable(True)
        self.teachingButton.Enable(True)
        self.autoButton.Enable(True)
        event.Skip()

    def OnMotionJoystickLeftUp(self, event):
        joyStick()
        # event.Skip()

    def OnMotionGamepadLeftUp(self, event):
        gamepad()
        event.Skip()

    def OnMotionUpLeftUp(self, event):
        r_up(self)
        readSensors(self)
        mTakePicture(self)
        event.Skip()
        
    def OnMotionDownLeftUp(self, event):
        r_down(self)
        readSensors(self)
        mTakePicture(self)
        event.Skip()

    def OnMotionLeftLeftUp(self, event):
        r_left(self)
        readSensors(self)
        mTakePicture(self)
        event.Skip()

    def OnMotionRightLeftUp(self, event):
        r_right(self)
        readSensors(self)
        mTakePicture(self)
        event.Skip()

    def OnReadLeftUp(self, event):
        readSensors(self)
        readSensors(self)
        event.Skip()

    def OnMazegenLeftUp(self, event):
        print 'Maze generated.'
        global m
        global en
        global ex
        global dir
        global pd
        h = self.height.GetValue()
        w = self.width.GetValue()
        if (self.mazegenChoice.GetCurrentSelection() == 0):
            m = mazegen_rb(h,w)
        elif (self.mazegenChoice.GetCurrentSelection() == 1):
            m = mazegen_kruskal(h,w)
        elif (self.mazegenChoice.GetCurrentSelection() == 2):
            m = mazegen_prim(h,w)
        elif (self.mazegenChoice.GetCurrentSelection() == 3):
            m = [[1,1,1,2,1,1,1,1,1],[1,0,0,0,1,0,0,0,1],[1,0,1,1,1,1,1,0,1],[1,0,0,0,0,0,1,0,1],[1,1,1,1,1,0,1,0,1],[1,0,0,0,1,0,0,0,1],[1,0,1,1,1,1,1,0,1],[1,0,0,0,0,0,0,0,1],[1,1,1,1,1,3,1,1,1]];
            en = [7,5]
            ex = [1,3]
            dir = 3
        global pos
        pos = en
        pos_x = pos[0]
        pos_y = pos[1]
        print 'Current position is %d,%d' % (pos_x,pos_y)
        print 'The current direction is %d' % dir
        print 'The previous direction is %d' % pd
        m[pos_x][pos_y] = -3
        drawmaze(m)
        
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
              
        global n
        n = 0
        global right
        right = 1
        event.Skip()

    def OnSolveLeftUp(self, event):
        global s
        s = mazesolve_follow(m)
        drawmaze(s)
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
        event.Skip()

    def OnTeachingButtonLeftUp(self, event):
        if (self.teachingButton.GetValue == "Start"):
            self.teachingButton.SetValue("Stop")
        else:
            self.teachingButton.SetValue("Start")
        event.Skip()

    def OnAutoButtonLeftUp(self, event):
        if (self.autoButton.GetValue == "Start"):
            self.autoButton.SetValue("Stop")
        else:
            self.autoButton.SetValue("Start")

        event.Skip()

    def OnMazeButton(self, event):
        event.Skip()

    def OnMs_upLeftUp(self, event):
        global pd
        doit = m_up(self)
        if (self.reallyMove.GetValue() == True)&(doit == 1):
            r_up(self)
            readSensors(self)
            mTakePicture(self)
        pd = 0
        event.Skip()

    def OnMs_downLeftUp(self, event):
        global pd
        doit = m_down(self)
        if (self.reallyMove.GetValue() == True)&(doit == 1):
            r_down(self)
            readSensors(self)
            mTakePicture(self)
        pd = 2
        event.Skip()

    def OnMs_leftLeftUp(self, event):
        global pd
        doit = m_left(self)
        if (self.reallyMove.GetValue() == True)&(doit == 1):
            r_left(self)
            readSensors(self)
            mTakePicture(self)
        pd = 3
        event.Skip()

    def OnMs_rightLeftUp(self, event):
        global pd
        doit = m_right(self)
        if (self.reallyMove.GetValue() == True)&(doit == 1):
            r_right(self)
            readSensors(self)
            mTakePicture(self)
        pd = 1
        event.Skip()

    def OnResultsLeftUp(self, event):
        global right
        dlg = results.Results(self)
        dlg.resultsBox.ChangeValue(str(right))
        try:
            dlg.ShowModal()
        finally:
            dlg.Destroy()
        event.Skip()

    def OnExecLeftUp(self, event):
        global sln
        print 'Solution to be executed: %s' % sln
        sl = len(sln)
        for i in range(sl):
            print sln[i]
            if sln[i] == 0:
                doit = m_up(self)
                if (self.reallyMove.GetValue() == True)&(doit == 1):
                    r_up(self)
                    readSensors(self)
                    mTakePicture(self)
            elif sln[i] == 1:
                doit = m_right(self)
                if (self.reallyMove.GetValue() == True)&(doit == 1):
                    r_right(self)
                    readSensors(self)
                    mTakePicture(self)
            elif sln[i] == 2:
                doit = m_down(self)
                if (self.reallyMove.GetValue() == True)&(doit == 1):
                    r_down(self)
                    readSensors(self)
                    mTakePicture(self)
            elif sln[i] == 3:
                doit = m_left(self)
                if (self.reallyMove.GetValue() == True)&(doit == 1):
                    r_left(self)
                    readSensors(self)
                    mTakePicture(self)
        event.Skip()
        
# global stuff

    def OnGetPenLeftUp(self, event):
        global s
        
        x,y,page = getpendata(s)
        
        row = page/5
        col = page - (5*row)
        
        global m
        
        m[1+(2*(row-1))][1+(2*(col-1))] = -3
        
        drawmaze(m)
        
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
    
        event.Skip()

    def OnServerConnectLeftUp(self, event):
        global s
        print 'starting'
        host = '127.0.0.1'
        port = 8000
        size = 80
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60)
        try:
            s.connect((host,port))
        except:
            print 'error connect'
        event.Skip()

def m_left(self):
    global pos
    global prev
    global dir
    px = pos[0]
    py = pos[1]
    global m
    if (m[px-1][py] != 1):
        dir = 3
        px2 = px - 2
        m[px2][py] = -3
        m[px][py] = -4
        m[(px+px2)/2][py] = -4
        prev = pos
        pos = [px2,py]
        drawmaze(m)
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
        calculate(3)
        return(1)
    else:
        return(0)

def m_right(self):
    global pos
    global prev
    global dir
    px = pos[0]
    py = pos[1]
    global m
    if (m[px+1][py] != 1):
        dir = 1
        px2 = px + 2
        m[px2][py] = -3
        m[px][py] = -4
        m[(px+px2)/2][py] = -4
        prev = pos
        pos = [px2,py]
        drawmaze(m)
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
        calculate(1)
        return(1)
    else:
        return(0)
        
def m_down(self):
    global pos
    global prev
    global dir
    px = pos[0]
    py = pos[1]
    global m
    if (m[px][py+1] != 1):
        dir = 2
        py2 = py + 2
        m[px][py2] = -3
        m[px][py] = -4
        m[px][(py+py2)/2] = -4
        prev = pos
        pos = [px,py2]
        drawmaze(m)
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
        calculate(2)
        return(1)
    else:
        return(0)
    
def m_up(self):
    global pos
    global prev
    global dir
    px = pos[0]
    py = pos[1]
    global m
    if (m[px][py-1] != 1):
        dir = 0
        py2 = py - 2
        m[px][py2] = -3
        m[px][py] = -4
        m[px][(py+py2)/2] = -4
        prev = pos
        pos = [px,py2]
        drawmaze(m)
        self.Refresh()
        self.maze.SetBitmapDisabled(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/maze.png',
              wx.BITMAP_TYPE_PNG))
        calculate(0)
        return(1)
    else:
        return(0)

def r_up(self):
    global pd
    print 'For robot turning, previous direction was %d' % pd
    if (pd == 1):
        r_lturn()
    elif (pd == 2):
        r_uturn()
    elif (pd == 3):
        r_rturn()
    r_forward(self)

def r_down(self):
    global pd
    print 'For robot turning, previous direction was %d' % pd
    if (pd == 0):
        r_uturn()
    elif (pd == 1):
        r_rturn()
    elif (pd == 3):
        r_lturn()
    r_forward(self)

def r_left(self):
    global pd
    print 'For robot turning, previous direction was %d' % pd
    if (pd == 0):
        r_lturn()
    elif (pd == 2):
        r_rturn()
    elif (pd == 3):
        r_uturn()
    r_forward(self)
    
def r_right(self):
    global pd
    print 'For robot turning, previous direction was %d' % pd
    if (pd == 0):
        r_rturn()
    elif (pd == 1):
        r_uturn()
    elif (pd == 2):
        r_lturn()
    r_forward(self) 

def r_forward(self):
    global dir
    global s
    
    a = .5
    b = .5
    al = a
    bl = b
    
    #if (self.usePen.GetValue() == True):
    # turn right - increase a, turn left - decrease a
    x,y,page = getpendata(s)
    xi = x
    yi = y
    xl = xi
    yl = yi
    xg = xi
    yg = yi
    original = page
    t1l = 0.0
    t2l = 0.0

    pl = page
    
    if (dir==0):
        while ((page == original)|(y > 2200)):
            print 'Movin\' on up'
            x,y,page = getpendata(s)
            
            if (page == original):
                dy = y + 2200.0 #vertical distance from current point to target
            else:
                dy = y - 2200.0
            dx = x-2200.0 #horizontal distance from current point to target
            dmx = x-xl #horizontal change in last motion
            dmy = y-yl #vertical change in last motion
            if (dmx != 0):
                t1 = -(((math.pi)/2.0)-math.atan(dmy/dmx))
                t1l = t1
                xg = x
                yg = y
            else:
                t1 = t1l
                dmx = x-xg
                dmy = y-yg
            if (dx != 0):
                t2 = -(((math.pi)/2.0)-math.atan(dy/dx))
                t2l = t2
            else:
                t2 = t2l
            theta = (t1-t2)/18.0
            print 'dmx: %f' % dmx
            print 'dmy: %f' % dmy
            print 't1: %f' % t1
            print 't2: %f' % t2
            print 'theta: %f' % theta
            if (theta > 0):
                print 'turn right!'
            else:
                print 'turn left!'
            if ((abs(dmx)<600)&(abs(dmy)<600)&(page==pl)):
                motors(.3+theta,.3-theta)
                time.sleep(0.1)
                print 'actually do it!'
            xl = x
            yl = y
            pl = page
            motors(.3,.3)
            print (page == original)
            print (y > 2700)
        motors(0,0)

    elif (dir==1):
        while ((page == original)|(x < 2200)):
            print 'Movin\' on up'
            x,y,page = getpendata(s)
            if (page == original):
                dx = (5000-x) + 2200.0 #vertical distance from current point to target
            else:
                dx = 2200-x
            dy = y-2200.0 #horizontal distance from current point to target
            dmy = y-yl #horizontal change in last motion
            dmx = x-xl #vertical change in last motion
            if (dmy != 0):
                t1 = -(((math.pi)/2.0)-math.atan(dmx/dmy))
                t1l = t1
                xg = x
                yg = y
            else:
                t1 = t1l
                dmx = x-xg
                dmy = y-yg
            if (dx != 0):
                t2 = -(((math.pi)/2.0)-math.atan(dx/dy))
                t2l = t2
            else:
                t2 = t2l
            theta = (t1-t2)/18.0
            print 'dmx: %f' % dmx
            print 'dmy: %f' % dmy
            print 't1: %f' % t1
            print 't2: %f' % t2
            print 'theta: %f' % theta
            if (theta > 0):
                print 'turn right!'
            else:
                print 'turn left!'
            if ((abs(dmx)<600)&(abs(dmy)<600)&(page==pl)):
                motors(.3+theta,.3-theta)
                time.sleep(0.1)
                print 'actually do it!'
            xl = x
            yl = y
            pl = page
            motors(.3,.3)
            
        motors(0,0)
    elif (dir==2):
        while ((page == original)|(y < 2200)):
            print 'Movin\' on up'
            x,y,page = getpendata(s)
            if (page == original):
                dx = x + 2200.0 #vertical distance from current point to target
            else:
                dx = 2200-x
            dy = y-2200.0 #horizontal distance from current point to target
            dmy = y-yl #horizontal change in last motion
            dmx = x-xl #vertical change in last motion
            if (dmy != 0):
                t1 = -(((math.pi)/2.0)-math.atan(dmy/dmx))
                t1l = t1
                xg = x
                yg = y
            else:
                t1 = t1l
                dmx = x-xg
                dmy = y-yg
            if (dx != 0):
                t2 = -(((math.pi)/2.0)-math.atan(dy/dx))
                t2l = t2
            else:
                t2 = t2l
            theta = (t1-t2)/18.0
            print 'dmx: %f' % dmx
            print 'dmy: %f' % dmy
            print 't1: %f' % t1
            print 't2: %f' % t2
            print 'theta: %f' % theta
            if (theta > 0):
                print 'turn right!'
            else:
                print 'turn left!'
            if ((abs(dmx)<600)&(abs(dmy)<600)&(page==pl)):
                motors(.3+theta,.3-theta)
                time.sleep(0.1)
                print 'actually do it!'
            xl = x
            yl = y
            pl = page
            motors(.3,.3)
            
        motors(0,0)
    elif (dir==3):
        while ((page == original)|(x > 2200)):
            print 'Movin\' on up'
            x,y,page = getpendata(s)
            if (page == original):
                dx = x + 2200.0 #vertical distance from current point to target
            else:
                dx = x-2200
            dy = y-2200.0 #horizontal distance from current point to target
            dmy = y-yl #horizontal change in last motion
            dmx = x-xl #vertical change in last motion
            if (dmy != 0):
                t1 = -(((math.pi)/2.0)-math.atan(dmy/dmx))
                t1l = t1
                xg = x
                yg = y
            else:
                t1 = t1l
                dmx = x-xg
                dmy = y-yg
            if (dx != 0):
                t2 = -(((math.pi)/2.0)-math.atan(dy/dx))
                t2l = t2
            else:
                t2 = t2l
            theta = (t1-t2)/18.0
            print 'dmx: %f' % dmx
            print 'dmy: %f' % dmy
            print 't1: %f' % t1
            print 't2: %f' % t2
            print 'theta: %f' % theta
            if (theta > 0):
                print 'turn right!'
            else:
                print 'turn left!'
            if ((abs(dmx)<600)&(abs(dmy)<600)&(page==pl)):
                motors(.3+theta,.3-theta)
                time.sleep(0.1)
                print 'actually do it!'
            xl = x
            yl = y
            pl = page
            motors(.3,.3)
            
        motors(0,0)
    #else:
        #forward(.8,.8)
            
def getpendata(s):
    print 'Getting pen data'
    s.send(buffer('1'))
    data = s.recv(80)
     
    d = str(data)
    arr = d.split('(');
    arr2 = arr[1].split(',');
    x = int(arr2[0])
    y = int(arr2[1].split(')')[0])
    print 'Coordinates from pen: %d,%d' % (x,y)
    
    arr3 = d.split('.');
    last = arr3[3]
    arr4 = last.split('\t');
    page = int(arr4[0])
    print 'Page number from pen: %d' % page
    
    return x,y,page  
    
def r_lturn():
    turnLeft(.57,1)

def r_rturn():
    turnRight(.6,1)

def r_uturn():
    turnRight(.8,1)
    return
    
def readSensors(self):
    # Light sensors
    l1 = 30000-getLight(0)
    l2 = 30000-getLight(1)
    l3 = 30000-getLight(2)
    if ((l1 < 0) | (l1 == 30000)):
        l1 = 0
    if ((l2 < 0) | (l2 == 30000)):
        l2 = 0
    if ((l3 < 0) | (l3 == 30000)):
        l3 = 0
    self.light1.SetValue(l1)
    self.light2.SetValue(l2)
    self.light3.SetValue(l3)
    
    # IR sensors
    i1 = getIR(0)
    i2 = getIR(1)
    if (i1 == 0):
        it1 = "Off"
    else:
        it1 = "On"
    if (i2 == 0):
        it2 = "Off"
    else:
        it2 = "On"
    self.ir1.SetLabel(it1)
    self.ir2.SetLabel(it2)
    
    #Stall sensor
    s = getStall()
    if (s == 0):
        st = "Not Stalled"
    else:
        st = "Stalled"
    self.stall.SetLabel(st)
    
    # Battery
    b = getBattery()
    self.battery.SetValue(b)
    
def mTakePicture(self):
    c = self.imgChoice.GetCurrentSelection()
    if c == 0:
        p = takePicture("color")
    elif c == 1:
        p = takePicture("gray")
    elif c == 2:
        p = takePicture("blob")
    savePicture(p, 'C:/Documents and Settings/Jason/My Documents/Robotics/Maze/camera.jpg')
    self.img.SetBitmap(wx.Bitmap('C:/Documents and Settings/Jason/My Documents/Robotics/Maze/camera.jpg',
          wx.BITMAP_TYPE_JPEG))

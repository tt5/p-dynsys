import numpy as np
import math
import sys
import random
from matplotlib import pyplot as plt
import imageio

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)

writer = imageio.get_writer('new_video.mp4', fps=60)

def do_add( spile, tumbled ):
    """ Updates spile in place """
    spile[ :-1, :] += tumbled[ 1:, :] # Shift N and add                 
    spile[ 1:, :] += tumbled[ :-1, :] # Shift S   
    spile[ :, :-1] += tumbled[ :, 1:] # Shift W
    spile[ :, 1:] += tumbled[ :, :-1] # Shift E

def tumble( spile ):
    while ( spile > 3 ).any():
        tumbled, spile = np.divmod( spile, 4 )
        do_add( spile, tumbled )
        #spile = np.clip(spile, 0, 10)
        # print( spile, '\n' )  # Uncomment to print steps
    return spile

def tumbleR( spile ):
    while ( spile > 3 ).any():
        tumbled, spile = np.divmod( spile, 4 )
        do_add( spile, tumbled )
        spile = np.clip(spile, 0, 8)
        # print( spile, '\n' )  # Uncomment to print steps
    return spile

size = 144

T = np.zeros((size,size), dtype='int')
C = np.zeros((size,size), dtype='int')
ND = np.zeros((size,size), dtype='int')
AC = np.zeros((size,size), dtype='int')

# 1 queen
# 2 N
# 3 D
# 4 A
# 5 C


C[size//2,size//2] = 1

C[2*size//3,size//3] = 1
C[3*size//5,size//5] = 1
C[7*size//11,size//11] = 1
C[13*size//17,size//13] = 1
#C[19*size//23,size//19] = 1
#C[31*size//37,size//31] = 1

C[-size//2,size//2] = 1
C[-2*size//3,size//3] = 1
C[-7*size//11,size//11] = 1
#C[-13*size//17,size//13] = 1

C[size//2,-size//2] = 1
C[2*size//3,-size//3] = 1
C[7*size//11,-size//11] = 1
#C[13*size//17,-size//13] = 1

C[size//3,2*size//3] = 1
C[size//5,3*size//5] = 1
C[size//11,7*size//11] = 1
C[size//17,13*size//17] = 1
#C[size//23,19*size//23] = 1
#C[size//37,31*size//37] = 1

C[-size//3,2*size//3] = 1
C[-size//5,3*size//5] = 1
#C[-size//11,7*size//11] = 1

C[size//3,-2*size//3] = 1
C[size//5,-3*size//5] = 1
#C[size//11,-7*size//11] = 1

C[2*size//3,2*size//3] = 1
C[3*size//5,3*size//5] = 1
C[7*size//11,7*size//11] = 1
C[13*size//17,13*size//17] = 1
#C[19*size//23,19*size//23] = 1
#C[31*size//37,31*size//37] = 1

C[-2*size//3,2*size//3] = 1
C[-3*size//5,3*size//5] = 1
C[-7*size//11,7*size//11] = 1

C[2*size//3,-2*size//3] = 1
C[3*size//5,-3*size//5] = 1
C[7*size//11,-7*size//11] = 1

C[size//3,size//3] = 1
C[size//7,size//7] = 1
C[size//11,size//11] = 1
C[size//13,size//13] = 1
C[size//17,size//17] = 1
C[size//19,size//19] = 1
#C[size//23,size//23] = 1

C[-size//3,size//3] = 1
C[-size//7,size//7] = 1
C[-size//11,size//11] = 1

C[size//3,-size//3] = 1
C[size//7,-size//7] = 1
C[size//11,-size//11] = 1

C[-1,0] = 1
C[0,-1] = 1
C[0,0] = 4
C[-1,-1] = 5
ACs = np.where(C > 3)
for (y,x) in zip(ACs[0],ACs[1]):
    AC[y,x] = 256

AC = tumble(AC)


a0 = 0.1
alpha = 0.5 # help from defectors
gamma = 2 # cooperation for C

cAA = 1.5

cAC = 1.3
cCC = 0.1

for tick in range(4000):

    # eating
    As = np.where(C == 4)
    for (y,x) in zip(As[0],As[1]):
        north = south = east = west = northeast = northwest = southeast = southwest = 0
        if y>0:
            north = C[y-1,x]
        if y<size-1:
            south = C[y+1,x]
        if x<size-1:
            east = C[y,x+1]
        if x>0:
            west = C[y,x-1]
        if y>0 and x<size-1:
            northeast = C[y-1,x+1]
        if y>0 and x>0:
            northwest = C[y-1,x-1]
        if y<size-1 and x<size-1:
            southeast = C[y+1,x+1]
        if y<size-1 and x>0:
            southwest = C[y+1,x-1]
        neighbors = [north, south, east, west, northeast, northwest, southeast, southwest]
        nD = neighbors.count(3)
        nA = neighbors.count(4)
        nC = neighbors.count(5)
        # can eat N, D
        for i, j in enumerate(neighbors):
            if j == 2:
                # conditions
                pkill = max(0, min(a0+alpha*nD / 1 + cAA*nA + cAC*nC, 1))
                if pkill < 0.5:
                    break
                if i == 0:
                    # north
                    if(C[y-1,x]==1):
                        print("no")
                    C[y-1,x] = 0
                    ND[y-1,x] = 0
                elif i == 1:
                    # south
                    if C[y+1,x]==1:
                        print("no")
                    C[y+1,x] = 0
                    ND[y+1,x] = 0
                elif i == 2:
                    # east
                    if C[y,x+1]==1:
                        print("no")
                    C[y,x+1] = 0
                    ND[y,x+1] = 0
                elif i == 3:
                    # west
                    if C[y,x-1]==1:
                        print("no")
                    C[y,x-1] = 0
                    ND[y,x-1] = 0
                elif i == 4:
                    # northeast
                    if C[y-1,x+1]==1:
                        print("no")
                    C[y-1,x+1] = 0
                    ND[y-1,x+1] = 0
                elif i == 5:
                    # northwest
                    if C[y-1,x-1]==1:
                        print("no")
                    C[y-1,x-1] = 0
                    ND[y-1,x-1] = 0
                elif i == 6:
                    # southeast
                    if C[y+1,x+1]==1:
                        print("no")
                    C[y+1,x+1] = 0
                    ND[y+1,x+1] = 0
                elif i == 7:
                    # southwest
                    if C[y+1,x-1]==1:
                        print("no")
                    C[y+1,x-1] = 0
                    ND[y+1,x-1] = 0
            elif j == 3:
                if 2 not in neighbors:
                    if i == 0:
                        # north
                        C[y-1,x] = 0
                        ND[y-1,x] = 0
                    elif i == 1:
                        # south
                        C[y+1,x] = 0
                        ND[y+1,x] = 0
                    elif i == 2:
                        # east
                        C[y,x+1] = 0
                        ND[y,x+1] = 0
                    elif i == 3:
                        # west
                        C[y,x-1] = 0
                        ND[y,x-1] = 0
                    elif i == 4:
                        # northeast
                        C[y-1,x+1] = 0
                        ND[y-1,x+1] = 0
                    elif i == 5:
                        # northwest
                        C[y-1,x-1] = 0
                        ND[y-1,x-1] = 0
                    elif i == 6:
                        # southeast
                        C[y+1,x+1] = 0
                        ND[y+1,x+1] = 0
                    elif i == 7:
                        # southwest
                        C[y+1,x-1] = 0
                        ND[y+1,x-1] = 0


    Cs = np.where(C == 5)
    for (y,x) in zip(Cs[0],Cs[1]):
        north = south = east = west = northeast = northwest = southeast = southwest = 0

        if y>0:
            north = C[y-1,x]
        if y<size-1:
            south = C[y+1,x]
        if x<size-1:
            east = C[y,x+1]
        if x>0:
            west = C[y,x-1]
        if y>0 and x<size-1:
            northeast = C[y-1,x+1]
        if y>0 and x>0:
            northwest = C[y-1,x-1]
        if y<size-1 and x<size-1:
            southeast = C[y+1,x+1]
        if y<size-1 and x>0:
            southwest = C[y+1,x-1]
        neighbors = [north, south, east, west, northeast, northwest, southeast, southwest]
        nD = neighbors.count(3)
        nA = neighbors.count(4)
        nC = neighbors.count(5)
        # can eat N, D
        for i, j in enumerate(neighbors):
            if j == 2:
                pkill = max(0, min(a0+alpha*nD / 1 + cCC - gamma*nC + cAC*nA, 1))
                if pkill < 0.5:
                    break;
                if i == 0:
                    # north
                    C[y-1,x] = 0
                    ND[y-1,x] = 0
                elif i == 1:
                    # south
                    C[y+1,x] = 0
                    ND[y+1,x] = 0
                elif i == 2:
                    # east
                    C[y,x+1] = 0
                    ND[y,x+1] = 0
                elif i == 3:
                    # west
                    C[y,x-1] = 0
                    ND[y,x-1] = 0
                elif i == 4:
                    # northeast
                    C[y-1,x+1] = 0
                    ND[y-1,x+1] = 0
                elif i == 5:
                    # northwest
                    C[y-1,x-1] = 0
                    ND[y-1,x-1] = 0
                elif i == 6:
                    # southeast
                    C[y+1,x+1] = 0
                    ND[y+1,x+1] = 0
                elif i == 7:
                    # southwest
                    C[y+1,x-1] = 0
                    ND[y+1,x-1] = 0
            elif j == 3:
                if 2 not in neighbors:
                    if i == 0:
                        # north
                        C[y-1,x] = 0
                        ND[y-1,x] = 0
                    elif i == 1:
                        # south
                        C[y+1,x] = 0
                        ND[y+1,x] = 0
                    elif i == 2:
                        # east
                        C[y,x+1] = 0
                        ND[y,x+1] = 0
                    elif i == 3:
                        # west
                        C[y,x-1] = 0
                        ND[y,x-1] = 0
                    elif i == 4:
                        # northeast
                        C[y-1,x+1] = 0
                        ND[y-1,x+1] = 0
                    elif i == 5:
                        # northwest
                        C[y-1,x-1] = 0
                        ND[y-1,x-1] = 0
                    elif i == 6:
                        # southeast
                        C[y+1,x+1] = 0
                        ND[y+1,x+1] = 0
                    elif i == 7:
                        # southwest
                        C[y+1,x-1] = 0
                        ND[y+1,x-1] = 0

    # add new ND to C
    NDs = np.where(ND > 0)
    for (y,x) in zip(NDs[0],NDs[1]):
        north = south = east = west = 0
        if y>0:
            north = C[y-1,x]
        if y<size-1:
            south = C[y+1,x]
        if x<size-1:
            east = C[y,x+1]
        if x>0:
            west = C[y,x-1]
        neighbors = [north, south, east, west]
        nN = neighbors.count(2)
        nD = neighbors.count(3)
        nA = neighbors.count(4)
        if nA>0 and nN>0:
            if C[y,x] != 1:
                C[y,x] = 3
        else:
            if C[y,x] != 1:
                C[y,x] = 2

    # add new AC to C, don't occupy ND
    ACs = np.where(AC > 0)
    for (y,x) in zip(ACs[0],ACs[1]):
        if C[y,x]==2 or C[y,x]==3 or C[y,x]==1:
            continue
        #TAC[y,x] = 1
        north = south = east = west = 0
        if y>0:
            north = C[y-1,x]
        if y<size-1:
            south = C[y+1,x]
        if x<size-1:
            east = C[y,x+1]
        if x>0:
            west = C[y,x-1]
        neighbors = [north, south, east, west]
        nA = neighbors.count(4)
        nC = neighbors.count(5)
        if nA>nC:
            C[y,x] = 4
        elif nA<nC:
            C[y,x] = 5
        else:
            #C[y,x] = 4
            if random.randint(0,2)<2:
                C[y,x] = 5
            else:
                C[y,x] = 4

            #C[y,x] = 5-random.randint(0,1)

    # new ND
    Qs = np.where(C == 1)
    for (y,x) in zip(Qs[0],Qs[1]):
        ND[y,x] = ND[y,x]+512
        T[y,x] = (T[y,x] + 1)
        north = south = east = west = 1024
        if y>0:
            north = T[y-1,x]
        if y<size-1:
            south = T[y+1,x]
        if x<size-1:
            east = T[y,x+1]
        if x>0:
            west = T[y,x-1]
        neighbors = [north, south, east, west]
        if north < min(south, east, west):
            direction = 1
        elif south < min(north, east, west):
            direction = 2
        elif east < min(north, south, west):
            direction = 3
        elif west < min(north, south, east):
            direction = 4
        else:
            direction = random.randint(1,4)

        stepsize = 2
        if 1<x<size-2 and 1<y<size-2:
            if direction==1:
                if C[y-stepsize,x]!=1:
                    C[y,x] = 0
                    C[y-stepsize,x]=1
            elif direction == 2:
                if C[y+stepsize,x]!=1:
                    C[y,x] = 0
                    C[y+stepsize,x]=1
            elif direction == 3:
                if C[y,x+stepsize]!=1:
                    C[y,x] = 0
                    C[y,x+stepsize]=1
            else:
                if C[y,x-stepsize]!=1:
                    C[y,x] = 0
                    C[y,x-stepsize]=1

        else:
            if x < 2:
                if C[y,x+6]!=1:
                    C[y,x] = 0
                    C[y, x+6]=1
            elif x >= size-2:
                if C[y,x-6]!=1:
                    C[y,x] = 0
                    C[y, x-6]=1
            elif y < 2:
                if C[y+6,x]!=1:
                    C[y,x] = 0
                    C[y+6, x]=1
            else:
                if C[y-6,x]!=1:
                    C[y,x] = 0
                    C[y-6, x]=1



    # AC increment age
    if tick%17==0:
        ACs = np.where(AC > 0)
        for (y,x) in zip(ACs[0],ACs[1]):
            AC[y,x] = AC[y,x]+random.randint(0,3)


    ND = np.clip(ND,0,1024)
    AC = np.clip(AC,0,255)
    AC = np.clip(AC-(ND//3),0,8)
    ND = tumbleR(ND)
    AC = tumble(AC)

    frame = np.zeros((size,size,3), dtype='int')
    #frame[:,:,1] = (TAC)
    #frame[:,:,2] = (AC)
    frame[:,:,0] = (C==2)*128+(C==3)*128
    frame[:,:,1] = (C==4)*255
    frame[:,:,2] = (C==5)*255
    #frame[:,:,2] = (frame[:,:,2] == 2)*85
    writer.append_data(np.array(frame, dtype=np.uint8))
    #print(C)
    if tick%10==0:
        print(tick)


writer.close()

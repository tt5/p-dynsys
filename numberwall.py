
import numpy as np
from PIL import Image, ImageColor

def modm(n,m): #Reduces an integer modulo n modulo m.
    return n-m*(n//m)

def modminv(n,m): #Finds the inverse of a number n modulo m.
    if n==0:
        return 0
    for i in range(m):
        if modm(i*n,m)==1:
            return i

def numbwall(seq,m): #Input sequence and base, outputs portion of numberwall
    #print('seq=',seq)
    L=len(seq) #L is the length of the sequence inputted.
    for i in range(L):
        seq[i]=modm(seq[i],m)#Sequence taken mod m.
    ans=[] #This set will be the number wall.
    rowm1=[]
    row0=[]
    for i in range(L): #Creates row -1 and row 0 of the number wall.
        row0.append(1)
        rowm1.append(0)
    ans.append(rowm1)#Adds row -1 into the numberwall.
    ans.append(row0) #Adds row 0 into the numberwall.
    ans[0].insert(0,' ')
    ans[1].insert(0,' ') #Adds * to the left side of first two rows
    for c in range(0,int(np.ceil(L/2))): #Makes shape of number wall, fills with 1
        row=[' '] #Adds an astrix to the start of every row. This is so the
        #innerframe function does not overrun into the right hand side portion
        #of the number wall.
        for i in range(c):
            row.append(' ')#A finite sequence generates a trapesium shaped 
            #portion of the numberwall. This puts astrix's in the gaps to fill 
            #it into a rectangle, which is useful for display reasons.
        for i in range(L-2*c):
            row.append(-1) #This puts the number -1 in everywhere in the number wall 
            #one would expect there to be a number. -1 is chosen as it never naturally 
            #appears in the number wall, so mistakes are easy to spot.
        for i in range(c):
            row.append(' ')#Fills out the right side of the trapesium to complete
            #the rectangle.
        ans.append(row)
    for i in range(len(ans)):
        ans[i].append(' ')
    #print('before first row',ans)
    for i in range(1,L+1): #Fills in row 1 with the sequence.
        ans[2][i]=seq[i-1]
    #print(ans)
    for c in range(3,2+int(np.ceil(L/2))): #Fills in the remaining rows.
        if c==3: #Row 2 is filled seperately, since it never has a zero two rows 
        #above. This might be unnecessary, but don't fix what isn't broken.
            for j in range(c-1,L-c+3):
                ans[c][j]=modm(ans[c-1][j]**2-ans[c-1][j-1]*ans[c-1][j+1],m)
                #Uses the first frame constraint formula knowing that two rows above is entirely 1.
        if c!=3: #For the remaining rows, use frame constraints.
            for j in range(c-1,L-c+3):
                if ans[c-2][j]!=0: #If entry two above isn't zero.
                    ans[c][j]=modm(modminv(ans[c-2][j],m)*(ans[c-1][j]**2-ans[c-1][j-1]*ans[c-1][j+1]),m)
                    #First frame constraint formula
                if ans[c-2][j]==0 and ans[c-1][j]==0: #If both the two entries above are zero
                    A,B,C,D=innerframe(ans,c-2,j)#Find inner frame
                    li,lj, ui, uj = windowfind(ans,c-2,j)#Find corners of window
                    deltam1=len(A)-2#find length of window
                    k=deltam1-j+lj#Find value for k
                    if ui-li!=uj-lj:#If window not square
                        ans[c][j]=0#Make it so
                    else:
                        #Use frame constraints
                        ans[c][j]=modm((-1)**(deltam1*k)*B[k]*C[k]*modminv(A[k],m),m)
                if (ans[c-2][j]==0) and (ans[c-1][j]!=0): #If the entry two above isn't zero 
                #but the entry one above is.
                    A,B,C,D=innerframe(ans,c-2,j)#Inner frame
                    E,F,G,H = outerframe(ans,c-2,j)#Outer frame
                    P,Q,R,S = ratiofinder(ans,c-2,j,m)#Ratios of inner frame
                    li,lj, ui, uj = windowfind(ans,c-2,j)#Window corners
                    deltam1=len(A)-2#length of window
                    k=deltam1-j+lj#Value for k
                    if ui-li!=uj-lj:#If window not square 
                        ans[c][j]=0#Make it so
                    else:#Use finall frame constraint.
                        ans[c][j]=modm((Q*E[k]*modminv(A[k],m)+(-1)**(k)*P*F[k]*modminv(B[k],m)-(-1)\
                                        **(k)*S*G[k]*modminv(C[k],m))*modminv(R*modminv(D[k],m),m),m)
    return ans #return number wall


def windowfind(set,i,j):#Finds the upper left and lower right corners of a window
    if set[i][j]!=0: #If a window is not inputted
        return('Window not found') 
    #These values will be pushed out to find the corners of the window
    lj=j
    li=i
    uj=j
    ui=i
    while set[li][j]==0 and li>=0:
        li-=1#Find left side of window
    while set[li+1][lj]==0 and lj >=0:
        lj-=1#Find right side of window
    while ui<=len(set)-1 and set[ui][j]==0:
        ui+=1#Find top row of window
    while uj <= len(set[i])-1 and set[li+1][uj]==0:
        uj+=1#Find bottom of window
    if li==-1: #Deals with issue caused by zeros in the input sequence,
    #where the value of li would go into row -1
        li+=1
    return li+1,lj+1,ui-1,uj-1 #Return corners of window

def innerframe(set, i, j): #Finds inner frame
    li,lj, ui, uj = windowfind(set,i,j) #Corners of window
    A = []
    na = lj-1#Starting at the topleft wall of the window
    while na<=uj+1 and na<=len(set[li-1])-1: #Go along the top row of window
    #and only stop adding the entries to A when the window closes or the number
    #wall ends
        A.append(set[li-1][na])
        na+=1
    nb = li-1 #Same idea as A
    B=[]
    while nb<=ui+1 and nb<=len(set)-1:
        B.append(set[nb][lj-1])
        nb+=1
    nc = lj-1#Same idea as A
    C=[]
    while nc<=uj+1 and nc<=len(set[ui+1])-1:
        #print(nc)
        C.insert(0,set[ui+1][nc])
        nc+=1
    nd = li-1#Same idea as A
    D=[]
    while nd<=ui+1 and nd<=len(set)-1:
        D.insert(0,set[nd][uj+1])
        nd+=1
    return A,B,D,C
    
def outerframe(set, i, j): #Finds outer frame
    li,lj, ui, uj = windowfind(set,i,j) #Finds window corners
    E = [] #As in A, finds the start of the outer frame and then adds it to a 
    #list until it the window closes ot the number wall stops
    na = lj-1
    while na<=uj+1 and na<=len(set[li-1])-1:
        E.append(set[li-2][na])
        #print(na)
        na+=1
    nb = li-1
    F=[]
    while nb<=ui+1 and nb<=len(set)-1:
        F.append(set[nb][lj-2])
        nb+=1
    nc = lj-1
    G=[]
    while nc<=uj+1 and nc<=len(set[ui+1])-1:
        #print(nc)
        G.insert(0,set[ui+2][nc])
        nc+=1
    nd = li-1
    H=[]
    while nd<=ui+1 and nd<=len(set)-1:
        H.insert(0,set[nd][uj+2])
        nd+=1
    return E,F,H,G

def ratiofinder(set,i,j,m): #Finds ratios of the geometric series comprising the 
#inner frame
    A,B,C,D=innerframe(set,i,j) #Finds inner frame
    P=modm(A[1]*modminv(A[0],m),m) #Multiplies the second term by the inverse of
    #the first to find ratio.
    Q=modm(B[1]*modminv(B[0],m),m)
    for i in range(len(C)-1): #Scans the C row and if two consecutive entries are
    #integers, finds the ratio between them. Necessary because it would 
    #sometimes try and multiply by an astrix
        if type(C[i])==int and type(C[i+1])==int:
            R=modm(C[i+1]*modminv(C[i],m),m)
            pass
    #R=modm(C[-1]*modminv(C[-2]))
    for i in range(len(D)-1): #Same as R
        if type(D[i])==int and type(D[i+1])==int:
            S=modm(D[i+1]*modminv(D[i],m),m)
            pass
    return P,Q,R,S

def PrintNW(seq,m):#Creates an image of the number wall generated by a given sequence modulo m.
    data=numbwall(seq,m)
    #print(data)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j]==' ':
                data[i][j]=-1
    im = Image.new('RGBA', (len(data[0]),len(data))) # create the Image of size 1 pixel 
    #print(data)
    for i in range(len(data)):
        for j in range(len(data[i])): #Change Colours below   
            #print(i,j)
            if data[i][j]==-1:
                im.putpixel((j,i), ImageColor.getcolor('white', 'RGBA'))
            elif data[i][j]==0:
                im.putpixel((j,i), ImageColor.getcolor('red', 'RGBA'))
            elif data[i][j]==1:
                im.putpixel((j,i), ImageColor.getcolor('#222021', 'RGBA'))
            elif data[i][j]==2:
                im.putpixel((j,i), ImageColor.getcolor('#363636', 'RGBA'))
            elif data[i][j]==3:
                im.putpixel((j,i), ImageColor.getcolor('#544C4A', 'RGBA'))
            elif data[i][j]==4:
                im.putpixel((j,i), ImageColor.getcolor('#787276', 'RGBA'))
            elif data[i][j]==5:
                im.putpixel((j,i), ImageColor.getcolor('#787276', 'RGBA'))
            else:
                im.putpixel((j,i), ImageColor.getcolor('#787276', 'RGBA'))
                    
    #im.show()
    x='numberwallout'
    im.save(x+'.png',interlace=False) # or any image format
    return im
    

def PrintSpacedNW(seq,m):#Creates image of number wall with spaces between entries
    data=numbwall(seq,m)
    #print(data)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j]==' ':
                data[i][j]=-1
    im = Image.new('RGBA', (10*len(data[0]),10*len(data))) # create the Image of size 1 pixel 
    #print(data)
    for i in range(len(data)):
        for j in range(len(data[i])):    
            #print(i,j)
            if data[i][j]==-1:
                for k in range(10):
                    for l in range(10):
                        im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('white', 'RGBA'))
            if data[i][j]==0:
                for k in range(10):
                    for l in range(10):
                        if k==0 or l==0:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('white', 'RGBA'))
                        else:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('red', 'RGBA'))
                        
            if data[i][j]==1:
                for k in range(10):
                    for l in range(10):
                        if k==0 or l==0:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('white', 'RGBA'))
                        else:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('#222021', 'RGBA'))
            if data[i][j]==2:
                for k in range(10):
                    for l in range(10):
                        if k==0 or l==0:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('white', 'RGBA'))
                        else:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('#363636', 'RGBA'))
            if data[i][j]==3:
                for k in range(10):
                    for l in range(10):
                        if k==0 or l==0:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('white', 'RGBA'))
                        else:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('#544C4A', 'RGBA'))
            if data[i][j]==4:
                for k in range(10):
                    for l in range(10):
                        if k==0 or l==0:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('white', 'RGBA'))
                        else:
                            im.putpixel((10*j+k,10*i+l), ImageColor.getcolor('#787276', 'RGBA'))
    im.show()
    x='Thue Morse'
    im.save(x+'.png',interlace=False) # or any image format
    return im

def deftwoIterate(start,size,m): #finds all possible sequences of length L,
# and counts how many have a window of size exactly L with top left corner ulpos
    #produces every possible sequence of length
    #L made of digits 0,1,2. Must be changed manually to work over F_5 or F_7.
    #Would need new code for F_p p double digit prime.
    ans=0
    ans3=[]
    c=0
    L=len(start[0])+2
    for i in start:
        C=0
        for p in range(m):
            #print(i,p)
            c+=1
            if c%1000000==0:
                print(100*(c/(len(start)*m)),'%')
            ans2=[]
            for q in i:
                ans2.append(q)
            ans2.append(p)
            d=0
            nw = numbwall(ans2,m)
            for j in range(2,1+int(np.ceil(L/2))):
                e=0
                for k in range(size+1):
                    #print(nw[2],nw[j][L-j+1-k])
                    if nw[j][L-j+1-k]==0:
                        e+=1
                    if e==size+1:
                        d+=1
                        break
            if d==0:
                C+=1
                ans3.append(ans2)
                ans+=1
    print('L=',L-1,'number of sequences=', m**L,'number of squences of deficiency',ans)
    #print(ans3)
    return(ans3)

def defn(size,m):#Count how many sequences modulo m have windows of size 'size'
    start=[[]]
    while len(start)>0:
        start=deftwoIterate(start,size,m)

def calculate_nth(n):
  return bin(n).count("1") % 2

seq = [calculate_nth(x) for x in range(0,300)]
#print(seq)


#out = numbwall([1,2,3,4,5],2)
#print(out)
#seq = [1,2,3,4,5]
m = 2
PrintNW(seq,m)


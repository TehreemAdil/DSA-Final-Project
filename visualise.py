import matplotlib.animation as animation
from mapgen import *
from AstarAlgo import *

w, h = 200,200
mapimage = mapgenerate(w,h)

#using a helper function to find a random 0 so we dont start or end in a wall
def getfloor(grid):
    floors = np.argwhere(grid==0)
    if len(floors) == 0:
        return None
    return tuple(random.choice(floors))

#find a valid path(loops until it find two points that are connected)
path = None
while path is None:
    startnode = getfloor(mapimage)
    endnode = getfloor(mapimage)
    if startnode and endnode and startnode != endnode:
        path = astar(mapimage, startnode, endnode)


#visualisation code

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(mapimage, cmap="gray_r")
ax.axis('off')

# initialize plot elements
pathline, = ax.plot([], [], color='red', linewidth=2)
visitedscatter = ax.scatter([], [], color='yellow', s=5, alpha=0.5, label='Visited')
frontierscatter = ax.scatter([], [], color='blue', s=3, alpha=0.5, label='Frontier')
ax.scatter(startnode[1], startnode[0], color='lime', s=100, label='Start')
ax.scatter(endnode[1], endnode[0], color='cyan', s=100, label='Goal')
ax.legend()

#creating the path generation initially
pathgenerate = astar(mapimage, startnode, endnode)

def update(data):
    try:
        closeset, openheap, path, isdone = data

        #update the visited nodes
        if closeset:
            vy, vx = zip(*closeset)
            visitedscatter.set_offsets(np.c_[vx,vy])
        #update the nodes in the priotity queue
        if openheap:
            fx = [item[1][1] for item in openheap]
            fy = [item[1][0] for item in openheap]
            frontierscatter.set_offsets(np.c_[fx,fy])
        #if path is found, draw it, else clear the blue frontier dots if the heap is empty
        else:
            frontierscatter.set_offsets(np.empty((0,2)))

        if isdone:
            if path:
                py,px = zip(*path)
                pathline.set_data(px,py)
                print("Path rendered, check it.")
            else:
                print("Path not found.")
    except StopIteration:
            pass
    return visitedscatter, frontierscatter,pathline

ani = animation.FuncAnimation(fig, update, frames=pathgenerate, interval=1, blit=True, repeat=False)
plt.show() 
#frames is the number of frames the animation will run, set it to a definite value or
#the variable whoich has the path stored in it can be passed to frames until the algorithm is complete
#invterval in line 62 is the delay in miliseconds between frames
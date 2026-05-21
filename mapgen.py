import numpy as np
import matplotlib.pyplot as plt
import random

def mapgenerate(width, height, fillprob=0.48, iteration=5): #fillprob is the density of filling on the map
    #initialize
    grid = np.random.choice([1,0], size=(height,width), p=[fillprob,1-fillprob])

    #forcing border walls so the path doesnt shoot off the map
    grid[0, :] = 1
    grid[-1, :] = 1
    grid[:, 0] = 1
    grid[:, -1] = 1

    for i in range(iteration):
        newgrid = grid.copy()

        #stay 1 pixel away from the edge to keep our border intact
        for y in range(1,height-1):
            for x in range(1, width -1):

                #counting neighbours in a 3x3 area
                neighborhood = grid[y-1:y+2, x-1:x+2]
                wallcount = np.sum(neighborhood) - grid[y,x]

                #rule: 4-5 rule
                # if a pixel is surrounded by more than 4 walls, then it becomes a wall as well (to prevent small caves from forming)
                # if a pixel has less than 4 walls, delete it to prevent small unnecesary dots on the map

                if wallcount > 4:
                    newgrid[y,x] = 1
                elif wallcount < 4:
                    newgrid[y,x] = 0
        
        #re-enforce border after each pass to pass to prevent "erosion"
        newgrid[0, :] = 1
        newgrid[-1, :] = 1
        newgrid[:, 0] = 1 
        newgrid[:, -1] = 1
        grid = newgrid







        
    return grid

#declaration of the function above and how to run it

mapimage = mapgenerate(200,200)

# These are used to see if the map is generating fine

# plt.figure(figsize=(3,3))
# plt.imshow(mapimage, cmap='gray_r') 
# plt.axis('off')
# plt.show()


            


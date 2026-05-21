import numpy as np
import matplotlib.pyplot as plt
import heapq
from mapgen import *
import math


def heuristic(a,b):
    #coordinate geometry distance formula
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def astar(grid,start,goal):
    #possible neighbors to scan, in all 8 directions allowing for diagonal movement
    neighbors = [
        (0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1),     
        (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)  #1.414 = root 2
    ]

    closeset = set() #the nodes that are already visited
    comingfrom = {} #dictionary to track the path (parent of each node)
    gscore = {start:0} #g score is the cost from the start to current node
    fscore = {start:heuristic(start,goal)} #f score is the total estimated cost from start to goal node passing through a node n (g+h)
    openheap = [] #priority queue that allows us to pick the lowest Fscore

    heapq.heappush(openheap, (fscore[start], start))
    #heapq in python is a priority queue where the smallest value is always at the top
    #parameters of heappush(the heaplist itself, item that you will push in)
    #by pushing a tuple in "(fscore[start], start)", the philosophy goes like: python compares the first element of the tuple so our list is sorted by the fscore

    while openheap:
        current = heapq.heappop(openheap)[1] #getting the node with the lowest fscore

        if current == goal: #if we reached the goal
            path = []
            temp = current
            while temp in comingfrom: #backtrack from goal to start
                path.append(temp)
                temp = comingfrom[temp]
            yield closeset, openheap, path[::-1], True #yielding the final and a "finished flag"
            return
        
        closeset.add(current)
        
        for i,j, cost in neighbors:
            neighbor = (current[0] + i , current[1] + j)

            #boundary and wall check
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
                if grid[neighbor[0]][neighbor[1]] == 1: #if its a wall just skip it
                    continue
            else:
                continue
            
            #calculating cost to reach this neighbor
            temporaryGscore = gscore[current] + cost

            #if we find a better more efficent path update it
            if neighbor in closeset and temporaryGscore >= gscore.get(neighbor,0):
                continue
            
            if temporaryGscore < gscore.get(neighbor, float("inf")):
                comingfrom[neighbor] = current
                gscore[neighbor] = temporaryGscore
                fscore[neighbor] = gscore[neighbor] + heuristic(neighbor,goal)
                heapq.heappush(openheap, (fscore[neighbor], neighbor))

                #NOW YIELD THE CURRENT STATE TO THE ANIMATOR --> (visited nodes, frontier nods, currentpath, isdone)
        yield closeset, openheap, [], False 
    yield closeset, openheap, None, True #no path found

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

#from graphviz import Digraph
#dot = Digraph(comment='the round table')
from utils import heuristics
import queue as Q
from heappriority import PriorityQueue # for A* search
import time
import sys

def in_range(n):
    if 0 <= n <= 3  :
        return True
    else : 
        return False

def goalPrint(state,expanded):
    search_depth = 0
    goal_states = []
    
    cost = state.cost
    
    while state.parent != None:
        search_depth += 1
        goal_states.append(state)
        state = state.parent
    goal_states.reverse()
    print('path_to_goal: ',[g.config for g in goal_states])
    print("cost_of_path: ", cost)
    print('nodes_expanded: ', expanded)
    print('search_depth: ', search_depth)
## The Class that Represents the Puzzle
    
class PuzzleState(object):
    
    """docstring for PuzzleState"""
    def __init__(self, config, parent=None, action="Initial", cost=0,other = None):
        self.riverside = config[2]
        self.cost = cost
        self.heuristic_cost = 0
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []
        self.other = other
        
    def add_cost(self,cost):
        self.heuristic_cost = self.cost + cost
        return self.heuristic_cost
    # prints literally the table of the current configuration
    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)
            
    def miss_miss(self):
#        print('running miss_miss')
        if self.riverside:    
            m,c = self.config[0] - 2,self.config[1]
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0) or ( c>m and m>0 ) :  
                    return None
        else :
            m,c =  self.config[0] + 2,  self.config[1]
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ):  
                    return None
#            other_m, other_c = 3 - m , 3 - c
#            if other_c > other_m and other_m >0 :
#                return None
        riverside = not self.riverside
        return PuzzleState((m,c,riverside),parent = self,action = 'miss and miss {}'.format(riverside),cost= self.cost + 1)       
            
    def can_can(self):
#        print('running cann_vann')
        if self.riverside:    
            m,c = self.config[0],self.config[1] - 2
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ) :  
                    return None           
        else :
            m,c =  self.config[0] ,  self.config[1] + 2
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ):  
                    return None
            
            
        riverside = not self.riverside
        return PuzzleState((m,c,riverside),parent = self,action = 'can and can {}'.format(riverside),cost= self.cost + 1)
        
    
    def miss_can(self):
#        print('running miss_cann')
        if self.riverside:    
            m,c = self.config[0] - 1,self.config[1] - 1
            if c != m:
                if ( not in_range(c) or not in_range(m) )  :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ) :  
                    return None
        else :
            m,c =  self.config[0] + 1, self.config[1] + 1
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ):  
                    return None
        riverside = not self.riverside
        return PuzzleState((m,c,riverside),parent = self,action = 'miss and cann {}'.format(riverside),cost= self.cost + 1)
    
    def move_miss(self):
#        print('running miss_only')
        if self.riverside:    
            m,c = self.config[0] - 1,self.config[1]
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ):  
                    return None
                
        else :
            m,c =  self.config[0] + 1, self.config[1]
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ):  
                    return None
        riverside = not self.riverside
        return PuzzleState((m,c,riverside),parent = self,action = 'miss only {}'.format(riverside),cost= self.cost + 1)
        
    def move_can(self):
#        print('running cann_only')
        if self.riverside:    
            m,c = self.config[0] ,self.config[1] - 1
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ):  
                    return None
        else :
            m,c = self.config[0] , self.config[1] + 1
            if c != m:
                if ( not in_range(c) or not in_range(m) ) :
                    return None
                if ((3-c)>(3-m)  and (3-m) > 0)  or ( c>m and m>0 ):  
                    return None
        riverside = not self.riverside
        return PuzzleState((m,c,riverside),parent = self,action = 'cann only {}'.format(riverside),cost= self.cost + 1)
        

    def expand(self):
        """expand the node"""
        # add child nodes in order of UDLR
        if len(self.children) == 0:
            move1 = self.move_miss()
            if move1 is not None:
                self.children.append(move1)
            move2 = self.move_can()
            if move2 is not None:
                self.children.append(move2)
            move3 = self.miss_miss()
            if move3 is not None:
                self.children.append(move3)
            move4 = self.can_can()
            if move4 is not None:
                self.children.append(move4)
            move5 = self.miss_can()
            if move5 is not None:
                self.children.append(move5)
            
        return self.children
    

def bfs_search(initial_state,goal_state = (0,0,False)):
    """BFS search"""
    print('*** Running BFS ***')
    time1 = time.process_time()
    max_search_depth = 0
    expanded = -1
    counter = 1
    frontier = Q.Queue()
    frontierDict = {}
    frontier.put(initial_state)
    while not frontier.empty() :
        #REMOVE
        state = frontier.get()
        frontierDict[state.config] = state
        
        expanded += 1
#        if expanded == 0: 
#            dot.node(str(expanded),str(state.config) +' ' + str(expanded))
        #GOAL CHECK
        if state.config == goal_state:
            goalPrint(state,expanded)
            print('final state ', state.config)
            print('max_search_depth: ',max_search_depth)
            print('running_time: ', time.process_time()-time1)
            return state
          
        next_states = state.expand()
#        state_neighbours.reverse()
        #EXPAND
        for i in next_states:
            
#            dot.node(str(counter),str(i.config) + ' ' + str(counter))
#            dot.edge(str(expanded),str(counter))
            
            counter += 1
            if i.config not in frontierDict:             
                # these are the node in the queue, not the expanded nodes sucker
                frontier.put(i)
                frontierDict[i.config] = i

            if i.cost >= max_search_depth :
                    max_search_depth = i.cost
        
def dfs_search(initial_state,goal_state = (0,0,False)):

    """DFS search"""
    print('*** Running DFS ***')
    time1 = time.time()
    max_search_depth = 0
    expanded = -1
    frontier = []
    frontierDict = {}
    
    frontier.append(initial_state)
    explored = set()
    while len(frontier) != 0 :
        #REMOVE
        state = frontier.pop()
        explored.add(state)
        frontierDict[state.config] = state
        next_states = state.expand()
        next_states.reverse()
        expanded += 1
        #GOAL CHECK
        
        if state.config == goal_state:
            
            goalPrint(state,expanded)
            print('max_search_depth: ',max_search_depth)
            print('running_time: ', time.time()-time1)
            return state
          
        #EXPAND
        for i in next_states:            
            if i.config not in frontierDict:             
                frontier.append(i)
                frontierDict[i.config] = i

            if i.cost >= max_search_depth :
                    max_search_depth = i.cost
                    
def ast(initial_state,goal_state = (0,0,False)):
    """A* search"""
    print('*** Running A* ***')
    time1 = time.time()
    max_search_depth = 0
    expanded = -1
    frontier = PriorityQueue()
    frontierDict = {}
    frontier.put(initial_state,0)
    while not frontier.empty():
        #REMOVE
#   
        state = frontier.get()
        expanded += 1
        frontierDict[state.config] = state
        state.expand()
        
        #GOAL CHECK
        if state.config == goal_state:
            
            goalPrint(state,expanded)
            print('max_search_depth: ',max_search_depth)
            print('running_time: ', time.time()-time1)
            return state
          
        next_states = state.expand()
        for i in next_states: 
            
            new_cost = i.add_cost(heuristics(i.config)) 
            if i.config in frontierDict :
#                print(frontierDict[i.config].heuristic_cost)
                if new_cost < frontierDict[i.config].heuristic_cost :
                    frontierDict[i.config] = i
            else :
                frontier.put(i,new_cost)
                frontierDict[i.config] = i
                
            if i.cost >= max_search_depth :
                max_search_depth = i.cost 



start_state = PuzzleState((3,3,True))

sm = sys.argv[1].lower()
if sm == 'bfs':
    final_state = bfs_search(start_state)
if sm == 'dfs':
    final_state = dfs_search(start_state)
if sm == 'ast':
    final_state = ast(start_state)

goal_states = []
while final_state.parent != None:
        goal_states.append(final_state)
        final_state = final_state.parent
goal_states.reverse()
goal_states = [g.config for g in goal_states]
#dot.render('test-output/round-table-3.gv', view=True)

##################### ENTER PYGAME ##################################33


 
import pygame, sys
from pygame.locals import *
from time import sleep

pygame.init()
pygame.mixer.init()
DISPLAYSURF = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Jesus and Demons!!')

white=(255,255,255)
green=(154,205,50)
brown=(165,42,42)
treeGreen=(0,255,0)
orange=(255,127,80)
sky=(135,206,235)
water=(65,105,225)
flag=(220,20,60)

clock = pygame.time.Clock()


def draw_tree():
    pygame.draw.rect(DISPLAYSURF, brown, [108, 220, 20, 100])
    pygame.draw.polygon(DISPLAYSURF, treeGreen, [[190, 220], [115, 70], [40, 220]])
    pygame.draw.polygon(DISPLAYSURF, treeGreen, [[180, 170], [115, 50], [50, 170]])

def draw_tree2():
    pygame.draw.rect(DISPLAYSURF, brown, [260, 400, 30, 100])
    pygame.draw.polygon(DISPLAYSURF, treeGreen, [[350, 400], [275, 250], [200, 400]])
    pygame.draw.polygon(DISPLAYSURF, treeGreen, [[340, 350], [275, 230], [210, 350]])

def sun():
    pygame.draw.circle(DISPLAYSURF,orange, (400,80),75)

class jesus_class(pygame.sprite.Sprite):
    def __init__(self,centerx, centery):                                  #(100,350) -- jesus1, (150,350) -- jesus2 , (200,350) -- jesus3
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('jesus.png')
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        self.leftx = centerx
        self.lefty = centery
        self.state = True


    def moveToboat(self,ele):
        print('Jesus MOVVVEEEVEVEGVEH')
        if(boat.numberOnboard == 1):
            self.rect.center = (boat.rect.x+40,boat.rect.y+30)
        elif(boat.numberOnboard ==2):
            self.rect.center = (boat.rect.x+90,boat.rect.y+30)
        boat.element.append(ele)
        if(self.state == True):
            self.state = False
        else:
            self.state = True

    def moveToground(self):
        print('Jesus heree')
        print(state.boat)
        print(self.leftx)
        if(state.boat == True):
                self.rect.center = (self.leftx+500,  self.lefty)
        if(state.boat == False):
                self.rect.center = (self.leftx, self.lefty)


class demon_class(pygame.sprite.Sprite):
    def __init__(self, centerx,centery):
        pygame.sprite.Sprite.__init__(self)                             #(80,410) , (140,410), (200,410)
        self.image=pygame.image.load('demonnn.png')
        self.rect = self.image.get_rect()
        self.rect.center = (centerx,centery)
        self.leftx = centerx
        self.lefty = centery
        self.state = True

    def moveToboat(self,ele):
        print('MOVVVEEEVEVEGVEH')
        if(boat.numberOnboard == 1):
            self.rect.center = (boat.rect.x+40,boat.rect.y+30)
        elif(boat.numberOnboard ==2):
            self.rect.center = (boat.rect.x+90,boat.rect.y+30)
        boat.element.append(ele)
        if(self.state == True):
            self.state = False
        else:
            self.state = True

    def moveToground(self):
        print('heree')
        print(state.boat)
        print(self.leftx)
        if(state.boat == True):
                self.rect.center = (self.leftx+500,  self.lefty)
        if(state.boat == False):
                self.rect.center = (self.leftx, self.lefty)






class boat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('boatt.png')
        self.rect = self.image.get_rect()
        self.rect.center = (362.5,410)
        self.numberOnboard = 0
        self.element =[]

    def update_boat(self):
            print(self.rect.centerx)
            if(state.boat==True):
                while(self.rect.centerx<450):
                    self.rect.centerx +=5
                    print(self.rect.centerx)
                    self.rect.center=(self.rect.centerx,410)
                    print(self.element[0])
                    self.element[0].rect.center=(boat.rect.x+40,boat.rect.y+30)
                    if(boat.numberOnboard == 2):
                        self.element[1].rect.center=(boat.rect.x+90,boat.rect.y+30)
            else:
                while(self.rect.centerx>362):
                    self.rect.centerx -=5
                    print(self.rect.centerx)
                    self.rect.center=(self.rect.centerx,410)
                    print(self.element[0])
                    self.element[0].rect.center=(boat.rect.x+40,boat.rect.y+30)
                    if(boat.numberOnboard == 2):
                        self.element[1].rect.center=(boat.rect.x+90,boat.rect.y+30)






class state():
    def __init__(self):
        self.leftJesus = 3
        self.leftDemon = 3
        self.rightJesus = 0
        self.rightDemon = 0
        self.boat = True
        self.moves = 0

def message():
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    # string = str('[' + state.leftJesus + ' ' + state.leftDemon + ' ' + state.boat)
    textsurface_states = myfont.render('[' + str(state.leftJesus) + ' ' + str(state.leftDemon) + ' ' + str(state.boat) +']', False, (0, 0, 0))
    DISPLAYSURF.blit(textsurface_states,(0,0))

    textsurface_moves = myfont.render('Moves:' + str(state.moves), False, (0,0,0))
    DISPLAYSURF.blit(textsurface_moves,(650,0))



all_sprites = pygame.sprite.Group()
jesus1 = jesus_class(100,350)
jesus2 = jesus_class(150,350)
jesus3 = jesus_class(200,350)
demon1 = demon_class(80,410)
demon2 = demon_class(140,410)
demon3 = demon_class(200,410)
boat = boat()
all_sprites.add(jesus1,jesus2,jesus3,demon1,demon2,demon3,boat)
state=state()


i = 0
end = False


while True: # main game loop

    #Draw on screen
    DISPLAYSURF.fill(sky)
    pygame.draw.rect(DISPLAYSURF,green,(0,200,300,400))       #(x,y,width,height)
    pygame.draw.rect(DISPLAYSURF,green,(500,200,300,400))
    pygame.draw.rect(DISPLAYSURF,water,(300,200,200,400))
    draw_tree()
 
    sun()


    all_sprites.draw(DISPLAYSURF)

    message()


    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if (state.leftJesus == 0 and state.leftDemon == 0):
                end = True
                break

            else:
                if (state.leftJesus != goal_states[i][0]):
                    n = abs(state.leftJesus - goal_states[i][0])

                    for y in range(n):
                        boat.numberOnboard += 1
                        if(state.boat == True):
                            if (jesus1.state == True ):
                                jesus1.moveToboat(jesus1)
                            elif (jesus2.state == True):
                                jesus2.moveToboat(jesus2)
                            elif (jesus3.state == True):
                                jesus3.moveToboat(jesus3)
                        else:
                            if (jesus1.state == False ):
                                jesus1.moveToboat(jesus1)
                            elif (jesus2.state == False):
                                jesus2.moveToboat(jesus2)
                            elif (jesus3.state == False):
                                jesus3.moveToboat(jesus3)

                if (state.leftDemon != goal_states[i][1]):
                    print(i)
                    n = abs(state.leftDemon - goal_states[i][1])
                    for y in range(n):
                        boat.numberOnboard +=1
                        if(state.boat == True):
                            if (demon1.state == True ):
                                demon1.moveToboat(demon1)
                            elif (demon2.state == True):
                                demon2.moveToboat(demon2)
                            elif (demon3.state == True):
                                demon3.moveToboat(demon3)
                        else:
                            print('dhinkaajasdk')
                            if (demon1.state == False ):
                                demon1.moveToboat(demon1)
                            elif (demon2.state == False):
                                demon2.moveToboat(demon2)
                            elif (demon3.state == False):
                                demon3.moveToboat(demon3)

                boat.update_boat()

                if(boat.numberOnboard == 1):
                        boat.element[0].moveToground()
                elif(boat.numberOnboard ==2):
                        print(boat.element[0])
                        boat.element[0].moveToground()
                        boat.element[1].moveToground()
                boat.element = []
                boat.numberOnboard = 0

                pygame.time.wait(500)
                pygame.event.clear()

                state.leftJesus=goal_states[i][0]
                state.rightJesus= 3 - state.leftJesus


                state.leftDemon=goal_states[i][1]
                state.rightDemon= 3 - state.leftDemon

                state.moves +=1
                if (state.boat == True):
                    print('hiyyayayyayadyayu')
                    state.boat = False
                else:
                    state.boat = True
                print('akjsdbkjasnd')
                print(state.boat)
                print(demon1.state)
                print(state.leftDemon)
                print(state.rightDemon)
                print(state.leftJesus)
                print(state.rightJesus)
                i = i+1
                print("END")




        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if(end == True ):
        end_game=pygame.image.load('PewDiePie.png')
        DISPLAYSURF.blit(end_game,(350,180))


    #Update
    pygame.display.update()
    all_sprites.update()
    clock.tick(20)








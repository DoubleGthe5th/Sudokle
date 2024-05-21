import random
import pygame

#CREATES SUDOKU
sudoku = [
    [4,5,3,8,2,6,1,9,7],
    [8,9,2,5,7,1,6,3,4],
    [1,6,7,4,9,3,5,2,8],
    [7,1,4,9,5,2,8,6,3],
    [5,8,6,1,3,7,2,4,9],
    [3,2,9,6,8,4,7,5,1],
    [9,3,5,2,1,8,4,7,6],
    [6,7,1,3,4,5,9,8,2],
    [2,4,8,7,6,9,3,1,5],
]
#shuffles rows
for x in range(0,9,3):
    rows = [x,x+1,x+2]
    random.shuffle(rows)
    a = sudoku[x]
    b = sudoku[x+1]
    c = sudoku[x+2]
    sudoku[rows[0]] = a
    sudoku[rows[1]] = b
    sudoku[rows[2]] = c 
#shuffle columns
for x in range(0,9,3):
    rows = [x,x+1,x+2]
    random.shuffle(rows)
    a = [r[x] for r in sudoku]
    b = [r[x+1] for r in sudoku]
    c = [r[x+2] for r in sudoku]
    for r in range(9):
        sudoku[r][rows[0]] = a[r] 
        sudoku[r][rows[1]] = b[r] 
        sudoku[r][rows[2]] = c[r] 
#shuffles numbers
numbers = [1,2,3,4,5,6,7,8,9]
random.shuffle(numbers)
for x in range(9):
    for y in range(9):
        sudoku[x][y] = numbers.index(sudoku[x][y]) + 1
for row in sudoku:
    print(row)

#starting stuff
pygame.init()
screen = pygame.display.set_mode((800,800))
n = 3
displayedboard = [[[] for x in range(n**2)] for x in range(n**2)]#guesses 
solvedboard = [[[] for x in range(n**2)] for x in range(n**2)]#actual numbers typed while solving
#fonts
tiles_font = pygame.font.SysFont("Times New Roman",size=int(600/(n**2))-2)
chars = [chr(x) for x in range(49,49+9)]+ [chr(48)] + [chr(x) for x in range(65+32,65+32+26)] + [chr(x) for x in range(65,65+26)] + ["!","@","#","$","%","^","&","*","(",")"] + [",",".","/",";","'","[","]","\\","-","="] + ['<',">","?",":","\"","{","}","|","_","+"] + [chr(x) for x in range (130,138)] #chars for game
print(chars)
#specific to this
rowchosen = 0
numbersinputted = 0
colors = [[],[],[],[],[],[],[],[],[]]
showclues = True

#main running
mode = "inputting"
running = True
while running:
    if mode == "inputting":    
        #does events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                #edit board
                if pos[0] >= 100 and pos[0] <= 700 and pos[1] >= 100 and pos[1] <= 700:
                    pos[0] -=100 
                    pos[0] -= (pos[0]%int(600/(n**2)))
                    pos[0] /= int(600/(n**2))
                    pos[1] -=100 
                    pos[1] -= (pos[1]%int(600/(n**2)))
                    pos[1] /= int(600/(n**2))
                    selected = [int(pos[0]),int(pos[1])]
            elif event.type == pygame.KEYDOWN:
                try:
                    char = ord(chr(event.key))
                except:
                    pass
                else:
                    #Input number
                    if char > 48 and char < 58 and numbersinputted < 9 and rowchosen != 9:
                        displayedboard[rowchosen][numbersinputted] = [char - 49]
                        numbersinputted += 1
                    #Submit row
                    elif (char == 13 or char == 10) and numbersinputted == 9 and rowchosen != 9:
                        rowchosen += 1
                        numbersinputted = 0
                        for x in range(9):
                            d = displayedboard[rowchosen - 1][x][0] + 1
                            if sudoku[rowchosen - 1][x] == d:
                                colors[rowchosen - 1].append("Y")
                            else:
                                if sudoku[rowchosen - 1][x - x%3] == d or sudoku[rowchosen - 1][x - x%3 + 1] == d or sudoku[rowchosen - 1][x - x%3 + 2] == d:
                                    colors[rowchosen - 1].append("M")  
                                else:
                                    colors[rowchosen - 1].append("N")
                        if rowchosen == 9:
                            mode = "solving"
                            selected = [8,8]
                    elif char == 8 and numbersinputted > 0 and rowchosen != 9:
                        displayedboard[rowchosen][numbersinputted - 1] = []
                        numbersinputted -= 1
        #renders board


        screen.fill((255,255,255))
        #small lines
        for x in range(len(displayedboard)):
            for y in range(len(displayedboard[0])):
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*x-1,100+600/(n**2)*y-1),(600/(n**2)+2,600/(n**2)+2)),color=(0,0,0))
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*x,100+600/(n**2)*y),(600/(n**2),600/(n**2))),color=(255,255,255))
        #colors
        for x in range(len(colors)):
            for y in range(len(colors[x])):
                color = (255,255,255)   
                if colors[x][y] == "Y":
                    color = (0,150,0)
                elif colors[x][y] == "M":
                    color = (200,100,0)
                elif colors[x][y] == "N":
                    color = (150,150,150)
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*y,100+600/(n**2)*x),(600/(n**2),600/(n**2))),color=color)
        #text
        for x in range(len(displayedboard)):
            for y in range(len(displayedboard[0])):
                if displayedboard[x][y] != []:
                    text = tiles_font.render(chars[displayedboard[x][y][0]],True,(0,0,0))
                    screen.blit(text,text.get_rect(center=(100+600/(n**2)*(y+0.5),100+600/(n**2)*(x+0.5))))
        #large lines
        for x in range(n+1):
            pygame.draw.line(surface=screen,start_pos=(100,100+600/n*x),end_pos=(100+600,100+600/n*x),color=(0,0,0),width=3)
            pygame.draw.line(surface=screen,start_pos=(100+600/n*x,100), end_pos=(100+600/n*x,100+600),color=(0,0,0),width=3)
        pygame.display.flip()      
    
    
    
    
    
    
    
    
    elif mode == "solving":
        #does events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = list(pygame.mouse.get_pos())
                #clicks the showclues button
                if pos[0] >= 100 and pos[0] <= 150 and pos[1] >= 10 and pos[1] <= 60:
                    showclues = not showclues
                #edit board
                if pos[0] >= 100 and pos[0] <= 700 and pos[1] >= 100 and pos[1] <= 700:
                    pos[0] -=100 
                    pos[0] -= (pos[0]%int(600/(n**2)))
                    pos[0] /= int(600/(n**2))
                    pos[1] -=100 
                    pos[1] -= (pos[1]%int(600/(n**2)))
                    pos[1] /= int(600/(n**2))
                    selected = [int(pos[0]),int(pos[1])]
            elif event.type == pygame.KEYDOWN:
                try:
                    char = ord(chr(event.key))
                except:
                    pass
                else:
                    #Input number
                    if char > 48 and char < 58:
                        solvedboard[selected[0]][selected[1]] = [char - 49] 
                    elif char == 8:
                        solvedboard[selected[0]][selected[1]] = []               
        #renders board


        screen.fill((255,255,255))
        #small lines
        for x in range(len(displayedboard)):
            for y in range(len(displayedboard[0])):
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*x-1,100+600/(n**2)*y-1),(600/(n**2)+2,600/(n**2)+2)),color=(0,0,0))
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*x,100+600/(n**2)*y),(600/(n**2),600/(n**2))),color=(255,255,255))
        if showclues:
            #colors
            for x in range(len(colors)):
                for y in range(len(colors[x])):
                    color = (255,255,255)   
                    if colors[x][y] == "Y":
                        color = (0,150,0)
                    elif colors[x][y] == "M":
                        color = (200,100,0)
                    elif colors[x][y] == "N":
                        color = (150,150,150)
                    pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*y,100+600/(n**2)*x),(600/(n**2),600/(n**2))),color=color)
            #selected tile
            pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*selected[0],100+600/(n**2)*selected[1]),(600/(n**2),600/(n**2))),color=(143,235,213))
            #text of guesses
            for x in range(len(displayedboard)):
                for y in range(len(displayedboard[0])):
                    if displayedboard[x][y] != []:
                        text = tiles_font.render(chars[displayedboard[x][y][0]],True,(0,0,0))
                        screen.blit(text,text.get_rect(center=(100+600/(n**2)*(y+0.5),100+600/(n**2)*(x+0.5))))
        else:
            #selected tile
            if colors[selected[1]][selected[0]] == "Y":
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*selected[0],100+600/(n**2)*selected[1]),(600/(n**2),600/(n**2))),color=(143,235,213))
            elif colors[selected[1]][selected[0]] == "M":
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*selected[0],100+600/(n**2)*selected[1]),(600/(n**2),600/(n**2))),color=(235,229,143))
            else:
                pygame.draw.rect(surface=screen,rect=((100+600/(n**2)*selected[0],100+600/(n**2)*selected[1]),(600/(n**2),600/(n**2))),color=(156,156,156))    

        #text of solved board
        for x in range(len(solvedboard)):
            for y in range(len(solvedboard[0])):
                if solvedboard[x][y] != []:
                    if solvedboard[x][y][0] + 1 == sudoku[y][x]:
                        text = tiles_font.render(chars[solvedboard[x][y][0]],True,(0,0,255))
                    else:
                        text = tiles_font.render(chars[solvedboard[x][y][0]],True,(255,0,0))
                    screen.blit(text,text.get_rect(center=(100+600/(n**2)*(x+0.5),100+600/(n**2)*(y+0.5))))
        #show clues button
        pygame.draw.rect(surface=screen,rect=((100,10),(50,50)),color=(170,170,170))
        #large lines
        for x in range(n+1):
            pygame.draw.line(surface=screen,start_pos=(100,100+600/n*x),end_pos=(100+600,100+600/n*x),color=(0,0,0),width=3)
            pygame.draw.line(surface=screen,start_pos=(100+600/n*x,100), end_pos=(100+600/n*x,100+600),color=(0,0,0),width=3)
        pygame.display.flip()  
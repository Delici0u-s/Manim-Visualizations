from manim import *
import numpy as np

array1o = np.array([
    [1, 0, 3, -2],
    [0, 1, 4, 1],
    [0, 0, 0, 0]
    ])
array1 = np.array([
    [1, 2, 0, 3, 5, 0, 0, 7, 0],
    [0, 0, 1, 4, 6, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 1, 0, 9, 0],
    [0, 0, 0, 0, 0, 0, 1, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    ])

def GetHermanIndexLinePoints(arr):
    out = []
    height = len(arr)
    width = len(arr[0])
    foundhor = -1
    for row in range(width):
        foundvert = 0
        for col in range(height-1, -1, -1):
            curr = arr[col][row]
            if (curr != 0 and col >= foundvert and (col > foundhor or col == height-1)):
                foundvert = col
                foundhor = col
                # print("Row: ", row, " FoundHor: ", foundhor)
                #out.append(row + col * (height+1))
                out.append(np.ravel_multi_index((col, row), arr.shape))
                
    for col in range(height):
        if np.all(arr[col] == 0):
            out.append(np.ravel_multi_index((col, width-1), arr.shape))
            break
    
    # print(out)
    return out

def GetRedLine(Matrix, array):
            matrix_mob = Matrix.get_entries()
        
            yas = GetHermanIndexLinePoints(array)
            CenteredElements = [matrix_mob[yas[i]].get_center() for i in range(len(yas))]
            
            vertical_distance = abs(matrix_mob[0].get_y() - matrix_mob[len(array[0]+1)].get_y())*0.5
            horizontal_distance = abs(matrix_mob[0].get_x() - matrix_mob[1].get_x())*0.5
            PercDOWN = DOWN * vertical_distance
            PercUP = UP * vertical_distance
            PercLEFT = LEFT * horizontal_distance + RIGHT * 0.3
            PercRIGHT = RIGHT * horizontal_distance + RIGHT * 0.3
            def DrawRightAngle(index):
                vertical_line = Line(
                    CenteredElements[index] + PercUP + PercLEFT,
                    CenteredElements[index] + PercDOWN + PercLEFT,
                    color=RED
                )
                
                try:
                    CenteredElements[index+1]
                    DoTrans = CenteredElements[index+1] + PercUP - PercRIGHT * 0.3
                except:
                    DoTrans = CenteredElements[index] + PercDOWN + PercRIGHT * 0.3
                    pass
                    
                horizontal_line = Line(
                        CenteredElements[index] + PercLEFT + PercDOWN,
                        DoTrans,
                        color=RED
                    )
                
                return VGroup(vertical_line, horizontal_line)
            
            out = []
            for i in range(len(yas)):
                out.append(DrawRightAngle(i))
            '''
            balls = []
            for i in range(len(yas)):
                balls.append(Cube(fill_opacity=0, stroke_width=2, side_length=horizontal_distance).move_to(CenteredElements[i]))
            '''
            return VGroup(*out)
        
def WriteXHeaders(Matrix, array):
    matrix_mob = Matrix.get_entries()
        
    yas = GetHermanIndexLinePoints(array)
    CenteredElements = [matrix_mob[yas[i]].get_center() for i in range(len(yas))]
    
    vertical_distance = abs(matrix_mob[0].get_y() - matrix_mob[len(array[0]+1)].get_y())*0.5
    horizontal_distance = abs(matrix_mob[0].get_x() - matrix_mob[1].get_x())*0.5
    PercDOWN = DOWN * vertical_distance
    PercUP = UP * vertical_distance
    PercLEFT = LEFT * horizontal_distance + RIGHT * 0.3
    PercRIGHT = RIGHT * horizontal_distance + RIGHT * 0.3
    
    out = []
    toppos = (Matrix.get_top() + UP * 0.3)[1]
    pos = [(Matrix.get_left()+PercRIGHT*0.65)[0], toppos, 0]
    
    for i in range(len(array[0])):
        out.append(MathTex(f"x_{i}", color=GREEN).move_to(pos))
        pos += RIGHT * horizontal_distance * 2
    
    return VGroup(*out)
    
    
class Hermische_Normalform(Scene):
    def construct(self):
        visuMatrix1 = Matrix(array1)
        self.add(visuMatrix1)
        # self.play(Write(visuMatrix1))
        self.wait(1)

        
        self.play(Write(WriteXHeaders(visuMatrix1, array1)))
        
        self.play(Create(GetRedLine(visuMatrix1, array1)))
        
        self.wait(2)

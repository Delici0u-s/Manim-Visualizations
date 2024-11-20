
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
# test
def GetHermanIndexLinePoints(arr):
    out = []
    height = len(arr)
    width = len(arr[0])
    
    # access array in transformed position and grab total Index, only for edges
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

    # checks if row is entirely nulls, makes that the end ish
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
    PercRIGHT = RIGHT * horizontal_distance

    out = []
    toppos = (Matrix.get_top() + UP * 0.3)[1]
    pos = [(Matrix.get_left()+PercRIGHT)[0]-0.1, toppos, 0]

    for i in range(len(array[0])):
        out.append(MathTex(f"x_{i}", color=GREEN).move_to(pos))
        pos += PercRIGHT*2+[0.02, 0, 0]
        # pos += PercRIGHT  # HERE RIGHT HERE CHATGPT

    return VGroup(*out)

ImpHeaderIDs = []

def GetImportantColumnHighlighterBox(Matrix, array, Headers):
    matrix_mob = Matrix.get_entries()

    vertical_distance = abs(matrix_mob[0].get_y() - matrix_mob[len(array[0]+1)].get_y())*0.5
    horizontal_distance = abs(matrix_mob[0].get_x() - matrix_mob[1].get_x())*0.5
    PercDOWN = DOWN * vertical_distance
    PercLEFT = LEFT * horizontal_distance + RIGHT * 0.3
    PercRIGHT = RIGHT * horizontal_distance + RIGHT * 0.3
    
    
    
    out = []
    asd = [0 for i in range((len(array[0])))]
    for i in range(len(array[0])):
        prev = False
        for j in range(len(array)-1, -1, -1):
            if prev or array[j][i] != 0:
                prev = True
                asd[i] += 1
                
    for count, i in enumerate(Headers, start=0):
        try:
            if asd[count] == asd[count-1]:
                ImpHeaderIDs.append(count)
                Tangle = RoundedRectangle(color=PURE_RED ,corner_radius=0.25*PercRIGHT[0], width=2*PercLEFT[0], height=PercDOWN[1]*asd[count]*2+PercDOWN[1]*1.5)
                out.append(Tangle.move_to(i.get_center()+(PercDOWN*asd[count])))
        except:
            pass
        
    return out

def Create_Solution(self, Matrix):
    self.add(Cube())
    return None
class Hermische_Normalform(Scene):
    def construct(self):
        visuMatrix1 = Matrix(array1)
        self.add(visuMatrix1)
        # self.play(Write(visuMatrix1))
        # self.wait(1)

        MatrixHeaders = WriteXHeaders(visuMatrix1, array1)
        self.add(MatrixHeaders)
        # self.play(Write(MatrixHeaders))

        RedIndicatorLine = GetRedLine(visuMatrix1, array1)
        self.add(RedIndicatorLine)
        # self.play(Create(RedIndicatorLine))
        # self.wait(1)
        
        ImportantLines = GetImportantColumnHighlighterBox(visuMatrix1, array1, MatrixHeaders)
        self.play(
            AnimationGroup(
                *[TransformFromCopy(MatrixHeaders[ImpHeaderIDs[i]], ImportantLines[i]) for i in range(len(ImportantLines))],
                lag_ratio=0.1,
            )
        )
        # ImportantLinesGroup = VGroup(*ImportantLines)
        # self.play(Create(ImportantLinesGroup))
        self.wait(2)
        self.play(
            AnimationGroup(
                *[Transform(ImportantLines[i], MatrixHeaders[ImpHeaderIDs[i]]) for i in range(len(ImportantLines))],
                lag_ratio=0.1,
            )
        )
        Create_Solution(self, visuMatrix1)
        
        self.wait(2)

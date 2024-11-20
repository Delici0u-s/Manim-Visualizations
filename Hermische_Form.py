
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
                    DoTrans = CenteredElements[index+1] + PercUP - PercRIGHT * 0.29
                except:
                    DoTrans = CenteredElements[index] + PercDOWN + PercRIGHT * 0.29
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
        out.append(MathTex(f"x_{i+1}", color=GREEN).move_to(pos))
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
    asd = [0 for _ in range((len(array[0])))]
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

def Create_Solution(self, Matrix, array, MatrixHeaders, ImportantLine, RowID, AdditionalObjects):
    matrix_mob = Matrix.get_entries()
    yas = GetHermanIndexLinePoints(array)
    
    ColumnID = ImpHeaderIDs[RowID]
    
    for i in range(len(array)-1, -1, -1):
        if array[i][ColumnID] != 0:
            MaxItemID = np.ravel_multi_index((i, ColumnID), array.shape)
            break
    
    CleanupObjects = VGroup()
    
    # self.play(TransformFromCopy(MatrixHeaders[ColumnID], ImportantLine))
    # self.play(Transform(ImportantLine, MatrixHeaders[ColumnID]))
    
    CurrentItemSelector = Elbow(width=0.5, angle = 5*PI/4, color=PURE_RED).move_to(MatrixHeaders[ColumnID].get_bottom()+DOWN*0.1)
    CleanupObjects.add(CurrentItemSelector)
    self.play(Create(CurrentItemSelector))
    
    ResetOutputMatrix(self, AdditionalObjects[3], array)
    
    Items = []
    for i in range(len(array)):
        MatrixMobPos = np.ravel_multi_index((i, ColumnID), array.shape)
        if MatrixMobPos <= MaxItemID:
            Items.append(matrix_mob[MatrixMobPos])
            self.play(Create(Cube(side_length=0.5).move_to(matrix_mob[MatrixMobPos].get_center())))


    
    
    #FirstLineOne(self, MatrixHeaders[ColumnID], AdditionalObjects[3][0][ColumnID])
    
    for i in range(len(Items)-1, -1, -1):
        #PutInto(self, Items[i], matrix_mob[yas[i]], MatrixHeaders[yas[i]%len(array[0])], AdditionalObjects[3][0][yas[i]%len(array[0])], AdditionalObjects[0])
        ...
        
    otherItemsArr = set()
    for i in range(len(Items)):
        otherItemsArr.add(yas[i]%len(array[0]))
        
    print(otherItemsArr)
    outMats = []
    for i in range(len(AdditionalObjects[3][0])):
        if  i != ColumnID and i not in otherItemsArr:
            outMats.append(AdditionalObjects[3][0][i])
            
    if outMats:
        self.play(AnimationGroup(
                *[Transform(outMats[i], MathTex("0").move_to(outMats[i].get_center())) for i in range(len(outMats))],
                lag_ratio=0.1,
            ))
    
    
    self.play(FadeOut(CleanupObjects), scale=0.5)
    return None

def PutInto(self, OrigMatrixObj, OrigMatrixGoal, HeaderObj, EndMatrixObj, NegativeOne):
    tmpObj = OrigMatrixObj.copy()
    tmpObj.generate_target()
    tmpObj.target.move_to(OrigMatrixGoal.get_center())
    
    self.play(MoveToTarget(tmpObj))
    
    tmpObj.target.move_to(HeaderObj.get_center()+UP*0.8)
    self.play(MoveToTarget(tmpObj))
    
    tmpCopyOne = NegativeOne.copy()
    tmpCopyOne.generate_target()
    tmpCopyOne.target.move_to(tmpObj.get_center())
    
    self.play(MoveToTarget(tmpCopyOne))
    
    tmp = MathTex(str(int(tmpObj.get_tex_string())*int(tmpCopyOne.get_tex_string()))).move_to(tmpObj.get_center())
    tmp2 =  VGroup(tmpObj, tmpCopyOne)
    self.play(Transform(
        tmp2,
        tmp
    ))
    
    tmp2.generate_target()
    tmp2.target.move_to(EndMatrixObj.get_center())
    self.play(MoveToTarget(tmp2))
    
    self.play(Transform(EndMatrixObj, tmp2))
    self.remove(tmp2)
    
def FirstLineOne(self, HeaderObj, EndMatrixObj):
    Oneobj = MathTex("1").move_to(HeaderObj.get_center())
    self.play(TransformFromCopy(HeaderObj, Oneobj))
    
    Oneobj.generate_target()
    Oneobj.target.move_to(HeaderObj.get_center()+UP*0.8)
    self.play(MoveToTarget(Oneobj))
    Oneobj.target.move_to(EndMatrixObj.get_center())
    self.play(MoveToTarget(Oneobj))
    
    self.play(Transform(EndMatrixObj, Oneobj))
    self.remove(Oneobj)

def AddAdditionalObjects(self, visuMatrix1, array, MatrixHeaders, RedIndicatorLine):
    
    NegativeOneTopRight = MathTex("-1").to_corner((UP + LEFT)*.5)
    SolutionSymbols = MathTex("\mathbb{L}: ").to_corner(DOWN + RIGHT).shift(LEFT*1.5)
        
    AllRelevntObject = VGroup(visuMatrix1, *MatrixHeaders, *RedIndicatorLine)
    self.play(AllRelevntObject.animate.shift(LEFT * 1.3))
    OutText = MathTex("=>").move_to(visuMatrix1.get_right()+RIGHT*0.7)
    
    tmpArr = [[f"x_{i+1}"] for i in range(len(array[0]))]
    OutMatrix = Matrix(tmpArr)
    OutMatrix.move_to(OutText.get_right() + RIGHT*0.7)
    
    
    self.play(FadeIn(OutText))
    self.play(AnimationGroup(
        FadeIn(OutMatrix),
        FadeIn(SolutionSymbols),
        lag_ratio=0.1,
    ))
    
    self.play(FadeIn(NegativeOneTopRight))
    
    out = [NegativeOneTopRight, AllRelevntObject, OutText, OutMatrix, SolutionSymbols]
    # [0] is -1 top right;  [1] is the group of to the right shifted elements;  [2] is the =>;  [3] is the ResultMatrix;   [4] is the LösungsMengeSymbol
    return out


def ResetOutputMatrix(self, visMatrix, array):
    tmpArr = [[f"x_{i+1}"] for i in range(len(array[0]))]
    refreshMatrix = Matrix(tmpArr).move_to(visMatrix.get_center())
    
    visMatrixMob = visMatrix.get_entries()
    refreshMatrixMob = refreshMatrix.get_entries()
    
    self.play(AnimationGroup(
            *[Transform(visMatrixMob[i], refreshMatrixMob[i]) for i in range(len(refreshMatrixMob))],
            lag_ratio=0.1,
        ))
        

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
        """
        self.play(
            AnimationGroup(
                *[TransformFromCopy(MatrixHeaders[ImpHeaderIDs[i]], ImportantLines[i]) for i in range(len(ImportantLines))],
                lag_ratio=0.1,
            )
        )
        
        
        self.wait(2)
        self.play(
            AnimationGroup(
                *[Transform(ImportantLines[i], MatrixHeaders[ImpHeaderIDs[i]]) for i in range(len(ImportantLines))],
                lag_ratio=0.1,
            )
        )
        """
        
        
        AddObjOutput = AddAdditionalObjects(self, visuMatrix1, array1, MatrixHeaders, RedIndicatorLine)
        # [0] is -1 top right;  [1] is the group of to the right shifted elements;  [2] is the =>;  [3] is the ResultMatrix;   [4] is the LösungsMengeSymbol
        
        
        
        
        for i in range(len(ImpHeaderIDs)):
            Create_Solution(self, visuMatrix1, array1, MatrixHeaders, ImportantLines[i], i, AddObjOutput)
        
        self.wait(2)

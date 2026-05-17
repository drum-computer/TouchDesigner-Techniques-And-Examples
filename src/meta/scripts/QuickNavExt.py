
class QuickNavExt:
    """
    QuickNavExt description
    """
    def __init__(self, ownerComp: baseCOMP):
        self._ownerComp: baseCOMP = ownerComp 
        self._navPoints: list[OP] = []
        self._currentPoint: int = 0
        self._mainPane: Pane = ui.panes[0]
    
    def OnPrevious(self):
        numPoints: int = len(self._navPoints)
        if(numPoints == 0):
            return

        if(self._currentPoint <= 0):
            self._currentPoint = numPoints - 1
        else:
            self._currentPoint -= 1

        self._mainPane.home(zoom=True, op=self._navPoints[self._currentPoint])

    def OnNext(self):
        numPoints: int = len(self._navPoints)
        if(numPoints == 0):
            return
        if(self._currentPoint >= numPoints):
            self._currentPoint = 0
        else:
            self._currentPoint += 1

        self._mainPane.home(zoom=True, op=self._navPoints[self._currentPoint])
    

    def OnRestart(self):
        if(len(self._navPoints) == 0):
            return
        self._mainPane.home(zoom=True, op=self._navPoints[0])
        self._currentPoint = 0
                                
        

    def OnAdd(self):
        currentOp: OP = self._ownerComp.parent().currentChild
        print(f'added {currentOp} to the list of nav points')
        self._navPoints.append(currentOp)

    def OnDelete(self):
        pass

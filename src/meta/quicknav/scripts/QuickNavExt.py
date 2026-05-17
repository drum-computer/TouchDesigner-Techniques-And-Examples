class QuickNavExt:
    """
    Quicknav is a component that let's you add custom navigation points
    across your TouchDesigner project and then jump between them
    IMPORTANT: this component assumes that your network view is Pane 0
    which might not always be the case. 
    """
    def __init__(self, ownerComp: baseCOMP):
        self._ownerComp: baseCOMP = ownerComp 
        self._navPoints: list[OP] = []
        self._currentPoint: int = 0
        self._mainPane: Pane = ui.panes[0]
        # shows to the user where we are in current nav
        self._currentText: parStr = self._ownerComp.par['Current']
        # show initial navigation
        self._currentText.val = 'no navigation points'
        self._changelogOp = op('changelog')
        self._helpOp = op('help')
    
    def OnPrevious(self):
        numPoints: int = len(self._navPoints)
        if(numPoints == 0):
            debug('no navigation points exist')
            return

        if(self._currentPoint <= 0):
            self._currentPoint = numPoints - 1
        else:
            self._currentPoint -= 1

        self._goTo(self._currentPoint)

    def OnNext(self):
        numPoints: int = len(self._navPoints)
        if(numPoints == 0):
            debug('no navigation points exist')
            return

        if(self._currentPoint >= (numPoints-1)):
            self._currentPoint = 0
        else:
            self._currentPoint += 1

        self._goTo(self._currentPoint)
    
    def OnRestart(self):
        if(len(self._navPoints) == 0):
            debug('no navigation points exist')
            return
        self._currentPoint = 0
        self._goTo(self._currentPoint)
                                
    def OnAdd(self):
        # get currently selected operator
        currentOp: OP = self._mainPane.owner.currentChild
        if currentOp in self._navPoints:
            print(f'{currentOp} is already in list of nav points')
            return
        self._navPoints.append(currentOp)
        print(f'added {currentOp} to the list of nav points')
        self._updateCurrentText()

    def OnDelete(self):
        if(len(self._navPoints) == 0):
            debug('no navigation points exist')
            return
        deletedOp = self._navPoints.pop(self._currentPoint)
        print(f'deleted {deletedOp} from the list of nav points')
        if(self._currentPoint > 0):
            self._currentPoint -= 1
        self._updateCurrentText()

    def OnImport(self):
        importDAT = self._ownerComp.par.Importfromdat.eval()
        if type(importDAT) != tableDAT:
            debug('import target must be a table dat with one collumn listing paths to operators')
        extractedOps = [] # this is needed to be able to abort in case we won't be able to extract all ops
        for v in importDAT.rows(val=True):
            extractedOp = op(v[0])
            if extractedOp == None:
                debug(f'couldn\'t find an operator with path: {v}')
                continue
            extractedOps.append(extractedOp)
        self._navPoints.extend(extractedOps)
        self._goTo(0) # reset ui
            
    def OnExport(self):
        exportDAT = self._ownerComp.par.Exporttodat.eval()
        if type(exportDAT) != tableDAT:
            debug('export target must be a table dat')
            return
        exportDAT.clear()
        for o in self._navPoints:
            exportDAT.appendRow(o)
        pass

    def OnChangelog(self):
        self._changelogOp.openViewer()

    def OnHelp(self):
        self._helpOp.openViewer()

    # go to selected nav point
    def _goTo(self, index: int):
        goToOp = self._navPoints[index]
        # We need to find under whicn path this operator is
        # so that we first can navigate to there and then focus this op
        # otherwise won't do anything if we're currently in a different "folder"
        # in the project's hierarchy
        parentToNavigateTo = goToOp.parent()
        self._mainPane.owner = parentToNavigateTo
        self._mainPane.home(zoom=True, op=goToOp)
        self._updateCurrentText()

    # update the ui that tells us at which nav point we are
    # and how many are there in total
    def _updateCurrentText(self):
        if(len(self._navPoints) == 0):
            self._currentText.val = 'no navigation points'
        else:
            self._currentText.val = f'{self._currentPoint + 1}/{len(self._navPoints)}'


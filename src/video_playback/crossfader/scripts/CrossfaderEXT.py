class CrossfaderEXT:
    def __init__(self, ownerComp: baseCOMP):
        self._ownerComp = ownerComp
        self._crossfadeTriggerOp = op('crossfade_trigger')
        self._crossfadeCurrentDeckOp = op('crossfade_current_deck')

    def OnClipLaunch(self, clipIndex: int):
        # prepare clip and start playback
        clipToPlay = self._getClipToPlay(clipIndex)
        clipToPlay.par.cuepulse.pulse()
        clipToPlay.par.play.val = True
        # put it in the right deck
        freeDeck = self._getFreeDeck()
        freeDeck.par.top = clipToPlay
        # trigger the crossfade
        self._crossfadeTriggerOp.click()

    def OnCrossfadeEnd(self, index: int):
        if(index == 0):
            clip = self._getPlayingClip(1)
            otherClip = self._getPlayingClip(0)
            # need this check in case we have the same clip in both decks
            if(clip != otherClip):
                clip.par.play.val = False
        if(index == 1):
            clip = self._getPlayingClip(0)
            otherClip = self._getPlayingClip(1)
            # need this check in case we have the same clip in both decks
            if(clip != otherClip):
                clip.par.play.val = False
        return

    def _getClipToPlay(self, index: int) -> moviefileinTOP:
        return op(f'moviefilein{index}')

    def _getPlayingClip(self, index: int) -> moviefileinTOP:
        deckA = opex('deck_a').asType(selectTOP)
        deckB = opex('deck_b').asType(selectTOP)
        if(index == 0):
            # eval will return it as an operator and not a plain text
            return deckA.par.top.eval()
        else:
            # eval will return it as an operator and not a plain text
            return deckB.par.top.eval()

    def _getFreeDeck(self):
        deckA = op('deck_a')
        deckB = op('deck_b')

        currentCrossfaderPosition: int = int(self._crossfadeCurrentDeckOp[0][0])
        if(currentCrossfaderPosition == 0):
            return deckB
        else:
            return deckA


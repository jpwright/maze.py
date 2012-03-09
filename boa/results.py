#Boa:Dialog:Results

import wx

def create(parent):
    return Results(parent)

[wxID_RESULTS, wxID_RESULTSRESULTSBOX, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Results(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_RESULTS, name='Results', parent=prnt,
              pos=wx.Point(282, 232), size=wx.Size(400, 250),
              style=wx.DEFAULT_DIALOG_STYLE, title='Results')
        self.SetClientSize(wx.Size(392, 216))

        self.resultsBox = wx.TextCtrl(id=wxID_RESULTSRESULTSBOX,
              name='resultsBox', parent=self, pos=wx.Point(56, 16),
              size=wx.Size(304, 160), style=0, value='Results:')

    def __init__(self, parent):
        self._init_ctrls(parent)

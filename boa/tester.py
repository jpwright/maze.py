#Boa:Frame:Frame1

import wx
import wx.lib.buttons

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1GENBUTTON1, wxID_FRAME1PANEL1, 
] = [wx.NewId() for _init_ctrls in range(3)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(282, 232), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(392, 216))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(64, 56), size=wx.Size(200, 100),
              style=wx.TAB_TRAVERSAL)

        self.genButton1 = wx.lib.buttons.GenButton(id=wxID_FRAME1GENBUTTON1,
              label='genButton1', name='genButton1', parent=self.panel1,
              pos=wx.Point(64, 56), size=wx.Size(76, 25), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

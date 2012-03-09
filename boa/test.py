#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1SPINCTRL1, 
] = [wx.NewId() for _init_ctrls in range(3)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(209, 170), size=wx.Size(400, 250),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(392, 216))

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label='button1',
              name='button1', parent=self, pos=wx.Point(128, 72),
              size=wx.Size(75, 23), style=0)

        self.spinCtrl1 = wx.SpinCtrl(id=wxID_FRAME1SPINCTRL1, initial=0,
              max=100, min=0, name='spinCtrl1', parent=self, pos=wx.Point(304,
              72), size=wx.Size(118, 21), style=wx.SP_ARROW_KEYS)

    def __init__(self, parent):
        self._init_ctrls(parent)

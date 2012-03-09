#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import maze_ui_main

modules ={u'maze': [0, '', u'../maze.py'],
 u'maze_ui_main': [1, 'Main frame of Application', u'maze_ui_main'],
 u'results': [0, '', u'results.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = maze_ui_main.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()

import wx
import requests
import webbrowser
import os

Project_ = 'Dcard Helper API 版'
url_list = []
tit_list = []

title_howbig = 6
context_howbig = 4.5
title_howlong = 37
context_howlong = 45

class HelloFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=Project_,
                           pos=wx.DefaultPosition, size=wx.Size(1200, 768))

        self.pnl = wx.ScrolledWindow(self, -1)

        st = wx.StaticText(self.pnl, label="Dcard備份搜尋:", pos=(250, 15))
        st2 = wx.StaticText(self.pnl, label="文章搜尋:", pos=(295, 55))

        font = st.GetFont()
        font.PointSize += 3
        font = font.Bold()
        st.SetFont(font)
        st2.SetFont(font)

        self.textCtrl1 = wx.TextCtrl(self.pnl, wx.ID_ANY, wx.EmptyString,
                                     wx.Point(375, 50), wx.Size(290, 30), 0)
        self.button1 = wx.Button(self.pnl, wx.ID_ANY, "Go",
                                 wx.Point(750, 55), wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.OnClickTop, self.button1)

        self.st3 = wx.StaticText(self.pnl, label="", pos=(295, 105))
        self.CreateStatusBar()
        self.SetStatusText(Project_)

    def OnClickTop(self, event):
        get_text = self.textCtrl1.GetValue()
        if not get_text:
            box = wx.MessageDialog(None, '請輸入文字', '訊息', wx.OK)
            answer = box.ShowModal()
            box.Destroy()
            return

        self.st3.Destroy()
        if len(tit_list):
            for i in range(1, len(tit_list)):
                self.butt[i].Destroy()
                self.butt2[i].Destroy()
                self.arti[i].Destroy()
                self.arti2[i].Destroy()
            self.pnl.SetScrollbars(0, 50, 0, -1)

        api_url = f"https://www.dcard.tw/service/api/v2/search/posts?query={get_text}&limit=20"
        res = requests.get(api_url)
        data = res.json()

        self.butt = {}
        self.butt2 = {}
        self.arti = {}
        self.arti2 = {}

        tit_list.clear()
        tit_list.append('x')
        url_list.clear()
        url_list.append('x')
        wText_list = ['x']
        wConText_list = ['x']

        for post in data:
            title = post['title']
            url = f"https://www.dcard.tw/f/{post['forumAlias']}/p/{post['id']}"
            excerpt = post['excerpt']
            created_at = post['createdAt'][:10]

            tit_list.append(title)
            url_list.append(url)
            wText_list.append(f"[{created_at}] {title[:title_howlong]}...")
            wConText_list.append(f"      發布時間: {created_at}\n      {excerpt[:context_howlong]}...")

        k1 = len(tit_list)
        self.st3 = wx.StaticText(self.pnl, label="共找到" + str(k1 - 1) + '篇文章.', pos=(295, 105))
        font = self.st3.GetFont()
        font.PointSize += 3
        font = font.Bold()
        self.st3.SetFont(font)
        if k1 - 1 == 0:
            return

        heigh = 130
        for i in range(1, len(tit_list)):
            self.butt[i] = wx.Button(self.pnl, i, "Go", pos=(940, 18 + i * heigh))
            self.Bind(wx.EVT_BUTTON, self.GoBrower, self.butt[i])
            nid = int('77' + str(i))
            self.butt2[i] = wx.Button(self.pnl, nid, "網頁備份", pos=(1040, 18 + i * heigh))
            self.Bind(wx.EVT_BUTTON, self.GoBrower_old, self.butt2[i])

        for i in range(1, len(tit_list)):
            self.arti[i] = wx.StaticText(self.pnl, label=str(i) + ' ' + wText_list[i],
                                         pos=(130, 15 + i * heigh), size=(800, 150),
                                         style=wx.TE_MULTILINE | wx.BORDER_RAISED)
            self.arti2[i] = wx.StaticText(self.pnl, label=wConText_list[i],
                                          pos=(133, 58 + i * heigh))

            font = self.arti[i].GetFont()
            font.PointSize += title_howbig
            font = font.Bold()
            self.arti[i].SetFont(font)

            font = self.arti2[i].GetFont()
            font.PointSize += context_howbig
            self.arti2[i].SetFont(font)

        self.pnl.SetScrollbars(0, 50, 0, 10 + i * 2.5)

    def GoBrower(self, event):
        event_id = event.GetId()
        webbrowser.open(url_list[event_id])

    def GoBrower_old(self, event):
        event_id = str(event.GetId())
        event_id = int(event_id.replace('77', ''))
        webbrowser.open('http://webcache.googleusercontent.com/search?q=cache:' + url_list[event_id])

if __name__ == '__main__':
    app = wx.App()
    frm = HelloFrame(None)
    frm.Show()
    app.MainLoop()

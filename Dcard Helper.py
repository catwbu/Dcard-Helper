
import wx,cloudscraper,webbrowser
import requests
from bs4 import BeautifulSoup
import os
import sys
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(sys._MEIPASS, 'cacert.pem')
'''
    For final python project
        ~Dcard Helper
'''
#define
Project_ = 'Dcard Helper Beta 1.1'
url_list = []
tit_list = []

title_howbig = 6
context_howbig = 4.5

title_howlong = 37
context_howlong = 45



class HelloFrame(wx.Frame):

    def __init__(self,parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = Project_,
        pos = wx.DefaultPosition, size = wx.Size( 1200,768 ))


        self.pnl = wx.ScrolledWindow(self, -1)
        # 文字方塊


        st=wx.StaticText(self.pnl, label="Dcard備份搜尋:",pos=(250,15),size=(-1,-1))
        st2=wx.StaticText(self.pnl, label="文章搜尋:",pos=(295,55),size=(-1,-1))


        font = st.GetFont()
        font.PointSize += 3
        font = font.Bold()
        st.SetFont(font)
        st2.SetFont(font)


        self.textCtrl2 = wx.TextCtrl( self.pnl, wx.ID_ANY, wx.EmptyString,
        wx.Point(375, 10), wx.Size(350, 30), 0 )

        self.button2 = wx.Button(self.pnl,wx.ID_ANY,"Go",
        wx.Point(750, 15),
        wx.DefaultSize,
        0)
        self.Bind(wx.EVT_BUTTON,  self.OnClickTop2, self.button2)

        self.textCtrl1 = wx.TextCtrl( self.pnl, wx.ID_ANY, wx.EmptyString,
        wx.Point(375, 50), wx.Size(290, 30), 0 )
        #Sizer1.Add( textCtrl1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.button1 = wx.Button(self.pnl,wx.ID_ANY,"Go",
        wx.Point(750, 55),
        wx.DefaultSize,
        0)
        self.Bind(wx.EVT_BUTTON,  self.OnClickTop, self.button1)


        # 套用字型
        self.button1.SetFont(font)
        self.button2.SetFont(font)
        self.st3=wx.StaticText(self.pnl, label="",pos=(295,105),size=(-1,-1))
        # and create a sizer to manage the layout of child widgets
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        #self.pnl.SetSizer(sizer)

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText(Project_)

        # create a menu bar
        #self.makeMenuBar()
    def OnClickTop(self, event):


        get_text = self.textCtrl1.GetValue()
        if not get_text:
            box=wx.MessageDialog(None,'請輸入文字','訊息',wx.OK)
            answer=box.ShowModal()
            box.Destroy()
            return
        self.st3.Destroy()
        if len(tit_list):

            for i in range(1,len(tit_list)):
                self.butt[i].Destroy()
                self.butt2[i].Destroy()
                self.arti[i].Destroy()
                self.arti2[i].Destroy()
            self.pnl.SetScrollbars(0, 50, 0,-1)




        url = 'https://www.dcard.tw/search/posts?query='+str(get_text)+'&field=title&since=3'
        url2 = 'https://www.dcard.tw/topics/'+str(get_text)+'?latest=true'




        n=0
        while n < 3:
            n+=1
            print('step1')
            r = cloudscraper.create_scraper().get(url).text
            soup = BeautifulSoup(r,"html.parser")
            print(url)
            sel = soup.select("h2") #標題
            sel2 = soup.select("h2 a") #網址
            sel3 = soup.select("article") #資訊
            if sel: break

        n=0
        while n < 3:
            n+=1
            print('step2')
            rr = cloudscraper.create_scraper().get(url2).text
            soupp = BeautifulSoup(rr,"html.parser")
            print(url2)

            sell = soupp.select("h2") #標題
            sell2 = soupp.select("h2 a") #網址
            sell3 = soupp.select("article") #資訊
            if sell: break


        self.butt  = {}
        self.butt2  = {}
        self.arti = {}
        self.arti2 = {}

        tit_list.clear()
        tit_list.append('x')

        url_list.clear()
        url_list.append('x')

        wText_list = []
        wText_list.append('x')
        wConText_list = []
        wConText_list.append('x')

        if sel:
            for s in sel: #批量標題存入陣列
                no_n = s.text
                no_n = no_n.replace('\n','')
                tit_list.append(no_n)

            for s in sel2: #批量存入陣列
                url_list.append('https://www.dcard.tw'+s['href'])
                #緩存文章資訊
                timel=[]
            for s in sel3:
                timel.append(s.text)


        if sell:
            for s in sell:
                no_n = s.text
                no_n = no_n.replace('\n','')
                tit_list.append(no_n)


            for s in sell2: #批量存入陣列
                url_list.append('https://www.dcard.tw'+s['href'])

             #緩存文章資訊

            for s in sell3:
                timel.append(s.text)

        k1=len(tit_list)
        self.st3=wx.StaticText(self.pnl, label="共找到"+str(k1-1)+'篇文章.',pos=(295,105),size=(-1,-1))
        font = self.st3.GetFont()
        font.PointSize += 3
        font = font.Bold()
        self.st3.SetFont(font)
        if k1-1 == 0: return

        i=1

        for ch in timel:

            ch = ch.replace('\n','')
            #print(i,ch,'\n',tit_list[i],url_list[i])
            ch_hr =ch[1:int(ch.index(tit_list[i]))]
            c=1
            while not ch_hr:
                ch_hr =ch[0:int(ch.index(tit_list[i],c))]
                c+=1

            no_ = ch[:-4]
            context = no_[len(ch_hr)+len(tit_list[i])+1:len(ch_hr)+len(tit_list[i])+context_howlong]+'...'


            #print('n'+ch_hr)
            if '才剛發布' in ch_hr:
                str2 = '才剛發布'
                #向後包多少位
                l=4
                #向前包多少位
                h=0
                #矯正回歸的最大限度
                max=0

            if ' 分鐘前' in ch_hr:
                str2 = ' 分鐘前'
                l=4
                h=1
                max=1
            if ' 小時前' in ch_hr:
                str2 = ' 小時前'
                l=4
                h=1
                max=1
            if ' 天前' in ch_hr:
                str2 = ' 天前'
                l=3
                h=1
                max=1
            if '月' in ch_hr and '日' in ch_hr:
                str2='日'
                l=1
                h=6
                max=2
            if '年' in ch_hr and  '月' in ch_hr:
                str2='日'
                l=1
                h=11
                max=4


            inpos = int(ch_hr.index(str2))
            foru = ch_hr[0:int(inpos-h)]
            hr = ch_hr[inpos-h:inpos+l]

            #矯正回歸
            c=1
            while any(chr.isdigit() for chr in foru):
                if c > max:
                    break


                if 'COVID-19' in foru:
                    foru = ch_hr[0:8]
                    hr = ch_hr[8:inpos+l]
                    break
                if '坂道 46' in foru:
                    foru = ch_hr[0:5]
                    hr = ch_hr[5:inpos+l]
                    break

                if '菱格世代 DD52' in foru:
                    foru = ch_hr[0:9]
                    hr = ch_hr[9:inpos+l]
                    break

                if 'GOT7' in foru:
                    foru = ch_hr[0:4]
                    hr = ch_hr[4:inpos+l]
                    break

                if not foru[-1].isdigit():break
                foru = ch_hr[0:int(inpos-(h+c))]
                hr = ch_hr[inpos-(h+c):inpos+l]
                print(c)
                c+=1


            if len(tit_list[i])+len(foru) > title_howlong:
                tit_list[i] = str(tit_list[i][0:title_howlong])+'...'
            title = tit_list[i]
            i +=1
            print (foru,hr)
            wText_list.append('['+str(foru)+']'+str(title))
            wConText_list.append('      '+str(hr)+'\n'+'      '+str(context))
        #按鈕
        heigh=130

        for i in range(1,len(tit_list)):
            self.butt[i]=wx.Button(self.pnl, i, "Go", pos=(940, 18+i*heigh))
            self.Bind(wx.EVT_BUTTON,  self.GoBrower, self.butt[i])
            nid=int('77'+str(i))
            self.butt2[i]=wx.Button(self.pnl, nid, "網頁備份", pos=(1040, 18+i*heigh))
            self.Bind(wx.EVT_BUTTON,  self.GoBrower_old, self.butt2[i])

        #文字
        for i in range(1,len(tit_list)):
            ################################################################

            '''
            ################################################################
            '''
            self.arti[i]=wx.StaticText(self.pnl, label=str(i)+' '+wText_list[i],
            pos=(130,15+i*heigh),size=(800,150),style = wx.TE_MULTILINE|wx.BORDER_RAISED)
            self.arti2[i]=wx.StaticText(self.pnl, label=wConText_list[i],
            pos=(133,58+i*heigh),size=(-1,-1))


            print(str(i),tit_list[i])

            font = self.arti[i].GetFont()
            font.PointSize += title_howbig
            font = font.Bold()
            self.arti[i].SetFont(font)

            font = self.arti2[i].GetFont()
            font.PointSize += context_howbig

            self.arti2[i].SetFont(font)



        self.pnl.SetScrollbars(0, 50, 0, 10+i*2.5)
    def OnClickTop2(self, event):

        get_text = self.textCtrl2.GetValue()
        if 'https' in str(get_text):
            webbrowser.open('http://webcache.googleusercontent.com/search?q=cache:'+get_text)

        elif get_text:

            urll = 'https://www.google.com/search?q='+str(get_text)+'+site%3Adcard.tw'
            print(urll)
            n=0
            while n<3:
                n+=1
                print(n)
                r = cloudscraper.create_scraper().get(urll).text
                soup = BeautifulSoup(r,"html.parser")


                result = soup.select("a")

                for s in result:
                    if 'h3' in str(s):
                        print('sry')

                        uuu=str(s.get('href'))
                        print('sry2')

                        if 'dcard.tw/f/' in uuu:
                            print('sry3')

                            catch = int(uuu.index('http'))
                            if not catch == 0:
                                uuu=uuu[catch:]
                                print('it works')

                            urll='http://webcache.googleusercontent.com/search?q=cache:'+uuu
                            webbrowser.open(urll)
                            return

            box=wx.MessageDialog(None,'Sorry,找不到網頁','訊息',wx.OK)
            answer=box.ShowModal()
            box.Destroy()
            return
        else:
            box=wx.MessageDialog(None,'請輸入文字','訊息',wx.OK)
            answer=box.ShowModal()
            box.Destroy()
            return

    def GoBrower(self, event):
        event_id = event.GetId()
        webbrowser.open(url_list[event_id])

    def GoBrower_old(self, event):
        event_id = str(event.GetId())
        event_id = int(event_id.replace('77',''))
        webbrowser.open('http://webcache.googleusercontent.com/search?q=cache:'+url_list[event_id])
'''
    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)

'''
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None)
    frm.Show()
    app.MainLoop()

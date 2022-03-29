from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton,MDIconButton,MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.toolbar import MDToolbar
from kivy.lang import Builder
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
import mysql.connector as mys
import csv
try:
    mycon = mys.connect(host = 'db4free.net' ,port = 3306, password = 'mharrish7',user ='harrishm')
except:
    pass

connected = 0
try:
    if mycon.is_connected:
        connected = 1
except:
    pass
try:
    mycursor = mycon.cursor()
except:
    pass

try:
    mycursor.execute('use hardata')
except:
    pass


Window.size = (320,600)

colourb = '56/255,40/255,81/255,1'
colourf = '69/255,55/255,86/255,1'

cardt = """
MDCard:
    radius : dp(15)
    orientation : 'vertical'
    size_hint_y : None
    height : dp(120)
    md_bg_color : 69/255,55/255,86/255,1
    
    
"""
cardtp = """
MDCard:
    radius : dp(15)
    orientation : 'vertical'
    size_hint_y : None
    height : dp(80)
    md_bg_color : 69/255,55/255,86/255,1
    
    
"""

labelt = """
MDLabel:
    text : ''
    font_style : 'H6'
    halign : 'center'
"""


textt = """
MDTextField:
    size_hint_x : (0.9)
    size_hint_y : None
    height : dp(120)
    md_bg_color : 100/255,70/255,110/255,1

"""
gridt = """

MDGridLayout:
    cols : 1
    size_hint_y : None
    height : self.minimum_height
    spacing : dp(20)
    padding : [15,15,15,35]
    
"""
class Poll(MDScreen):
    pass
class Home(MDScreen):
    pass

class POLL(MDApp):
    def retry(self,arg):
        print('retry')
    def pollrecord(self,arg):
        l = ''
        for i in range(0,len(self.Input)):
            if i == (len(self.Input) - 1):
                l = l + "'" + self.Input[i].text + "'"
            else:
                l = l + "'" + self.Input[i].text + "'" + ","
        print('insert into ' + self.tables[self.table] + ' values(' + l + ')')
        self.mycursor.execute('insert into ' + self.tables[self.table] + ' values(' + l + ')')
        self.mycon.commit()
        file = open(str(self.tables[self.table]) + '.csv' , mode = 'w')
        mywriter = csv.writer(file,delimiter = ',')
        self.mycursor.execute('select * from ' + str(self.tables[self.table]))
        for row in self.mycursor:
            if row != []:
                mywriter.writerow(row)
        
        
            
        
            
        
    def backp(self):
        self.sm.current = 'home'
        self.sm.transition.direction = 'right'
    def press(self,arg):
        self.table = 0
        for i in range(0,len(self.L)):
            if self.L[i] == arg:
                self.table = i
                break
        self.sm.current = 'poll'
        self.sm.transition.direction = 'left'
        try:
            self.boxp.remove_widget(self.Scrollp)
        except:
            pass
        self.qfix(self.table)
        
        
        
            
                

    def build(self):
        global mycursor,cardt,textt,labelt,cardtp,gridt,mycon,connected
        self.connected = connected
        try:
            self.mycon = mycon
        except:
            pass
        self.table = 0
        self.gridt = gridt
        self.cardtp = cardtp
        self.cardt = cardt
        self.textt = textt
        self.labelt = labelt
        try:
            self.mycursor = mycursor
        except:
            pass
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette ='DeepPurple'
        self.sm = ScreenManager()
        home = Home(name = 'home')
        home.md_bg_color = 56/255,40/255,81/255,1
        self.sm.add_widget(home)
        poll = Poll(name = 'poll')
        poll.md_bg_color = 56/255,40/255,81/255,1
        self.sm.add_widget(poll)


        box = MDBoxLayout(orientation = 'vertical')
        tool = MDToolbar(title = 'HOME',pos_hint = {'top' : 1})
        tool.elevation = 10
        tool.md_bg_color = 100/255,70/255,110/255,1
        self.L = []
        self.tables = []
        box.add_widget(tool)
        retry = 0
        def cardfix(arg = ''):
            if self.connected == 1:
                self.scroll = ScrollView()
                self.scroll.do_x_scroll = False

                self.grid = Builder.load_string(self.gridt)
                self.mycursor.execute('show tables')

                for row in self.mycursor:
                    
                    top = str(row[0])
                    top1 = top[12:]
                    top2 = top1[:-2]
                    self.tables = self.tables + [top2]
                    card1  = Builder.load_string(cardt)
                    lab1 = MDLabel(text= top2,font_style= 'H6',halign = 'center')
                    but1 = MDRaisedButton(on_press = self.press,text='GO',font_style= 'H6',pos_hint = {'center_x' : 0.5,'center_y' : 0.5})
                    but1.md_bg_color = 100/255,70/255,110/255,1
                    self.L.append(but1)
                    card1.add_widget(lab1)
                    card1.add_widget(but1)
                

                    self.grid.add_widget(card1)
                self.scroll.add_widget(self.grid)
                
                box.add_widget(self.scroll)
            else:
                
                label1 = MDLabel(text = 'NO NETWORK ACCESS' , font_style = 'H6')
                label1.halign = 'center'
                label2 = MDLabel(text = 'PLEASE REOPEN APP AFTER CONNECTING TO NETWORK' , font_style = 'Subtitle1')
                label2.halign = 'center'
                box.add_widget(label1)
        
                box.add_widget(label2)
                
                
        
        
        
        
        cardfix()
        
            
        
        home.add_widget(box)

        toolp = MDToolbar(title = 'POLL',pos_hint = {'top' : 1})
        toolp.left_action_items = [['arrow-left', lambda x: self.backp()]]
        toolp.elevation = 10
        toolp.md_bg_color = 100/255,70/255,110/255,1
        self.boxp = MDBoxLayout(orientation = 'vertical')
        self.Input = []
        #poll
        def qfix(table):
            self.Input = []
            self.mycursor.execute('desc {0}'.format(self.tables[table]))
            self.Scrollp = ScrollView()
            self.Scrollp.do_x_scroll = False
            gridp = Builder.load_string(self.gridt)
            for row in self.mycursor:
                cardp = Builder.load_string(self.cardtp)
                labelp = Builder.load_string(self.labelt)
                labelp.text = row[0]
                cardp.add_widget(labelp)
                inputp = Builder.load_string(self.textt)
                self.Input = self.Input + [inputp]
                gridp.add_widget(cardp)
                gridp.add_widget(inputp)
                
            
            butp1 = MDRaisedButton(text = 'SUBMIT',on_press = self.pollrecord)
            butp1.md_bg_color = 100/255,70/255,110/255,1
            gridp.add_widget(butp1)
            self.Scrollp.add_widget(gridp)
            
            self.boxp.add_widget(self.Scrollp)
        self.boxp.add_widget(toolp)        
        self.qfix = qfix

        poll.add_widget(self.boxp)
        
            

        return self.sm


        

POLL().run()





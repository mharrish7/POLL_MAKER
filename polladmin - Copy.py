from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton,MDFloatingActionButton,MDIconButton,MDRaisedButton
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
from kivymd.uix.dialog import MDDialog


connected = 0




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
    size_hint_x : 0.9
    radius : dp(15)
    orientation : 'vertical'
    size_hint_y : None
    height : dp(90)
    md_bg_color : 69/255,55/255,86/255,1
    text : ''
    MDLabel:
        size_hint_x : 0.9
        text : root.text
        font_style : 'Subtitle1'
        halign : 'center'
        pos_hint : {'center_x' : 0.5,'center_y' : 0.4}
"""


gridt = """

MDGridLayout:
    cols : 1
    size_hint_y : None
    height : self.minimum_height
    spacing : dp(20)
    padding : [15,15,15,35]
    
"""

Window.size = (320,600)

class Adds(MDScreen):
    pass
class Home(MDScreen):
    pass
class Result(MDScreen):
    pass
class POLLADMIN(MDApp):
    def deletepoll(self,arg):
        try:
            self.mycursor.execute('drop table ' + self.tables[self.table])
            self.dia.text = 'DELETED SUCCESSFULLY'
            self.dia.open()
        except:
            self.dia.text = 'FAILED DUE TO ERROR'
            self.dia.open()
    def updatehome(self):
        try:
            self.box.remove_widget(self.Scroll)    
            self.Scroll = ScrollView()
            self.Scroll.do_x_scroll = False
            grid = Builder.load_string(self.gridt)
            self.mycursor.execute('show tables')
            self.L = []

            for row in self.mycursor:
                print(row)
                top = str(row[0])
                top1 = top[12:]
                top2 = top1[:-2]
                self.tables = self.tables + [top2]
                card1  = Builder.load_string(cardt)
                lab1 = MDLabel(text= top2,font_style= 'H6',halign = 'center')
                but1 = MDRaisedButton(on_press = self.read,text='SEE RESULT',font_style= 'H6',pos_hint = {'center_x' : 0.5,'center_y' : 0.5})
                but1.md_bg_color = 100/255,70/255,110/255,1
                self.L.append(but1)
                card1.add_widget(lab1)
                card1.add_widget(but1)
                grid.add_widget(card1)



            self.Scroll.add_widget(grid)
            self.box.add_widget(self.Scroll)
        except:
            pass
    def createpoll(self,arg):
        if self.text1.text == '' or self.text1.text == ' ':
            self.text1.text = ''
        else:
            
            self.ls = self.text1.text + "("
            self.lsh = self.text1.text + ":"
            self.labela.text = self.lsh
            self.text1.text = ''
        
    def addq(self,arg):
        if self.text2.text == '' or self.text2.text == ' ':
            self.text2.text =''
        else:
            self.lsh = self.lsh + self.text2.text + ","
            self.labela.text = self.lsh
            self.ls = self.ls  + self.text2.text + "  " + "varchar(50)"+ ","
            self.text2.text =''
        
    def scpoll(self,arg):
        if self.ls == '' or self.ls == ' ':
            pass
        else:
            print('create table ' + self.ls[:-1] + ')')
            try:
                self.mycursor.execute('create table ' + self.ls[:-1] + ')')
                self.mycon.commit()
                self.dia.text = 'CREATED SUCCESSFULLY'
                self.dia.open()
            except:
                self.dia.text = 'FAILED DUE TO AN ERROR'
                self.dia.open()

     
    def addf(self):
        
        self.sm.current = 'adds'
        self.sm.transition.direction = 'left'
        card1 = Builder.load_string(self.cardtp)
        card1.text = 'ENTER POLL NAME'
        card1.pos_hint = {'center_x' : 0.5,'center_y' : 0.7}
        
        but1 = MDRaisedButton(pos_hint = {'center_x' : 0.5,'center_y' : 0.5},text = 'CREATE',on_press = self.createpoll)
        card1.add_widget(but1)
        self.adds.add_widget(card1)

        card2 = Builder.load_string(self.cardtp)
        card2.text = 'ADD Questions'
        card2.pos_hint = {'center_x' : 0.5,'center_y' : 0.4}
        
        but2 = MDRaisedButton(pos_hint = {'center_x' : 0.5,'center_y' : 0.5},text = 'ADD',on_press = self.addq)
        card2.add_widget(but2)
        self.adds.add_widget(card2)
        buts = MDRaisedButton(pos_hint = {'center_x' : 0.5,'center_y' : 0.1},text = 'SUBMIT',on_press = self.scpoll)
        self.adds.add_widget(buts)
        
        
        
    def pressok(self,arg):
        self.dia.dismiss()
    def download(self,arg):
        la = []
        try:
            file = open(self.tables[self.table] + '.csv',mode = 'w')
            mywriter = csv.writer(file,delimiter = ',')
            self.mycursor.execute('desc ' + self.tables[self.table])
            for row in self.mycursor:
                la.append(row[0])
            self.mycursor.execute('select * from ' + self.tables[self.table])
            mywriter.writerow(la)
            for row in self.mycursor:
                mywriter.writerow(row)
            file.close()
            self.dia.text = 'FILE SAVED SUCCESSFULLY'
            self.dia.open()
        except:
            self.dia.text = 'FAILED TO DUE TO AN ERROR'
            self.dia.open()
        

    def read(self,arg):
        self.table = 0
        for i in range(0,len(self.L)):
            if self.L[i] == arg:
                self.table = i
                break
        self.sm.current = 'result'
        self.sm.transition.direction = 'left'
        try:
            self.boxr.remove_widget(self.Scrollr)
        except:
            pass
        self.rfix(self.table)
    def rfix(self,table):
        l = ''
        self.mycursor.execute('select COUNT(*) from '+ self.tables[self.table])
        for row in self.mycursor:
            l = row[0]
        self.card1r.text = 'NO OF ENTRIES : ' + str(l)
        card2r = Builder.load_string(self.cardtp)
        card2r.text  = "Will be saved in the exe folder (desktop only)"
        card2r.pos_hint = {'center_x' : 0.5,'center_y' : 0.5}
        but1r = MDRaisedButton(text = 'SAVE RESULT' , on_press = self.download,pos_hint = {'center_x' : 0.5,'center_y' : 0.5} )
        card2r.add_widget(but1r)
        self.result.add_widget(card2r)
        
    def backr(self):
        self.sm.current = 'home'
        self.sm.transition.direction = 'right'
        self.updatehome()
        
    def build(self):
        global connected,cardtp,gridt
        self.gridt = gridt
        self.cardtp = cardtp
        
        self.connected = connected
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette ='DeepPurple'
        self.sm = ScreenManager()
        home = Home(name = 'home')
        home.md_bg_color = 56/255,40/255,81/255,1

        self.sm.add_widget(home)
        self.result = Result(name = 'result')
        self.result.md_bg_color = 56/255,40/255,81/255,1
        self.sm.add_widget(self.result)
        self.adds = Adds(name = 'adds')
        self.adds.md_bg_color = 56/255,40/255,81/255,1

        self.sm.add_widget(self.adds)


        

        self.box = MDBoxLayout(orientation = 'vertical')
        tool = MDToolbar(title = 'HOME',pos_hint = {'top' : 1})
        tool.right_action_items = [['plus', lambda x: self.addf()]]
        tool.elevation = 10
        tool.md_bg_color = 100/255,70/255,110/255,1
        self.box.add_widget(tool)
        self.L = []
        self.Lr = []
        self.tables = []
        self.table = 0
       

        def cardfix(arg = ''):

            try:
                box.remove_widget(self.Lr[0])
                box.remove_widget(self.Lr[1])
                box.remove_widget(self.Lr[2])
            except:
                pass 

            try:
                if self.connected == 0:
                    self.mycon = mys.connect(host = 'db4free.net' ,port = 3306, password = 'Pass',user ='User')
            except:
                pass
            try:
                if self.connected == 0:
                    if self.mycon.is_connected:
                        self.connected = 1
            except:
                pass
            try:
                self.mycursor = self.mycon.cursor()
            except:
                pass

            try:
                self.mycursor.execute('use hardata')
            except:
                pass
            
            
            if self.connected == 1:
                self.Scroll = ScrollView()
                self.Scroll.do_x_scroll = False
                grid = Builder.load_string(self.gridt)
                self.mycursor.execute('show tables')

                for row in self.mycursor:
                    print(row)
                    top = str(row[0])
                    top1 = top[12:]
                    top2 = top1[:-2]
                    self.tables = self.tables + [top2]
                    card1  = Builder.load_string(cardt)
                    lab1 = MDLabel(text= top2,font_style= 'H6',halign = 'center')
                    but1 = MDRaisedButton(on_press = self.read,text='SEE RESULT',font_style= 'H6',pos_hint = {'center_x' : 0.5,'center_y' : 0.5})
                    but1.md_bg_color = 100/255,70/255,110/255,1
                    self.L.append(but1)
                    card1.add_widget(lab1)
                    card1.add_widget(but1)
                    grid.add_widget(card1)



                self.Scroll.add_widget(grid)
                self.box.add_widget(self.Scroll)
                

            else:
                label1 = MDLabel(text = 'NO NETWORK ACCESS' , font_style = 'H6')
                label1.halign = 'center'
                label2 = MDLabel(text = 'PLEASE REOPEN APP AFTER CONNECTING TO NETWORK' , font_style = 'Subtitle1')
                label2.halign = 'center'
                butr = MDRaisedButton(text = 'RETRY',on_press = cardfix,pos_hint = {'center_x' : 0.5,'center_y' : 0.5})
                self.Lr = [label1,label2,butr]
                self.box.add_widget(label1)
                self.box.add_widget(butr)
                self.box.add_widget(label2)
        self.dia = MDDialog(text = '' , buttons = [MDFlatButton(text = 'OK',on_press = self.pressok)])

        cardfix()
        
        home.add_widget(self.box)



        #result
        self.createp =  ''
        self.addpq = ''
        toolr = MDToolbar(title = 'RESULT',pos_hint = {'top' : 1})
        toolr.left_action_items = [['arrow-left', lambda x : self.backr()]]
        toolr.elevation = 10
        toolr.md_bg_color = 100/255,70/255,110/255,1
        self.card1r = Builder.load_string(self.cardtp)
        self.card1r.pos_hint = {'center_x'  :0.5 , 'center_y' : 0.8}
        butd = MDRaisedButton(text = 'DELETE POLL',pos_hint = {'center_x'  :0.5 , 'center_y' : 0.2},on_press = self.deletepoll)
        self.result.add_widget(butd)
        
        
        self.result.add_widget(toolr)
        self.result.add_widget(self.card1r)


        #adds
        toola = MDToolbar(title = 'CREATE POLL',pos_hint = {'top' : 1})
        toola.left_action_items = [['arrow-left', lambda x : self.backr()]]
        toola.elevation = 10
        toola.md_bg_color = 100/255,70/255,110/255,1
        self.ls = ''
        self.lsh =''
        self.labela = MDLabel(font_style = 'Caption',text = 'ADD ITEMS',pos_hint = {'center_x' : 0.5,'center_y' : 0.2})
        self.text1 = MDTextField(size_hint_x  = 0.9,pos_hint = {'center_x'  :0.5 , 'center_y' : 0.6})
        self.text1.hint_text = 'POLLNAME'
        self.text2 = MDTextField(size_hint_x  = 0.9,pos_hint = {'center_x'  :0.5 , 'center_y' : 0.3})
        self.text2.hint_text = 'QUESTION'
        self.labela.halign = 'center'
        self.adds.add_widget(self.text1)
        self.adds.add_widget(self.text2)
       
        self.adds.add_widget(toola)
        self.adds.add_widget(self.labela)
        

        return self.sm


POLLADMIN().run()              

        
        
        










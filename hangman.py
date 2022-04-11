from tkinter import *
from time import time
from tkinter import messagebox
import tkinter.font as tkFont
import random
class Hangman:
    def __init__(self):
        self.root = Tk()
        self.root.title('Hangman')
        self.root.geometry('700x500')
        #self.root.configure(bg='#006c00')
        
        self.word_bank=['spring', 'stage', 'possessive', 'punish', 'gleaming', 'natural', 'advise', 'clean', 'conscious', 'share', 'infamous', 'haircut', 'sail', 'fuzzy', 'force', 'private', 'sticks', 'thought', 'voyage', 'sting', 'fling', 'output', 'delicate', 'wealth', 'audit', 'permit', 'typeset', 'become', 'sally', 'greasy', 'jellyfish', 'describe', 'distance', 'dance', 'honorable', 'library', 'cowardly', 'bawdy', 'invention', 'authority', 'crayon', 'observation', 'ordinary', 'spiders', 'mother', 'extend', 'tangible', 'sound', 'unsuitable', 'awake', 'quickest', 'course', 'detect', 'arrogant', 'fierce', 'obscene', 'beautify', 'promise', 'brain', 'continue', 'tremble']
        #self.word_bank=['spring']
        self.word_done=[]
        
        if len(self.word_bank)!=0:
            self.word=random.choice(self.word_bank).upper()
            self.word_done.append(self.word)
            self.word_bank.remove(self.word.lower())
        else:
            self.word_bank=self.word_done
            del self.word_done[:]
        
        self.word_len=len(self.word)
        self.letter=list(self.word)
        self.chances_left=7
        self.chances_display()
        self.letters_display()
        self.alpha_buttons()
        self.word_guess()
        
        messagebox.showinfo('Start', 'Game is gonna Start!')
        self.paused = False
        self.seconds = 120
        self.timer()
        self.root.mainloop()
        
    def chances_display(self):
        self.fontStyle = tkFont.Font(family="Comic Sans MS", size=12)
        self.chances_label = Label(self.root,text='Total Chances : 7',font=self.fontStyle,relief='groove',width=20)
        self.chances_label.place(x=10,y=5)
        self.chancesLeft_display = Label(self.root,text='Chances Left : '+str(self.chances_left),font=self.fontStyle,relief='groove',width=20)
        self.chancesLeft_display.place(x=280,y=5)
        self.timer_display = Label(self.root,font=self.fontStyle,fg='green',relief='flat')
        self.timer_display.place(x=550,y=5)
        
    def letters_display(self):
        self.letters_frame = LabelFrame(self.root,text='Letters',padx=5, pady=5,width=680,height=100,font=("Comic Sans MS", 12))
        self.letters_frame.place(x=10,y=40)
        self.letters=[]
        del self.letters[:]
        
        self.diff=9-self.word_len
        if self.diff<0:
            self.diff=1 
        self.start=int(self.diff/2)
        self.end=int(self.diff/2)+self.word_len
        if self.diff%2==0: 
            for i in range(9):
                if self.word_len==9:
                    self.letters.append(Label(self.letters_frame,text="",relief='sunken',width=2,font=('Comic Sans MS', 20, 'bold')))
                    self.letters[i].place(relx=float(1.05-((9-i)*0.11)),rely=0.5,anchor=CENTER)
                elif i in range(self.start,self.end) and self.diff>0:
                    self.letters.append(Label(self.letters_frame,text="",relief='sunken',width=2,font=('Comic Sans MS', 20, 'bold')))
                    self.letters[i].place(relx=float(1.05-((9-i)*0.11)),rely=0.5,anchor=CENTER)
                else:
                    self.letters.append(Label(self.letters_frame,text="",relief='flat',width=2,font=('Comic Sans MS', 20, 'bold')))
                    self.letters[i].place(relx=float(1.05-((9-i)*0.11)),rely=0.5,anchor=CENTER)
            
        else:
            if self.word_len!=10:
                self.start+=1
            for i in range(10):
                if self.word_len==10:
                    self.letters.append(Label(self.letters_frame,text="",relief='sunken',width=2,font=('Comic Sans MS', 20, 'bold')))
                    self.letters[i].place(relx=float(1.05-((10-i)*0.1)),rely=0.5,anchor=CENTER)
                elif i in range(self.start,self.end+1) :
                    self.letters.append(Label(self.letters_frame,text="",relief='sunken',width=2,font=('Comic Sans MS', 20, 'bold')))
                    self.letters[i].place(relx=float(1.05-((10-i)*0.1)),rely=0.5,anchor=CENTER)
                else:
                    self.letters.append(Label(self.letters_frame,text="",relief='flat',width=2,font=('Comic Sans MS', 20, 'bold')))
                    self.letters[i].place(relx=float(1.05-((10-i)*0.1)),rely=0.5,anchor=CENTER)
    
    def check_letter(self,button,a):
        button.configure(state=DISABLED)
        button.configure(relief='flat')
        self.indices=[i for i in range(self.word_len) if self.letter[i]==a]
        self.raise_letter()
    def check_word(self):
        if self.word!=self.guess_entry.get().upper():
            self.reduce(False)
        else:
            messagebox.showinfo('Win!', 'Congratualtions\nYou Got the Word.')
            self.quit()
    def raise_letter(self):
        if len(self.indices):
            for index in self.indices:
                self.letters[self.start+index].config(relief='raised')
                self.letters[self.start+index].config(text=self.letter[index])
            self.guessed_letter=[self.letters[i]['text'] for i in range(len(self.letters))]
            print(self.guessed_letter)
            guessed="".join(self.guessed_letter).strip()
            word="".join(self.letter).strip()
            if word==guessed:
                messagebox.showinfo('Win!', 'Congratulations\nWord: '+self.word)
                self.quit()
        else:
            self.reduce(True)
            
    def alpha_buttons(self):
        self.alpha_frame = LabelFrame(self.root,text='Alphabets',padx=5, pady=5,width=680,height=200,font=("Comic Sans MS", 12))
        self.alpha_frame.place(x=10,y=150)
        self.alphabets=[]
        del self.alphabets[:]
        for i in range(10):
            self.alphabets.append(Button(self.alpha_frame, text=chr(65+i),command=lambda i=i: self.check_letter(self.alphabets[i],chr(65+i)),width=3,height=1,font=("", 12)))
            self.alphabets[i].place(x=15+i*65,y=5)
        for i in range(10,20):
            self.alphabets.append(Button(self.alpha_frame, text=chr(65+i),command=lambda i=i: self.check_letter(self.alphabets[i],chr(65+i)),width=3,height=1,font=("", 12)))
            self.alphabets[i].place(x=15+(i-10)*65,y=65)
        for i in range(20,26):
            self.alphabets.append(Button(self.alpha_frame, text=chr(65+i),command=lambda i=i: self.check_letter(self.alphabets[i],chr(65+i)),height=1,font=("", 12)))
            self.alphabets[i].place(x=145+(i-20)*65,y=125)
            
    def word_guess(self):
        self.guess_frame = LabelFrame(self.root,text='Guess The Word',padx=5, pady=5,width=680,height=120,font=("Comic Sans MS", 12))
        self.guess_frame.place(x=10,y=360)
        self.guess_entry= Entry(self.guess_frame,font=("Comic Sans MS",16),borderwidth = 2,relief='solid',justify=CENTER)
        self.guess_entry.place(x=200,y=5)
        self.check_button= Button(self.guess_frame, text="Check",command=self.check_word,width=5,height=1,font=("", 12))
        self.check_button.place(x=300,y=50)
    def quit(self):
            self.root.destroy()
            
    def reduce(self,chances):
            if chances:
                self.chances_left=int(self.chances_left)-1
                self.chances_display()
                if self.chances_left==0:
                    self.paused=1
                    self.ans=messagebox.askretrycancel("You are out of chances!", "Do you want to try that again with 3 extra chances and 15 seconds penalty?")
                    if self.ans:
                        self.chances_left+=3
                        self.paused=0
                        self.seconds-=15
                        self.timer()
                    else:
                        messagebox.showinfo("Thank You","Word : "+self.word.capitalize())
                        self.quit()
            else:
                self.paused=1
                messagebox.showinfo('Message', 'Wrong Guess!\nTime penalty : 5 Secs')
                self.paused=0
                self.seconds-=4
                self.timer()
            
    def timer(self):
        if self.paused:
            return
        if self.seconds > 0:
            self.seconds-=1
            mins = self.seconds // 60
            m = str(mins)

            if mins < 10:
                m = '0' + str(mins)
            se = self.seconds - (mins * 60)
            s = str(se)

            if se < 10:
                s = '0' + str(se)
            timestr = "Time Left - {}:{}".format(m,s)
            if self.seconds<30:
                self.timer_display.config(fg='red')
            self.timer_display.config(text=timestr)
            # call this function again in 1,000 milliseconds
            self.timer_display.after(1000, self.timer)
            self.chances_display()
        elif self.seconds == 0:
            messagebox.showinfo('Oops!', 'Time Ran Out.\nWord : '+self.word.capitalize())
            self.quit()
            
Hangman()
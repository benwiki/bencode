from itertools import permutations
from time import time, sleep
#from keyboard import is_pressed
from tkinter import *
from math import sin, cos, pi
pms=permutations

#RENDEZD MÁR EL VALAHOGY KÉRLEK, MERT EZ ÍGY HÁNYÁS!!!!

osszbetu=[]

def wait_for_input():
        while tovabb==False:
                ablak.update()

def betuszerintbont(arr):
        global osszbetu
        new=[]
        ind=0
        for i in range(len(arr)):
                if i==0:
                        new.append([arr[i]])
                        osszbetu.append(arr[i][0])
                        continue
                if arr[i][0]==arr[i-1][0]:
                        new[ind].append([arr[i]])
                else:
                        new.append([arr[i]])
                        osszbetu.append(arr[i][0])
                        ind+=1
        return new
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getwords(s, w, n, a):
        global x_bef, y_bef, tovabb
        for i in range(len(w[n])):
                rajz.coords(wt[n][0], wt[n][1]-a[n]*8, 10+15*n)
                if n==len(w)-1:
                        szo=''.join([w[k][a[k]] for k in range(len(w))])
                        rajz.itemconfig(generated_word, text=szo)
                        if search(mygraph, szo) and not szo in osszes:
                                tovabb=False
                                wait_for_input()
                                osszes.append(szo)
                                rajz.create_text(x_bef+15, y_bef+len(words)+5, text=szo, font="Courier 10")
                                if y_bef<h-30:
                                        y_bef += 15
                                else:
                                        x_bef += len(words)*8+10
                                        y_bef = len(words)*15+20
                else:
                        getwords(s, w, n+1, a)
                if a[n]<len(w[n])-1:
                        a[n]+=1
                else:
                        a[n]=0
                ablak.update()
                        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def graph(arr, layer=0, letters=1, word=0, graphized=[]):
        
        if layer==0:
                graph(arr, layer=1, graphized=graphized)
                return graphized
                
        elif letters<=len(arr[word]) and word<len(arr):
                last_cur_word=cur_word=word
                
                while cur_word<len(arr) and arr[word][:letters-1] == arr[cur_word][:letters-1]:
                        new_index=cur_word
                        
                        cur_let=arr[cur_word][letters-1]
                        if cur_let not in graphized:
                                graphized.append(cur_let)
                        
                        if letters < len(arr[cur_word]):
                                if arr[cur_word-1][:letters]==arr[cur_word][:letters] and cur_word>0:
                                        graphized.append([''])
                                else:
                                        graphized.append([])
                                part=graphized[-1]
                                new_index=graph(arr, layer+1, letters+1, cur_word, part)
                                
                        if new_index==cur_word:
                                cur_word+=1
                        else: cur_word=new_index
                        
                        if layer==1:
                                print(cur_word)
                                loading(rajz, w/2, h/2, last_cur_word/len(arr)*100, cur_word/len(arr)*100)
                                last_cur_word=cur_word
                        
                return cur_word
                
        return word
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
def search(graph, word, letter=0):
        wlen=len(word)
        if letter<wlen and word[letter] in graph:
                list_ind=graph.index(word[letter])+1
                if len(graph)>list_ind:
                        part=graph[list_ind]
                        if isinstance(part, list):
                                return search(part,word,letter+1)
                        elif letter==wlen-1:
                                return True
                        else:
                                return False
                elif letter==wlen-1:
                        return True
                else:
                        return False
        elif '' in graph and letter==wlen:
                return True
        else:
                return False

def color2(a, b):
	arnyalat=255*a/b
	col="#"
	if arnyalat<16:
		col+='0'
	col+=str(hex(int(arnyalat)))[2:]
	col+="0000"
	return col

def loading(rajz, x, y, start, extent, db=400, r=100):
	start=int(db*start/100)
	extent=int(db*extent/100)
	teljesszog=2*pi
	for i in range(start, extent):
		arany=i/(db/2)
		if i<db/2:
			x1=x + cos(arany*teljesszog)*r
			y1=y + sin(arany*teljesszog)*r
			x2=x + cos(arany*teljesszog)*r*(1-arany)
			y2=y + sin(arany*teljesszog)*r*(1-arany)
		else:
			x1, y1=x, y
			x2=x + cos(arany*teljesszog)*r*(2-arany)
			y2=y + sin(arany*teljesszog)*r*(2-arany)
		rajz.create_line(x1, y1, x2, y2, width=5, fill=color2(i, db))
		ablak.update()
                
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

ablak = Tk()
ablak.config(bg='black')

def startfunc(x):
        global start
        if x()!=0:
                start=True

def sub():
        global submitted
        submitted=True

instruction=Label(ablak, fg='white', bg='black')
name=Entry(ablak)
submit=Button(text="submit", command=sub, bg='white', activebackground='white', width=8, height=3)
lightred='#FF7777'
gray='#555555'
lista=Listbox(bg=gray, fg='white', selectforeground=lightred, width=40, height=30)
startbutton=Button(command=lambda: startfunc(lista.size), bg='white', width=10, height=3)

instruction.config(text='Adj meg szavakat!')
instruction.pack()
lista.pack()

name.pack()
name.delete(0, END)
submit['text']='Hozzáad'
submit.pack()
startbutton['text']='INDÍT'
startbutton.pack()

words=[]
submitted=False
start=False
while not start:
        ablak.update()
        if submitted:
                if name.get()!='':
                    lista.insert(END, name.get())
                    words.append(name.get())
                submitted = False
                name.delete(0, END)
lista.delete(0, END)

name.pack_forget()
submit.pack_forget()
lista.pack_forget()
startbutton.pack_forget()
instruction.pack_forget()

instruction.pack(fill="none", expand=True)
instruction.config(text='Please wait!', font="Courier 20")
ablak.geometry("500x500")
ablak.update()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

try:
        f=open('word_database.txt', 'r')
        wordsarr = [word[:-1] for word in f]
        f.close()
        instruction.config(text='Please wait!\nFile read, generating graph...')
except:
        instruction.config(text='Sorry, no file found...')
        while 1:
                ablak.update()

w, h = 250, 250
rajz=Canvas(width=w, height=h, bg='black', highlightcolor='black', highlightbackground='black')
rajz.pack()

ablak.update()
mygraph=graph(wordsarr)
instruction.pack_forget()

w, h = 900, 650
ablak.geometry(str(w)+'x'+str(h+60))
rajz.config(width=w, height=h, bg='white')
rajz.delete(ALL)

def tov():
        global tovabb
        tovabb=True
tovButton = Button(text='Következő', command=tov, height=3, width=20)
tovButton.pack()

r=10
rajz.create_rectangle(w/2-3, 5, w/2+r+2, len(words)*15+5, outline='red', width=2)
word_text=[]
for i in range(len(words)):
    word_text.append([ rajz.create_text(w/2+len(words[i])/2*8,
                                        10+15*i,
                                        text = words[i],
                                        font="Courier 10"),
                       w/2+len(words[i])/2*8 ])
generated_word = rajz.create_text(w/2, len(words)*15+15, fill='red')
                                   
perm=pms([i for i in range(len(words))])
count=1
osszes=[]
x_bef, y_bef = len(words)*8/2+5, len(words)*15+20
for p in perm:
        wds=[words[k] for k in p]
        wt=[word_text[k] for k in p]
        index=[0 for w in words]
        s=[]
        getwords(s, wds, 0, index)
        print (str(count))
        count+=1
        
mainloop()

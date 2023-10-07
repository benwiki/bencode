from itertools import permutations
from time import time, sleep
from datetime import datetime
from tkinter import *
from math import sin, cos, pi
pms=permutations

osszbetu=[]

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
			new[ind].append(arr[i])
		else:
			new.append([arr[i]])
			osszbetu.append(arr[i][0])
			ind+=1
	return new
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getwords(s, w, n, a):
	for i in range(len(w[n])):
		if n==len(w)-1:
			szo=''.join([w[k][a[k]] for k in range(len(w))])
			s.append(szo)
		else:
			getwords(s, w, n+1, a)
		if a[n]<len(w[n])-1:
			a[n]+=1
		else:
			a[n]=0
			
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def hybrid_search(graph, words,word_ind=0, index=None, product=None):
	
	if index is None:
		index=[0 for i in words]
		product=[]
	
	def add_word_inside():
		szo=''.join([words[k][index[k]] for k in range(len(words))])
		if szo not in product:
			product.append(szo)
		
	try:
		cur_word=words[word_ind]
	except:
		if '' in graph and word_ind==len(words):
			add_word_inside()
		return product
			
	ind_ok = lambda: index[word_ind] < len(cur_word)
	cur_let=lambda: cur_word[index[word_ind]]
		
	used=[]
	while ind_ok():
		szo=''.join([words[k][index[k]] for k in range(len(words))])
		while ind_ok() and (cur_let() not in graph or cur_let() in used):
			index[word_ind]+=1
		if ind_ok():
			used.append(cur_let())
			list_ind=graph.index(cur_let())+1
			if len(graph)>list_ind:
				part=graph[list_ind]
				if isinstance(part, list):
					hybrid_search(part, words, word_ind+1, index, product)
				elif word_ind==len(words)-1:
					add_word_inside()
			elif word_ind==len(words)-1:
				add_word_inside()
		if index[word_ind]<len(cur_word)-1:
			index[word_ind]+=1
		else:
			index[word_ind]=0
			break
	return product
			
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def graph(arr, layer=0, letters=1, word=0, graphized=[], arrlen=0):
	
	if layer==0:
		graph(arr, layer=1, graphized=graphized, arrlen=len(arr))
		return graphized
		
	elif letters<=len(arr[word]) and word<len(arr):
		cur_word=word
		
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
				new_index=graph(arr, layer+1, letters+1, cur_word, part, arrlen=arrlen)
			
			if layer==4:
				draw.itemconfig(percentage, text=str(new_index*100//arrlen)+"%")
				loading(w/2, h/2, 300*cur_word//arrlen, 300*new_index//arrlen, 'red')
			if new_index==cur_word:
				cur_word+=1
			else: cur_word=new_index
			
		return cur_word
		
	return word

"""cucc1=['alma', 'alom', 'alpi', 'baci']
cucc1=graph(cucc1)
cucc2=['alkeszbe', 'analóg', 'pipicomb', 'ami']
print(cucc1)
print(hybrid_search(cucc1, cucc2))"""
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
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~
		
def add_word(graph, word, letter=0):
	wlen=len(word)
	if letter<wlen and word[letter] in graph:
		list_ind=graph.index(word[letter])+1
		if len(graph)>list_ind:
			part=graph[list_ind]
			if isinstance(part, list):
				add_word(part,word,letter+1)
			elif letter==wlen-1:
				return True
			else:
				graph=graph[:list_ind]+[[]]+graph[list_ind:]
				add_word(graph[list_ind],word,letter+1)
		elif letter==wlen-1:
			return True
		else:
			graph=graph[:list_ind]+[[]]+graph[list_ind:]
			add_word(graph[list_ind],word,letter+1)
	elif letter==wlen:
		if '' in graph:
			return True
		else:
			graph.append('')
	elif letter<wlen:
		graph.append(word[letter])
		graph.append([])
		add_word(graph[-1],word,letter+1)
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def colorizer(a, b, choice, ground=1):
	arnyalat=255*a/b
	part=''
	if ground:
		g='ff'
		arnyalat=255-arnyalat
	else:
		g='00'
	if arnyalat<16:
		part+='0'
	part+=str(hex(int(arnyalat)))[2:]
	if choice=='red':
		col=part+2*g
	elif choice=='green':
		col=g+part+g
	elif choice=='blue':
		col=2*g+part
	elif choice=='yellow':
		col=2*part+g
	elif choice=='magenta':
		col=part+g+part
	elif choice=='cyan':
		col=g+2*part
	else:
		col=3*part
	return "#"+col
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def loading(x, y, start, extent, color, db=300, r=250):
	#start=int(db*start/100)
	#extent=int(db*extent/100)
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
		draw.create_line(x1, y1, x2, y2, width=30, fill=colorizer(i, db, color, 0), capstyle=ROUND)
		draw.tag_raise(percentage)
		window.update()
	#window.update()
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
		
def start():
	words=wordlist.get(0, END)
	hany=len(words)
	perm=pms([i for i in range(hany)])
	count=1
	from math import factorial
	all=factorial(hany)
	osszes=[]
	
	frame1.grid_forget()
	if not wordlist2.winfo_ismapped():
		draw.config(height=int(h*0.1))
		wordlist2.grid()
		back.grid()
	frame2.grid()
	
	loading_bar=draw.create_line(0, 0, 0, 0, fill=lightred, width=int(h*0.05))
	percentage=draw.create_text(w/2, h*0.05, fill='white', font="Sans 15 bold")
	
	#filename='kigyujtott_'+str(datetime.now())+'.txt'
	
	for p in perm:
		wds=[words[k] for k in p]
		ergebnis=hybrid_search(mygraph, wds)
		draw.coords(loading_bar, 0, h*0.05,  count/all*w, h*0.05)
		draw.itemconfig(percentage, text=str(count*100//all)+"%")
		for word in ergebnis:
			if not search(osszes, word):
				wordlist2.insert(END, word)
				add_word(osszes, word)
				window.update()
		count+=1
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~
		
def settings(new=0):
	frame2.grid_forget()
	wordlist.delete(0, END)
	add.delete(0, END)
	frame1.grid()
	
def base_settings():
	cim1.grid(row=0, columnspan=2)
	space.grid(row=9, columnspan=2)
	add.grid(row=10, columnspan=2)
	entryaddword.grid(row=7, column=1)
	startprogram.grid(row=8, column=1)
	wordlist.grid(row=1, column=0, rowspan=8, padx=0, ipadx=0)
	draw.grid()
	frame2.grid()
		
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
gray="#777777"
lightred="#ff7f7f"

window=Tk()
window.config(bg="black")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()

frame1=Frame(bg="black")
frame2=Frame(bg='black')

draw=Canvas(frame2,width=w, height=h, bg='black', highlightthickness=0)

wordlist=Listbox(frame1, width=20, height=15, bg=gray, fg='white', selectforeground=lightred, highlightthickness=0)

wordlist2=Listbox(frame2, width=30, height=22, bg=gray, fg='white', selectforeground=lightred, highlightthickness=0)

add = Entry(frame1,width=30)

def eaw():
	if add.get()!='':
		wordlist.insert(END, add.get())
		add.delete(0, END)
		
entryaddword=Button(frame1,text="Add word", command=eaw, width=12, height=3)
startprogram=Button(frame1,text="START", command=start, width=12, height=3)
back=Button(frame2, text="Back", command=lambda: settings(1), height=2, width=20)

cim1=Label(frame1,text="Add some words please", font="Sans 15 bold", height=3, bg="black", fg="white")
space=Label(frame1,bg='black')

#@@@@@@@@@@@@@@@@@##@

base_settings()

f=open('word_database.txt', 'r')
draw.create_text(w/2, h/2, text="File is being processed...", fill="white")
window.update()

sorted=[word[:-1] for word in f]
f.close()
draw.create_text(w/2, h/2-50, text="File ready")

draw.delete(ALL)
percentage=draw.create_text(w/2, h/2, fill='white', font="Sans 15 bold")

mygraph=graph(sorted)
draw.delete(ALL)

settings(1)
mainloop()
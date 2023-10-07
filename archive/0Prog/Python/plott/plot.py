import tkinter as tk

class Plot(tk.Tk):
	def ovalcoords(self, x, y, r):
		return (x-r, y-r, x+r, y+r)

	def __init__(self, filename: str, sep=','):
		super().__init__()
		self.fname = filename
		self.sep = sep
		self.w = self.winfo_screenwidth()
		self.h = self.winfo_screenheight()
		self.draw = tk.Canvas(bg='white', width=self.w, height=self.h)
		self.draw.pack()
		x0, y0 = self.w*0.1, self.h*0.9
		xn, yn = self.w*0.9, self.h*0.1
		self.draw.create_line(x0, y0, x0, yn)
		self.draw.create_line(x0, y0, xn, y0)
		with open(self.fname, 'r') as f:
			self.graphdata = f.read().split('\n')
			self.numOfPts = len(self.graphdata)
			self.x1 = x0+(self.w-x0*2)/self.numOfPts
			self.xn_1 = x0+(self.w-x0*2)/self.numOfPts*(self.numOfPts-1)
			
			dom = set()
			for i in range(self.numOfPts):
			    x, y = self.graphdata[i].split(self.sep)
			    x, y = float(x), float(y)
			    
			    dom.add(y)
			    self.graphdata[i]=(x,y)
			self.y1 = y0+(self.h-y0*2)/len(dom)
			self.yn_1 = y0+(self.h-y0*2)/len(dom)*(len(dom)-1)
			
			
			self.xMax = max(self.graphdata, key=lambda pt: pt[0])[0]
			self.yMax = max(self.graphdata, key=lambda pt: pt[1])[1]
			self.xMin = min(self.graphdata, key=lambda pt: pt[0])[0]
			self.yMin = min(self.graphdata, key=lambda pt: pt[1])[1]
			self.draw.create_text(self.x1, y0+(self.h-y0)/2, text=self.xMin)
			self.draw.create_text(self.xn_1,y0+(self.h-y0)/2, text=self.xMax)
			self.draw.create_text(x0/2, self.y1, text=self.yMin)
			self.draw.create_text(x0/2, self.yn_1, text=self.yMax)
			self.plot()
		tk.mainloop()
		
	def plot(self):
		sx, sy = None, None
		for x, y in self.graphdata:
			xcoord = self.x1+x/self.xMax*(self.xn_1-self.x1)
			ycoord = self.y1+y/self.yMax*(self.yn_1-self.y1)
			self.draw.create_oval(self.ovalcoords(xcoord, ycoord, 5), fill='red', outline='')
			if sx is None:
				sx, sy = xcoord, ycoord
			self.draw.create_line(sx, sy, xcoord, ycoord, width=2, fill='red')
			sx, sy = xcoord, ycoord
		
Plot("graph.txt")
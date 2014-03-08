#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import shelve
import csv
import pyglet
from pyglet import image

global items,worlds

'''********************* fonctions Chargement ANCIENNE ****************************************************************'''

def loaditems(n,file):
	global items
	with open(file, 'rb') as f:
		liste=list(csv.reader(f,delimiter=';'))
		if len(liste)!=0:
			for i in range(1,len(liste)):
				items[liste[i][0]]={}
				for j in range(1,len(liste[i])):
					if liste[i][j][:1]=="#":
						items[liste[i][0]][liste[0][j]]=int(liste[i][j][1:])
					elif liste[i][j][:1]=="[":
						atemp=liste[i][j][1:-1].split(",")
						items[liste[i][0]][liste[0][j]]=[int(atemp[k]) for k in range(len(atemp))]
					elif liste[i][j][:1]=="{":
						atemp=items[liste[i][0]][liste[0][j]]=liste[i][j][1:-1].split(",")
						items[liste[i][0]][liste[0][j]]=[atemp[k] for k in range(len(atemp))]
					elif liste[i][j][:2]=="0x":
						items[liste[i][0]][liste[0][j]]=int(liste[i][j][2:],16)
					elif liste[i][j][:1]=="&":
						items[liste[i][0]][liste[0][j]]=float(liste[i][j][1:])
					elif liste[i][j][:1]=="@":
						items[liste[i][0]][liste[0][j]]=items[liste[i][j][1:]]		
					elif liste[i][j][:1]=="%":					
						items[liste[i][0]][liste[0][j]]=image.load(liste[i][j][1:])	
					else:
						items[liste[i][0]][liste[0][j]]=liste[i][j]
				if n!=0:
					items[liste[i][0]]['value']=n+i-1
				items[items[liste[i][0]]['value']]=liste[i][0]
		f.close()
		return len(liste)-1
		
def readgrid(file):
	global unroll,mousel,mousem,mouser,cout,selected,sizex,sizey,world_old,world_new,world_art,items,zoom,play,stat,cycle,nrj,rayon,tech,decx,decy,unroll,stat,victory,current,temp,debug,nom,descriptif,element,maxnrj,maxrayon,maxcycle,maxtemp
	try:
		with open(file, 'rb') as f:
			liste=list(csv.reader(f,delimiter=';'))
			sizey=(len(liste)-1)/2
			sizex=len(liste[1])
			nom=liste[0][0]
			element=liste[0][1]
			descriptif=liste[0][2]
			debug=int(liste[0][3])
			tech=int(liste[0][7])
			cout=int(liste[0][8])		
			victemp=liste[0][9][1:len(liste[0][9])-1].split(",")
			victory=[int(victemp[k]) for k in range(len(victemp))]
			curtemp=liste[0][10][1:len(liste[0][10])-1].split(",")
			current=[int(curtemp[k]) for k in range(len(curtemp))]
			cycle=int(liste[0][11])
			nrj=int(liste[0][12])
			rayon=int(liste[0][13])
			temp=int(liste[0][14])
			maxcycle=int(liste[0][15])
			maxnrj=int(liste[0][16])
			maxrayon=int(liste[0][17])
			maxtemp=int(liste[0][18])
			world_new = [[int(liste[sizey-i][j]) for i in range(sizey)] for j in range(sizex)]
			world_art = [[int(liste[-i-1][j]) for i in range(sizey)] for j in range(sizex)]		
			f.close()
			return True
	except IOError:
		return False
		
'''********************* fonction ecriture NOUVELLE ****************************************************************'''
		
def write(afile,var):
	d=shelve.open(afile,writeback=True)
	for k in var:
		d[k]=globals()[k]
	d.sync()
	d.close()	
	
items = {}
sizeworld=loaditems(int("0x40000", 16),"data/worlds.dat")	
loaditems(int("0x30000", 16),"data/elements2.dat")	
loaditems(int("0x10000", 16),"data/menus2.dat")	
loaditems(int("0x20000", 16),"data/menus.dat")
loaditems(0,"data/elements.dat")
worlds=[]
Uworlds=[]

for i in range(sizeworld):
	ele=items[items[int("0x40000",16)+i]]
	readgrid(ele['file'])
	print "situation", ele['world'],ele['grid'],len(worlds)
	while len(worlds)<=ele['world']:
		worlds.append(0)
		worlds[ele['world']]=[]
	while len(worlds[ele['world']])<=ele['grid']:
		worlds[ele['world']].append(0)
	link=[]
	for k in ele['validate']:
		if len(k)>4:
			link.append((int(k[5]),int(k[7])))
	worlds[ele['world']][ele['grid']]={'nom':nom, 
'element':element,
'description':descriptif,
'_xx':ele['coordx'],
'_yy':ele['coordy'],
'video':ele['tuto']!="",
'link':link,
'tech':tech,
'cout':cout,
'victory':victory,
'current':current,
'cycle':cycle,
'nrj':nrj,
'rayon':rayon,
'temp':temp,
'maxcycle':maxcycle,
'maxnrj':maxnrj,
'maxrayon':maxrayon,
'maxtemp':maxtemp,
'world_new':world_new,
'world_art':world_art}
print worlds
write("dbdata",["worlds"])
f=open("dbsrc", 'wb+')
afile="""#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import shelve

def write(afile,var):
	d=shelve.open(afile,writeback=True)
	for k in var:
		d[k]=globals()[k]
	d.sync()
	d.close()


global worlds

worlds="""
f.write(afile+str(worlds).replace(", '",",\n '").replace(", [",", \n\t\t\t[")+"""\nwrite("dbdata",["worlds"])""")
f.close()
		

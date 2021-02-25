import sys, random
from sti import register as sti
bg = sti.bg
fg = sti.fg
rojo = fg(255,17,0)+""
naranja = fg(255,153,0)+""
amarillo = fg(255,217,0)+""
lima = fg(191,255,0)+""
verde = fg(85,255,0)+""
celeste = fg(0,255,115)+""
cian = fg(0,255,195)+""
gris = fg(207,207,207)+""
azul = fg(0,149,255)+""
morado = fg(162,0,255)+""
violeta = fg(255,0,242)+""
rosa = fg(255,140,215)+""
blanco = fg(255,255,255)+""

def rainbow(message): #Printea en modo arcoiris
	scale = [(255,0,0),(255,50,0),(255,100,0),(255,150,0),(255,200,0),(255,255,0),(200,255,0),(150,255,0),(100,255,0),(50,255,0),(0,255,0),(0,255,50),(0,255,100),(0,255,150),(0,255,200),(0,255,255),(0,200,255),(0,150,255),(0,100,255),(0,50,255),(0,0,255),(50,0,255),(100,0,255),(150,0,255),(200,0,255),(255,0,255),(255,0,200),(255,0,150),(255,0,100),(255,0,50),(255,0,0)]
	msg = message.replace("","@@@")
	bb = msg.split("@@@")
	a = random.randint(0,30)
	sys.stdout.write ("")
	for sc in bb:
		if a == 31: a = 0
		ls = list(scale[int(a)])
		a = a + 1
		sc = sc.replace(sc,fg(str(ls[0]),str(ls[1]),str(ls[2]))+sc+fg.rs)
		sys.stdout.write(sc)
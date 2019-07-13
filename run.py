import cv2
import numpy as np

from utils import *
	
luzAmbiente = [1, 1, 1] 
m = 10
def rayTrace(p0, p1, faces, PontoDeObservacao):

	#vetor unitario
	raio = Vec3(p1.x-p0.x, p1.y-p0.y, p1.z-p0.z)
	raio = normaliza(raio)

	orig = p0
	center = Vec3(0,0,0)
	radius2 = np.power(1, 2)
	L = sub(orig, center)
	a = vectorialProd(raio, raio)
	b = 2*vectorialProd(raio, L)
	c = vectorialProd(L, L) - radius2

	intersepta, t0, t1 = solveQuadratic(a, b, c)
	
	#Cor de fundo (B, G, R)
	if(not intersepta):
		return 0.8,0.8,0.8

	if(t0 > t1):
		aux = t0
		t0 = t1
		t1 = aux
	if(t0 < 0):
		t0 = t1

	t = t0
	normal_prox = Vec3(p0.x+t*raio.x, p0.y+t*raio.y, p0.z+t*raio.z) 	
	
	#cor de reflexao (B, G, R)
	cor_reflexo = [0, 0.3, 0]    

	#posicao da luz (x, y, z)
	vetDifusa = Vec3(-3,-3,-5) 

	normal_prox = normaliza(normal_prox)
	vetDifusa = normaliza(vetDifusa)
	PontoDeObservacao = normaliza(PontoDeObservacao)

	nvl = np.power(2*vectorialProd(normal_prox, vetDifusa)*vectorialProd(normal_prox, PontoDeObservacao)-vectorialProd(PontoDeObservacao, vetDifusa), m)

	normal_luz = vectorialProd(normal_prox, vetDifusa)

	blue = cor_reflexo[0]*luzAmbiente[0]*normal_luz+luzAmbiente[0]*nvl
	green = cor_reflexo[1]*luzAmbiente[1]*normal_luz+luzAmbiente[1]*nvl
	red = cor_reflexo[2]*luzAmbiente[2]*normal_luz+luzAmbiente[2]*nvl

	return blue, green, red 			

'''
	Posicao no espaco:
	(x, y, z)

	   |y
	   | 
	   |_______x
	   /
	  /
	 /z

'''

lin = 380
cols = 310

PontoDeObservacao = Vec3(0,2,-3)
xmin = -1
ymin = -1
xmax = 1
ymax = 2

#janela de observacao
dist = -1 

width = (xmax-xmin)/cols
height = (ymax-ymin)/lin

image = np.zeros((lin, cols, 3))

for i in range(lin):
	print(i)
	for j in range(cols):
		p0 = PontoDeObservacao
		p1 = Vec3(xmin+width*(j+0.5), ymax-height*(i+0.5), dist)
		blue, green, red  = rayTrace(p0, p1, 0, PontoDeObservacao)
		image[i,j, 0] = blue	
		image[i,j, 1] = green
		image[i,j, 2] = red

cv2.imshow('bola.jpg',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
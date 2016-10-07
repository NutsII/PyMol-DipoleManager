# Usage: DipoleCalc.py file.mol2
#
# README: basicamente, cada atomo tem suas coordenadas em XYZ multiplicadas pela carga (em dic2 na funcao grep_line). Isso cria uma componente vetorial em cada eixo, que depois sao somadas
#         (todas as X, todas as Y, todas as Z), gerando os componentes vetoriais resultantes de cada eixo (dipoleX, dipoleY e dipoleZ).
#         Depois, usa-se uma soma vetorial (descrita na equacao module), obtendo-se o modulo do vetor Momento de Dipolo
#
########################################################################
# Loading libraries
#import numpy
import sys
#import re

arq = sys.argv[1]

# Setting parameters
eA = 4.80320440079 # Debye

# Grepping coordenates and charges
def grep_line(file):

	f = open(file,"r")
	l = "text"
	dic = {}
	dic2 = {}

	for i in range(7):		#acessing the atoms
		l = f.readline()


	while True:
		l = f.readline()
		if not l: break
		if l.split()[0] == '@<TRIPOS>BOND': break   ## nao consegui fazer ele terminar o readline sem ler o @<TRIPOS>BOND. Ai fiz essa gambiarra.
		if len(l) > 0:
			atom_number = l.split()[0]
			atom_code = l.split()[1]
			atom_X = float(l.split()[2])
			atom_Y = float(l.split()[3])
			atom_Z = float(l.split()[4])
			atom_charge = float(l.split()[8])
			dic[atom_number] = (atom_code, atom_X, atom_Y, atom_Z, atom_charge)
			dic2[atom_number] = (atom_X*atom_charge,atom_Y*atom_charge,atom_Z*atom_charge)
	f.close()

	return dic2

dic = grep_line(arq)

compX = 0
compY = 0
compZ = 0

for i in dic:

	compX = dic[i][0] + compX
	compY = dic[i][1] + compY
	compZ = dic[i][2] + compZ


module = ( ((compX*eA)**2) + ((compY*eA)**2) + ((compZ*eA)**2) )**0.5

print "###################################################\n"

print '>>>>>> Componente vetorial em X = '+ str(round(compX*eA,2)) + ' D'
print '>>>>>> Componente vetorial em Y = '+ str(round(compY*eA,2)) + ' D'
print '>>>>>> Componente vetorial em Z = '+ str(round(compZ*eA,2)) + ' D'

print '\n>>>>>> Modulo resultante = ' + str(round(module,2)) + ' D'

print "\n\nMD#17: 'It's a beautiful day!' (U2)"

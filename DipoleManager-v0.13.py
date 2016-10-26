# Usage: DipoleCalc.py file.mol2                                              #
# #README: Basically, each atom has its XYZ coordinates multiplied by their   #
# electrostatic charges (in dic2, on the grep_line function). That creates on #
# vectorial component on each axis, which are summed.                         #
# which are summed, resulting in their individual dipole results.             #
# After that, it is possible to find the Dipole Moment through the "module"   #
# equation.                                                                   #
###############################################################################
# Loading libraries
#import numpy
#import sys
#import re

import Tkinter
import tkFileDialog, tkMessageBox
import numpy
from pymol import cmd
from pymol.cgo import *

dialog = Tkinter.Tk()
dialog.withdraw()
#stored.coords = []

#arq = sys.argv[1]

# Setting parameters

#CHECAR SE REALMENTE ADICIONA O DIPOLE MANAGER AO MENU DO PYMOL

def __init__(self):
        self.menuBar.addmenuitem('Plugin', 'command','Dipole Manager',label = 'Dipole Manager',command = lambda s=self : open_mol2(s))

#DESCOBRIR COMO ABRIR O MOL2 E RETORNAR O ARQUIVO

def open_mol2(self):
        #--------------
        global s2
        #--------------
        myFormatsMOL2 = [('chemical/x-mol2Tripos MOL2 molecule model files.','*.mol2')]
        try:
                self.MOL2File = tkFileDialog.askopenfile(parent=dialog,mode='rb',filetypes=myFormatsMOL2, title='Choose MOL2 file')
        except:
                quitProgram(self, "No MOL2 File!")
        if self.MOL2File != None:

                cmd.load(self.MOL2File.name, "Shingonga" )
                print "Opening MOL2 file...", self.MOL2File.name
                #get_atom_data(self)
                s2 = []
                #cmd.iterate_state(0,'(all)','s1.append({resi,name,x,y,z,partial_charge})')
                #print s1
                myspace = {'coord_taker': coord_taker}
                cmd.iterate_state(0,'(all)', 'coord_taker(resi,name,x,y,z,partial_charge)', space=myspace)
                print len(s2)
                cog_calculator(self)
                cog_drawer(self)
                #axis_setter(self)
                print self.dipx, self.dipy, self.dipz, self.mdip
                #s2[].clear[]

def coord_taker(resi,name,x,y,z,partial_charge):
    global s2
    #print '%s`%s/%s' % (resn ,resi, name)
    s2.extend([resi,name,x,y,z,partial_charge])

def cog_calculator(self):
    global s2
    counter1 = 0
    self.cogx,self.cogy,self.cogz=0,0,0
    self.dipx,self.dipy,self.dipz=0,0,0
    self.mdip = 0
    while counter1 < len(s2):
        self.cogx+=s2[counter1+2]/(len(s2)/6)
        self.cogy+=s2[counter1+3]/(len(s2)/6)
        self.cogz+=s2[counter1+4]/(len(s2)/6)
        self.dipx+=(s2[counter1+2]*s2[counter1+5]*4.80320440079)
        self.dipy+=(s2[counter1+3]*s2[counter1+5]*4.80320440079)
        self.dipz+=(s2[counter1+4]*s2[counter1+5]*4.80320440079)
        counter1+=6
    self.mdip = ((self.dipx**2) + (self.dipy**2) + (self.dipz**2))**0.5


def cog_drawer(self):
    #com_object = 'cogmol2'
    #cmd.pseudoatom(object=com_object,pos=[self.cogx, self.cogy, self.cogz])
    #cmd.pseudoatom(object=com_object,pos=[self.cogx+self.dipx, self.cogy, self.cogz])
    #cmd.pseudoatom(object=com_object,pos=[self.cogx, self.cogy+self.dipy, self.cogz])
    #cmd.pseudoatom(object=com_object,pos=[self.cogx, self.cogy, self.cogz+self.dipz])

    xcone = IsNegative(self.dipx)*0.1*abs(self.dipx)
    ycone = IsNegative(self.dipy)*0.1*abs(self.dipy)
    zcone = IsNegative(self.dipz)*0.1*abs(self.dipz)

    self.obj = []
    #PRINCIPAL
    self.obj.extend([ 25.0, 1, 9.0, self.cogx, self.cogy, self.cogz, self.cogx+self.dipx, self.cogy+self.dipy, self.cogz+self.dipz, 0.03, 1, 0, 0, 1, 0, 0 ])
    self.obj.extend([CONE, self.cogx+self.dipx, self.cogy+self.dipy, self.cogz+self.dipz, self.cogx+self.dipx+xcone, self.cogy+self.dipy+ycone, self.cogz+self.dipz+zcone, 0.10, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0])
    #AUXILIARES
    self.obj.extend([ 25.0, 0.4, 9.0, self.cogx, self.cogy, self.cogz, self.cogx+self.dipx, self.cogy, self.cogz, 0.01, 1, 0, 0, 1, 0, 0 ])
    self.obj.extend([ 25.0, 0.4, 9.0, self.cogx, self.cogy, self.cogz, self.cogx, self.cogy+self.dipy, self.cogz, 0.01, 1, 0, 0, 1, 0, 0 ])
    self.obj.extend([ 25.0, 0.4, 9.0, self.cogx, self.cogy, self.cogz, self.cogx, self.cogy, self.cogz+self.dipz, 0.01, 1, 0, 0, 1, 0, 0 ])
    self.obj.extend([CONE, self.cogx+self.dipx, self.cogy, self.cogz, self.cogx+self.dipx+xcone, self.cogy, self.cogz, 0.05, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0])
    self.obj.extend([CONE, self.cogx, self.cogy+self.dipy, self.cogz, self.cogx, self.cogy+self.dipy+ycone, self.cogz, 0.05, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0])
    self.obj.extend([CONE, self.cogx, self.cogy, self.cogz+self.dipz, self.cogx, self.cogy, self.cogz+self.dipz+zcone, 0.05, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0])
    cmd.load_cgo(self.obj,'DipoleVectors')

def IsNegative(v):
    if v > 0:
        return int(1)
    elif v == 0:
        return int(0)
    elif v < 0:
        return int(-1)

#    self.xyz1 = get_coord('xdip')
#    self.xyz2 = get_coord('ydip')
#    cmd.show_as('spheres', com_object)
#    cmd.color('yellow', com_object)
#    cmd.set ('sphere_scale', '0.1', 'cogmol2')

# def get_coord(v):
#    if not isinstance(v, str):
#        return v
#    if v.startswith('['):
#        return cmd.safe_list_eval(v)
#    return cmd.get_atom_coords(v)




#def get_atom_data(self):
#    myspace = {'bfactors': []}
#    cmd.iterate('(all)', 'bfactors.append(b)', space=myspace)
#    print bfactors
#    self.s1 = ()
#    cmd.iterate_state(0,'(all)','self.s1.append([x,y,z])')
#    print self.s1

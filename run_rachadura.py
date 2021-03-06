# -*- coding: utf-8 -*-
import random
import numpy
import time
import matplotlib.pyplot as plot
from matplotlib import colors as colors

plot.ion()

#TODO: Detectei algum bug ao deixar ele rodando por um tempo. "list index out of range" para a função mutate (linha 53) para a chamada da linha 231.

class individuo():

    ind_size = 100;
    mutation_steps = 30;
    max_heads_size = 5;
    direction_map_x = {'baixo': 1, 'cima': -1}
    direction_map_y = {'esquerda': -1, 'direita': 1}

    def __init__(self, array_in = None, pontas_in = None):
        self.array = array_in
        self.pontas = pontas_in
        if not array_in:
            self.generate()

    def mutate(self):

        # For each step
        for step in range(self.mutation_steps):
            # Verifica se criamos uma ponta aleatóriamente
            if Utils.chancenovas():
                if len(self.pontas) < self.max_heads_size:
                    escolhidox = random.randrange (0,len(self.array),1)
                    escolhidoy = random.randrange (0,len(self.array),1)

                    self.array[escolhidox][escolhidoy].valor = 1
                    new_ponta = ponta(escolhidox, escolhidoy)
                    self.pontas.append(new_ponta)

            # Verifica se eliminamos uma ponta aleatóriamente
            if Utils.chancetira():
                if self.pontas:
                    self.pontas.remove(random.choice(self.pontas))

            # Foreach pontas
            for cadaponta in self.pontas:
                # Choose a random direction
                direction = Utils.definedirecao()

                y_test = self.direction_map_y.get(direction)
                x_test = self.direction_map_x.get(direction)
                #print(x_test)
                if x_test:
                    x_move = cadaponta.valorx + x_test if (cadaponta.valorx + x_test) < len(self.array) else 0
                    self.array[x_move][cadaponta.valory].mudavalor();
                    cadaponta.valorx = x_move
                elif y_test:
                    y_move = cadaponta.valory + y_test if (cadaponta.valory + y_test) < len(self.array) else 0
                    self.array[cadaponta.valorx][y_move].mudavalor();
                    cadaponta.valory = y_move
                else:
                    raise "DirectionNotFound"

    #def cross_with(self, individuo_to_cross):
     #   pass

    def update_draw(self, ax = None, cmap = 'Greys'):
        if ax != None:
            # Builds H
            drawing_matrix = []
            for line in self.array:
                H = []
                for item in line:
                    H.append(int(item.valor))
                drawing_matrix.append(H)
            # Updates plot
            ax.imshow(drawing_matrix,cmap=cmap, interpolation="nearest")
        pass

    def generate(self):
        '''Starts the first dot'''
        #global ind_size

        # Random mutation
        self.array = [[celula() for x in range(self.ind_size)] for y in range(self.ind_size)]
        escolhidox = random.randrange (0,len(self.array),1)
        escolhidoy = random.randrange (0,len(self.array),1)

        self.array[escolhidox][escolhidoy].valor = 1;

        # Corresponding edge
        self.pontas = []
        new_ponta = ponta(escolhidox, escolhidoy)
        self.pontas.append(new_ponta)

    #def clear_single_pixels(self):
     #   pass

class Utils():

    @staticmethod
    def definedirecao():
        chance = random.randrange(0,100,1)
        if chance < 25 :
            direcao = 'cima'
        elif chance < 50 :
            direcao = 'direita'
        elif chance < 75 :
            direcao = 'baixo'
        elif chance < 101:
            direcao = 'esquerda'
        return direcao

    @staticmethod
    def chancenovas ():
        '''Chance de criar novas cabeças.'''
        chancecabeca = random.randrange(0,10001,1)
        if chancecabeca > 9998 :
            return True
        else:
            return False

    @staticmethod
    def chancetira ():
        '''Chance de tirar uma cabeça.'''
        chancetirar = random.randrange(0,10001,1)
        if chancetirar > 9999:
            return True
        else:
            return False

class celula(object):

    def __init__ (self, valor = 0):
        self.valor = valor;

    def mudavalor(self):
        self.valor = not self.valor

class ponta(object):

    def __init__ (self, valorx_in = 0, valory_in = 0):
        self.valorx = valorx_in
        self.valory = valory_in

    def recebevalor (self, x, y):
        self.valorx = x
        self.valory = y

def limpamatriz(array):
    '''Elimina pixels mortos sem vizinhança.'''
    indice = (len(array))
    pontox = 0

    while pontox != len(array):
        pontoy = 0
        while pontoy != len(array):
            compararx1 = pontox + 1
            compararx2 = pontox - 1
            comparary1 = pontoy + 1
            comparary2 = pontoy - 1
            if array[pontox][pontoy].valor == 0:
                if compararx1 == len(array):
                     compararx1 = 0
                if compararx2 == -1:
                     compararx2 = len(array) -1
                if comparary1 == len(array):
                     comparary1 = 0
                if comparary2 == -1:
                     comparary2 = len (array) -1
                if array[compararx1][pontoy].valor == 1 and array[compararx2][pontoy].valor == 1 and array[pontox][comparary1].valor == 1 and array[pontox][comparary2].valor == 1 :
                    array[pontox][pontoy].valor = 1
            if array[pontox][pontoy].valor == 1:
                if compararx1 == len(array):
                     compararx1 = 0
                if compararx2 == -1:
                     compararx2 = len(array) -1
                if comparary1 == len(array):
                     comparary1 = 0
                if comparary2 == -1:
                     comparary2 = len (array) -1
                if array[compararx1][pontoy].valor == 0 and array[compararx2][pontoy].valor == 0 and array[pontox][comparary1].valor == 0 and array[pontox][comparary2].valor == 0 :
                    array[pontox][pontoy].valor = 0
            pontoy += 1
        pontox += 1

def printamatriz (array):
    for i in range(len(array)):
        linha = []
        for j in range (len (array[i])):
            linha += [array[i][j].valor]

def main():

    def onclick(event):

        x_press = event.x
        y_press = event.y

        inv_x, inv_y = fig.transFigure.inverted().transform((x_press,y_press))

        for i , ax in enumerate(individuos_plot):
            bb = ax.get_position()
            if bb.contains(inv_x, inv_y):
                print("Found plot %d " % i)

    # Cria 4 graficos
    fig = plot.figure()
    plot.title("Escolha o seu favorito")
    plot.show(False)
    plot.hold(False)

    cMap = 'Greys'
    nb_individuos = 4 # par por favor
    pause_time = 0.0000005

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # Cria lista de graphs
    individuos_plot = []
    for i in range(nb_individuos):
        ind_temp = plot.subplot(nb_individuos/2, nb_individuos/2, i+1)
        individuos_plot.append(ind_temp)

    # Cria 4 individuos
    individuo_list = []
    for x in range(nb_individuos):
        individuo_list.append(individuo())

    while(1):
        # Muta os individuos
        for i,individuo_single in enumerate(individuo_list):
            individuo_single.mutate();
            individuo_single.update_draw(individuos_plot[i])
        # Mostra o resultado
        plot.pause(pause_time)

main()

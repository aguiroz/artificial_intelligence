#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 20:40:57 2018

@author: aguiroz
"""

from abstract import NNScreenAbstract
from nn import TFMLP, TFCNN, TFRNN
from threading import Thread
from interface import ScreenInterface
from util import save_prediction, load_model_data

#Plotting
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
from tensorflow.train import AdadeltaOptimizer, AdagradDAOptimizer ,AdagradOptimizer, AdamOptimizer, FtrlOptimizer, GradientDescentOptimizer, ProximalAdagradOptimizer, ProximalGradientDescentOptimizer, RMSPropOptimizer

from tkinter import Tk, Toplevel, Label, Button, Entry, filedialog, StringVar, Frame, OptionMenu

class TFMLPScreen(NNScreenAbstract):

    def __init__(self, features, title='Rede Neural Multicamadas', train=None, test=None):
        NNScreenAbstract.__init__(self, title, train=train, test=test)
        self.features = features
        self.nn = TFMLP(self)

        return

    def fit(self):
        Thread(target=self.nn.fit, args=[self, self.train_data, int(self.qtd_train_var.get()), int(self.qtd_test_var.get()), self.features.lr, self.features.decay, self.features.momentum, self.features.epoch, self.features.test_period, self.features.batch_sz, self.features.optimizer]).start()
        return

    def predict(self):
        prediction = self.nn.predict(self.test_data)
        data = np.loadtxt(self.test_data.name, dtype=np.uint8, skiprows=1, delimiter=',')
        x = np.array([i.reshape(28, 28) for i in data])

        for i in range(x.shape[0]):
            save_prediction(x[i], prediction[i], i, self.nn.model_name)
        return


class TFCNNScreen(NNScreenAbstract):

    def __init__(self, features, title="Rede Neural Convolucional", train=None, test=None):
        NNScreenAbstract.__init__(self, title, train=train, test=test)
        self.features = features
        self.nn = TFCNN(self, batch_sz=self.features.batch_sz)
        return

    def fit(self):
        Thread(target=self.nn.fit, args=[self, self.train_data, int(self.qtd_train_var.get()), int(self.qtd_test_var.get()), self.features.lr, self.features.decay, self.features.momentum, self.features.epoch, self.features.test_period, self.features.batch_sz, self.features.optimizer]).start()
        return

    def predict(self):
        prediction = self.nn.predict(self.test_data)
        data = np.loadtxt(self.test_data.name, dtype=np.uint8, skiprows=1, delimiter=',')
        x = np.array([i.reshape(28, 28) for i in data])

        for i in range(x.shape[0]):
            save_prediction(x[i], prediction[i], i, self.nn.model_name)
        return

class TFRNNScreen(NNScreenAbstract):

    def __init__(self, features, title="Rede Neural Recorrente", train=None, test=None):
        NNScreenAbstract.__init__(self, title, train, test)
        self.features = features
        self.nn = TFRNN(self)
        return

    def fit(self):
        Thread(target=self.nn.fit, args=[self, self.train_data, int(self.qtd_train_var.get()), int(self.qtd_test_var.get()), self.features.lr, self.features.decay, self.features.momentum, self.features.epoch, self.features.test_period, self.features.batch_sz, self.features.optimizer]).start()
        return

    def predict(self):
        prediction = self.nn.predict(self.test_data)
        data = np.loadtxt(self.test_data.name, dtype=np.uint8, skiprows=1, delimiter=',')
        x = np.array([i.reshape(28, 28) for i in data])

        for i in range(x.shape[0]):
            save_prediction(x[i], prediction[i], i, self.nn.model_name)
        return


class MainScreen(ScreenInterface, Tk):
    def __init__(self, title="MatPy"):
        Tk.__init__(self)
        self.title(title)

        self.create_model()
        self.set_position()
        self.title("MatPy")
        self.geometry("750x200+100+100")

        self.features = FeatureScreen(show=True)
        print(self.features.optimizer)

        return

    def load_mlp(self):
        objMlp = TFMLPScreen(self.features, train=self.loadData.train_data, test=self.loadData.test_data)

        return

    def load_cnn(self):
        objCnn = TFCNNScreen(self.features, train=self.loadData.train_data, test=self.loadData.test_data)

        return

    def load_rnn(self):
        objRnn = TFRNNScreen(self.features, train=self.loadData.train_data, test=self.loadData.test_data)


        return

    def get_features(self):
        self.features = FeatureScreen()
        return

    def create_model(self):
        self.lb0 = Label(self, text="")
        self.lb1 = Label(self, text="Importar Dataset")
        self.lb2 = Label(self, text="RNA Multicamadas")
        self.lb3 = Label(self, text="RNA Convolucional")
        self.lb4 = Label(self, text="RNA Recorrente")
        self.lb5 = Label(self, text="Escolher Algoritmo de Treino")
        self.lb6 = Label(self, text="Visualizar Comparativos")

        self.btn1 = Button(self, text="Carregar", command=self.load_dataset)
        self.btn2 = Button(self, text="Carregar", command=self.load_mlp)
        self.btn3 = Button(self, text="Carregar", command=self.load_cnn)
        self.btn4 = Button(self, text="Carregar", command=self.load_rnn
                           )
        self.btn5 = Button(self, text="Carregar", command=self.get_features)
        self.btn6 = Button(self, text="Carregar", command=ReportScreen)
        self.btn7 = Button(self, text="Sair", command=self.destroy)
        self.btn8 = Button(self, text="Sobre", command=self.load_about)

        return

    def set_position(self):
        self.lb0.grid(row=5, column=0)
        self.lb1.grid(row=0, column=0)
        self.lb2.grid(row=0, column=1)
        self.lb3.grid(row=2, column=1)
        self.lb4.grid(row=4, column=1)
        self.lb5.grid(row=0, column=2)
        self.lb6.grid(row=0, column=3)

        self.btn1.grid(row=1, column=0)
        self.btn2.grid(row=1, column=1)
        self.btn3.grid(row=3, column=1)
        self.btn4.grid(row=5, column=1)
        self.btn5.grid(row=1, column=2)
        self.btn6.grid(row=1, column=3)
        self.btn8.grid(row=16, column=15)
        self.btn7.grid(row=16, column=16)

        return

    def load_dataset(self):
        self.loadData = LoadData(self)

        return

    def load_about(self):
        self.LoadData = LoadAbout(self)

        return

class LoadAbout(ScreenInterface, Toplevel):

    def __init__(self, root, title="Sobre o Software"):
        Toplevel.__init__(self, root)
        self.title(title)

        self.create_model()
        self.set_position()

        self.geometry("450x315+100+100")

    def create_model(self):
        self.lb1 = Label(self, text="UNIP 2018 - Ciência da Computação")
        self.lb2 = Label(self, text="Todos os direitos reservados.")
        self.lb22 = Label(self, text=" ")
        self.lb3 = Label(self, text="Projeto disponível em GitHub: https://github.com/aguiroz/tcc_unip")
        self.lb4 = Label(self, text="Autores: @aguiroz @diogofelix @fabiosoaresv @marcosaabarbosa")
        self.lb44 = Label(self, text=" ")
        self.lb5 = Label(self, text="O Trabalho de Conclusão de Curso realizado consiste em realizar ")
        self.lb6 = Label(self, text="uma análise comparativa entre Redes Neurais Artificiais, para ")
        self.lb7 = Label(self, text="validarmos qual algorimo de otimização e qual arquitetura de RNA ")
        self.lb8 = Label(self, text="obteve os melhores resultados em relação à consumo de recursos ")
        self.lb9 = Label(self, text="computacionais, taxa de acerto e tempo. ")
        self.lb99 = Label(self, text=" ")
        self.lb10 = Label(self, text="Obrigado à todos que contribuíram para este projeto :)")

        self.btn1 = Button(self, text="Voltar", command=self.destroy)

        return

    def set_position(self):

        self.lb1.grid(row=0, column=1)
        self.lb2.grid(row=1, column=1)
        self.lb3.grid(row=2, column=1)
        self.lb4.grid(row=3, column=1)
        self.lb44.grid(row=4, column=1)
        self.lb5.grid(row=5, column=1)
        self.lb6.grid(row=6, column=1)
        self.lb7.grid(row=7, column=1)
        self.lb8.grid(row=8, column=1)
        self.lb9.grid(row=9, column=1)
        self.lb99.grid(row=10, column=1)
        self.lb10.grid(row=11, column=1)
        self.btn1.grid(row=12, column=1)

        return

class LoadData(ScreenInterface, Toplevel):

    def __init__(self, root, title="Importar Dataset"):
        Toplevel.__init__(self, root)
        self.title(title)

        self.create_model()
        self.set_position()

        self.geometry("300x120+100+100")

    def set_position(self):

        self.lb1.grid(row=0, column=0)
        self.lb2.grid(row=2, column=0)
        self.ed1.grid(row=0, column=1)
        self.ed2.grid(row=2, column=1)
        self.btn1.grid(row=0, column=2)
        self.btn2.grid(row=2, column=2)
        self.btn3.grid(row=5, column=1)
        self.btn4.grid(row=7, column=1)

        return

    def add_action(self):
        pass

    def set_data(self):
        self.destroy()
        return

    def load_train_data(self):
        self.train_data = filedialog.askopenfile(initialdir="./data", title="Select File", filetypes=(("csv files", "*.csv"),("all files", "*.*")))
        self.train_var.set(self.train_data.name)
        return

    def load_test_data(self):
        self.test_data = filedialog.askopenfile(initialdir="./data", title="Select File", filetypes=(("csv files", "*.csv"),("all files", "*.*")))
        self.test_var.set(self.test_data.name)
        return

    def create_model(self):
        self.lb1 = Label(self, text="Treino: ")
        self.lb2 = Label(self, text="Teste: ")

        self.train_var = StringVar()
        self.test_var = StringVar()

        self.ed1 = Entry(self, textvariable=self.train_var)
        self.ed2 = Entry(self, textvariable=self.test_var)

        self.btn1 = Button(self, text="Procurar...", command=self.load_train_data)
        self.btn2 = Button(self, text="Procurar...", command=self.load_test_data)
        self.btn3 = Button(self, text="Selecionar", command=self.set_data)
        self.btn4 = Button(self, text="Cancelar", command=self.destroy)

        return

class ReportScreen(ScreenInterface, Toplevel):
    def __init__(self, title="Comparativos entre as RNA's"):
        Toplevel.__init__(self)

        self.create_model()
        self.set_position()

        self.title(title)
        self.geometry("1100x900+100+100")

        self.load_data()
        self.set_data()

        return

    def load_data(self):

        self.mlp = load_model_data('MLP', 'train_data')
        self.cnn = load_model_data('CNN', 'train_data')
        self.rnn = load_model_data('RNN', 'train_data')

        return

    def set_data(self):

        self.mlp_cost.set(self.mlp[-1, 2][0])
        self.mlp_rate.set("{} %".format(self.mlp[-1, 3][0] / self.mlp[-1, 4][0] * 100))
        self.mlp_correct.set("{} / {}".format(int(self.mlp[-1, 3][0]), int(self.mlp[-1, 4][0])))
        self.mlp_time.set(self.mlp[-1, 1][0])
        self.mlp_mem.set(self.mlp[-1, 5][0])

        self.cnn_cost.set(self.cnn[-1, 2][0])
        self.cnn_rate.set("{} %".format(self.cnn[-1, 3][0] / self.cnn[-1, 4][0] * 100))
        self.cnn_correct.set("{} / {}".format(int(self.cnn[-1, 3][0]), int(self.cnn[-1, 4][0])))
        self.cnn_time.set(self.cnn[-1, 1][0])
        self.cnn_mem.set(self.cnn[-1, 5][0])

        self.rnn_cost.set(self.rnn[-1, 2][0])
        self.rnn_rate.set("{} %".format(self.rnn[-1, 3][0] / self.rnn[-1, 4][0] * 100))
        self.rnn_correct.set("{} / {}".format(int(self.rnn[-1, 3][0]), int(self.rnn[-1, 4][0])))
        self.rnn_time.set(self.rnn[-1, 1][0])
        self.rnn_mem.set(self.rnn[-1, 5][0])

        return

    def create_model(self):

        self.lb0 = Label(self, text="Estatísticas ")
        self.lb1 = Label(self, text="Rede Neural Multicamadas")
        self.lb2 = Label(self, text="Custo Final: ")
        self.lb3 = Label(self, text="Taxa de Acerto: ")
        self.lb4 = Label(self, text="Qtde de Acerto: ")
        self.lb5 = Label(self, text="Tempo Decorrido: ")
        self.lb_mem_mlp = Label(self, text='Consumo médio de Memória')

        self.lb6 = Label(self, text="Rede Neural Convolucional ")
        self.lb7 = Label(self, text="Custo Final: ")
        self.lb8 = Label(self, text="Taxa de Acerto: ")
        self.lb9 = Label(self, text="Qtde de Acerto: ")
        self.lb10 = Label(self, text="Tempo Decorrido: ")
        self.lb_mem_cnn = Label(self, text='Consumo médio de Memória')

        self.lb11 = Label(self, text="Rede Neural Recorrente")
        self.lb12 = Label(self, text="Custo Final: ")
        self.lb13 = Label(self, text="Taxa de Acerto: ")
        self.lb14 = Label(self, text="Qtde de Acerto: ")
        self.lb15 = Label(self, text="Tempo Decorrido: ")
        self.lb_mem_rnn = Label(self, text='Consumo médio de Memória')

        self.lb16 = Label(self, text=" ")
        self.lb17 = Label(self, text=" ")
        self.lb18 = Label(self, text=" ")

        self.lb19 = Label(self, text="Gráficos ")
        self.lb20 = Label(self, text="Gráfico Tempo x Iteração: ")
        self.lb21 = Label(self, text="Gráfico Custo x Acerto: ")
        self.lb22 = Label(self, text="Gráfico Custo x Iteração: ")

        self.lblTime = Label(self, text="Gráfico de Tempo")
        self.lblCost = Label(self, text="Gráfico de Custo")
        self.lbMemory = Label(self, text="Gráfico de Memória")

        self.btnTime = Button(self, text="Gerar", command=self.plot_time)
        self.btnCost = Button(self, text="Gerar", command=self.plot_cost)
        self.btnMemory = Button(self, text="Gerar", command=self.plot_memory)

        self.lblAlg = Label(self, text='RMSProp')
        self.btnNextAlg = Button(self, text='>', command=self.next_alg)
        self.btnPrevAlg = Button(self, text='<', command=self.prev_alg)

        self.mlp_cost = StringVar()
        self.mlp_rate = StringVar()
        self.mlp_correct = StringVar()
        self.mlp_time = StringVar()
        self.mlp_mem = StringVar()

        self.cnn_cost = StringVar()
        self.cnn_rate = StringVar()
        self.cnn_correct = StringVar()
        self.cnn_time = StringVar()
        self.cnn_mem = StringVar()

        self.rnn_cost = StringVar()
        self.rnn_rate = StringVar()
        self.rnn_correct = StringVar()
        self.rnn_time = StringVar()
        self.rnn_mem = StringVar()

        self.ed1 = Entry(self, textvariable=self.mlp_cost)
        self.ed2 = Entry(self, textvariable=self.mlp_rate)
        self.ed3 = Entry(self, textvariable=self.mlp_correct)
        self.ed4 = Entry(self, textvariable=self.mlp_time)
        self.ed_mem_cnn = Entry(self, textvariable=self.cnn_mem)

        self.ed5 = Entry(self, textvariable=self.cnn_cost)
        self.ed6 = Entry(self, textvariable=self.cnn_rate)
        self.ed7 = Entry(self, textvariable=self.cnn_correct)
        self.ed8 = Entry(self, textvariable=self.cnn_time)
        self.ed_mem_mlp = Entry(self, textvariable=self.mlp_mem)

        self.ed9 = Entry(self, textvariable=self.rnn_cost)
        self.ed10 = Entry(self, textvariable=self.rnn_rate)
        self.ed11 = Entry(self, textvariable=self.rnn_correct)
        self.ed12 = Entry(self, textvariable=self.rnn_time)
        self.ed_mem_rnn = Entry(self, textvariable=self.rnn_mem)


        self.btn1 = Button(self, text="Gerar", command=self.plot_train_x_iteration)
        self.btn2 = Button(self, text="Gerar", command=self.plot_cost_x_correct)
        self.btn3 = Button(self, text="Gerar", command=self.plot_cost_x_iteration)

        #Plotting
        self.plot_frame = Frame(self, width=150, height=150, background='white')
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.graph = FigureCanvasTkAgg(self.figure, master=self.plot_frame)

        return

    def set_position(self):

        # Feedforward
        self.lb1.grid(row=4, column=0, columnspan=2)
        self.lb2.grid(row=6, column=0)
        self.lb3.grid(row=7, column=0)
        self.lb4.grid(row=8, column=0)
        self.lb5.grid(row=9, column=0)
        self.lb_mem_mlp.grid(row=10, column=0)

        # RNN
        self.lb6.grid(row=4, column=2, columnspan=2)
        self.lb7.grid(row=6, column=2)
        self.lb8.grid(row=7, column=2)
        self.lb9.grid(row=8, column=2)
        self.lb10.grid(row=9, column=2)
        self.lb_mem_cnn.grid(row=10, column=2)

        # CNN
        self.lb11.grid(row=4, column=4, columnspan=2)
        self.lb12.grid(row=6, column=4)
        self.lb13.grid(row=7, column=4)
        self.lb14.grid(row=8, column=4)
        self.lb15.grid(row=9, column=4)
        self.lb_mem_rnn.grid(row=10, column=4)

        # Label's de divisão
        self.lb17.grid(row=12, column=0)
        self.lb18.grid(row=15, column=0)

        self.ed1.grid(row=6, column=1)
        self.ed2.grid(row=7, column=1)
        self.ed3.grid(row=8, column=1)
        self.ed4.grid(row=9, column=1)
        self.ed_mem_mlp.grid(row=10, column=1)

        self.ed5.grid(row=6, column=3)
        self.ed6.grid(row=7, column=3)
        self.ed7.grid(row=8, column=3)
        self.ed8.grid(row=9, column=3)
        self.ed_mem_cnn.grid(row=10, column=3)

        self.ed9.grid(row=6, column=5)
        self.ed10.grid(row=7, column=5)
        self.ed11.grid(row=8, column=5)
        self.ed12.grid(row=9, column=5)
        self.ed_mem_rnn.grid(row=10, column=5)

        # Label's de divisão
        self.lb19.grid(row=16, column=2)
        self.lb20.grid(row=17, column=4)
        self.btn1.grid(row=17, column=5)
        self.lb21.grid(row=18, column=4)
        self.btn2.grid(row=18, column=5)
        self.lb22.grid(row=19, column=4)
        self.btn3.grid(row=19, column=5)

        self.lblTime.grid(row=17, column=1)
        self.lblCost.grid(row=18, column=1)
        self.lbMemory.grid(row=19, column=1)

        self.btnTime.grid(row=17, column=2)
        self.btnCost.grid(row=18, column=2)
        self.btnMemory.grid(row=19, column=2)

        self.lblAlg.grid(row=15, column=2)
        self.btnPrevAlg.grid(row=15, column=1)
        self.btnNextAlg.grid(row=15, column=3)


        #Plotting
        self.plot_frame.grid(row=20, column=1, columnspan=10)
        self.ax.grid()
        self.graph.get_tk_widget().pack(side='top', fill='both', expand=True)

        return

    def next_alg(self):

        if self.lblAlg['text'] == 'Descida Gradiente':
            self.lblAlg['text'] = 'Adadelta'
            self.mlp = load_model_data('MLP/Adadelta', 'train_data')
            self.cnn = load_model_data('CNN/Adadelta', 'train_data')
            self.rnn = load_model_data('RNN/Adadelta', 'train_data')
            self.set_data()
            return

        if self.lblAlg['text'] == 'Adadelta':
            self.lblAlg['text'] = 'RMSProp'
            self.mlp = load_model_data('MLP/RMSProp', 'train_data')
            self.cnn = load_model_data('CNN/RMSProp', 'train_data')
            self.rnn = load_model_data('RNN/RMSProp', 'train_data')
            self.set_data()
            return

        if self.lblAlg['text'] == 'RMSProp':
            return



    def prev_alg(self):
        if self.lblAlg['text'] == 'Descida Gradiente':
            return

        if self.lblAlg['text'] == 'Adadelta':
            self.lblAlg['text'] = 'Descida Gradiente'
            self.mlp = load_model_data('MLP/GradientDescent', 'train_data')
            self.cnn = load_model_data('CNN/GradientDescent', 'train_data')
            self.rnn = load_model_data('RNN/GradientDescent', 'train_data')
            self.set_data()
            return

        if self.lblAlg['text'] == 'RMSProp':
            self.lblAlg['text'] = 'Adadelta'
            self.mlp = load_model_data('MLP/Adadelta', 'train_data')
            self.cnn = load_model_data('CNN/Adadelta', 'train_data')
            self.rnn = load_model_data('RNN/Adadelta', 'train_data')
            self.set_data()
            return

        return


    def plot_train_x_iteration(self):

        self.ax.cla()
        self.ax.grid()
        self.ax.plot(self.mlp[:, 0], self.mlp[:, 1], color='red')
        self.ax.plot(self.cnn[:, 0], self.cnn[:, 1], color='green')
        self.ax.plot(self.rnn[:, 0], self.rnn[:, 1], color='blue')
        self.ax.legend(['Rede Multicamadas', 'Rede Convolucional', 'Rede Recorrente'])
        self.ax.set_xlabel('Iteração')
        self.ax.set_ylabel('Tempo')
        self.graph.draw()

        return

    def plot_cost_x_correct(self):

        self.ax.cla()
        self.ax.grid()
        self.ax.plot(self.mlp[:, 3], self.mlp[:, 2], color='red')
        self.ax.plot(self.cnn[:, 3], self.cnn[:, 2], color='green')
        self.ax.plot(self.rnn[:, 3], self.rnn[:, 2], color='blue')
        self.ax.legend(['Rede Multicamadas', 'Rede Convolucional', 'Rede Recorrente'])
        self.ax.set_xlabel('Acerto')
        self.ax.set_ylabel('Custo')
        self.graph.draw()

        return

    def plot_cost_x_iteration(self):

        self.ax.cla()
        self.ax.grid()
        self.ax.plot(self.mlp[:, 0], self.mlp[:, 2], color='red')
        self.ax.plot(self.cnn[:, 0], self.cnn[:, 2], color='green')
        self.ax.plot(self.rnn[:, 0], self.rnn[:, 2], color='blue')
        self.ax.legend(['Rede Multicamadas', 'Rede Convolucional', 'Rede Recorrente'])
        self.ax.set_xlabel('Iteração')
        self.ax.set_ylabel('Custo')
        self.graph.draw()

        return

    def plot_time(self):

        self.ax.cla()
        self.ax.grid()
        self.ax.plot(self.mlp[:, 1], color='red')
        self.ax.plot(self.cnn[:, 1], color='green')
        self.ax.plot(self.rnn[:, 1], color='blue')
        self.ax.legend(['Rede Multicamadas', 'Rede Convolucional', 'Rede Recorrente'])
        self.ax.set_xlabel('Iteração')
        self.ax.set_ylabel('Tempo (Segundos)')
        self.graph.draw()

        return

    def plot_cost(self):

        self.ax.cla()
        self.ax.grid()
        self.ax.plot(self.mlp[:, 2], color='red')
        self.ax.plot(self.cnn[:, 2], color='green')
        self.ax.plot(self.rnn[:, 2], color='blue')
        self.ax.legend(['Rede Multicamadas', 'Rede Convolucional', 'Rede Recorrente'])
        self.ax.set_xlabel('Iteração')
        self.ax.set_ylabel('Custo')
        self.graph.draw()

        return

    def plot_memory(self):

        self.ax.cla()
        self.ax.grid()
        self.ax.plot(self.mlp[:, 5], color='red')
        self.ax.plot(self.cnn[:, 5], color='green')
        self.ax.plot(self.rnn[:, 5], color='blue')
        self.ax.legend(['Rede Multicamadas', 'Rede Convolucional', 'Rede Recorrente'])
        self.ax.set_xlabel('Iteração')
        self.ax.set_ylabel('Consumo de Memória (GB)')
        self.graph.draw()

        return


class FeatureScreen(ScreenInterface, Toplevel):

    def __init__(self, title='Algorimo de Treino', show=False):
        Toplevel.__init__(self)

        self.create_model()
        self.set_position()

        self.title(title)
        self.geometry("300x200+100+100")

        if show:
            self.set_param()

        return

    def create_model(self):

        #Labels
        self.lb0 = Label(self, text="Taxa de Aprendizagem ")
        self.lb1 = Label(self, text="Decay ")
        self.lb2 = Label(self, text="Momentum ")
        self.lb3 = Label(self, text="Iterações ")
        self.lb4 = Label(self, text="Periodo de Teste ")
        self.lb5 = Label(self, text="Tamanho do Lote ")
        self.lb6 = Label(self, text="Algoritmo ")

        #Textvar
        self.lr_var = StringVar(self, value='0.001')
        self.decay_var = StringVar(self, value='0.9')
        self.mom_var = StringVar(self, value='0.0')
        self.epoch_var = StringVar(self, value='10')
        self.test_period_var = StringVar(self, value='10')
        self.batch_sz_var = StringVar(self, value='500')
        self.algorithm_var = StringVar(self, value='RMSPropOptimizer')

        #Options
        self.options = {'AdadeltaOptimizer', 'AdagradDAOptimizer', 'AdagradOptimizer', 'AdamOptimizer', 'FtrlOptimizer', 'GradientDescentOptimizer', 'ProximalAdagradOptimizer', 'ProximalGradientDescentOptimizer', 'RMSPropOptimizer'}

        #Algorithm
        self.algorithm = {
                'AdadeltaOptimizer': AdadeltaOptimizer,
                'AdagradDAOptimizer': AdagradDAOptimizer,
                'AdagradOptimizer': AdagradOptimizer,
                'AdamOptimizer': AdamOptimizer,
                'FtrlOptimizer': FtrlOptimizer,
                'GradientDescentOptimizer': GradientDescentOptimizer,
                'ProximalAdagradOptimizer': ProximalAdagradOptimizer,
                'ProximalGradientDescentOptimizer': ProximalGradientDescentOptimizer,
                'RMSPropOptimizer': RMSPropOptimizer
            }

        #Entry
        self.ed0 = Entry(self, textvariable=self.lr_var)
        self.ed1 = Entry(self, textvariable=self.decay_var)
        self.ed2 = Entry(self, textvariable=self.mom_var)
        self.ed3 = Entry(self, textvariable=self.epoch_var)
        self.ed4 = Entry(self, textvariable=self.test_period_var)
        self.ed5 = Entry(self, textvariable=self.batch_sz_var)

        #Dropdown
        self.opt = OptionMenu(self, self.algorithm_var, *self.options)

        #Button
        self.btnSave = Button(self, text='Save', command= lambda: self.set_param(self.lr_var.get(), self.decay_var.get(), self.mom_var.get(), self.epoch_var.get(), self.test_period_var.get(), self.batch_sz_var.get(), self.algorithm_var.get()))
        self.btnCancel = Button(self, text='Cancel', command=self.cancel)

        return

    def set_position(self):

        self.lb0.grid(row=1, column=0)
        self.lb1.grid(row=2, column=0)
        self.lb2.grid(row=3, column=0)
        self.lb3.grid(row=4, column=0)
        self.lb4.grid(row=5, column=0)
        self.lb5.grid(row=6, column=0)
        self.lb6.grid(row=7, column=0)

        self.ed0.grid(row=1, column=1)
        self.ed1.grid(row=2, column=1)
        self.ed2.grid(row=3, column=1)
        self.ed3.grid(row=4, column=1)
        self.ed4.grid(row=5, column=1)
        self.ed5.grid(row=6, column=1)

        self.opt.grid(row=7, column=1)

        self.btnSave.grid(row=8, column=0)
        self.btnCancel.grid(row=8, column=1)

        return

    def set_param(self, lr=0.001, decay=0.9, momentum=0.0, epoch=10, test_period=10, batch_sz=500, optimizer='RMSPropOptimizer'):

        self.lr = lr
        self.decay = decay
        self.momentum = momentum
        self.epoch = epoch
        self.test_period = test_period
        self.batch_sz = batch_sz
        self.optimizer = self.algorithm[optimizer]

        self.destroy()

        return

    def cancel(self):

        self.lr = 0.001
        self.decay = 0.9
        self.momentum = 0.0
        self.epoch = 10
        self.test_period = 10
        self.batch_sz = 300
        self.optimizer = self.algorithm['RMSPropOptimizer']

        self.destroy()

        return


if __name__ == "__main__":

    obj = MainScreen()
    obj.mainloop()

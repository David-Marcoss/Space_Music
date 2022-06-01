import sys

from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox
from PyQt5 import QtWidgets,QtGui


from interface2 import Ui_MainWindow as interface

sys.path.insert(1, '../')

from Classes.Class_tocar import tocar
from Classes.Class_musicas_desktop import musicas_descktop
from funcoe_auxiliares import formata_tempo

import threading
import pygame


class main_telas(QtWidgets.QWidget):

    def setupUi(self,Main):
        Main.setObjectName('Main')
        Main.resize(900, 600) #tamanho tela

        Main.setWindowTitle("Space Music")
        Main.setWindowIcon(QtGui.QIcon("imagens/icon_space.png"))

        self.QtStack = QtWidgets.QStackedLayout()

        self.QtStack0 = QtWidgets.QMainWindow()


        self.interface = interface()
        self.interface.setupUi(self.QtStack0)

        self.QtStack.addWidget(self.QtStack0)  # tela login




class main(QMainWindow,main_telas):

    def __init__(self,parent=None):
        super(main_telas,self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Space Music")
        self.setWindowIcon(QtGui.QIcon("imagens/icon_space.png"))


        """--------------------------BOTOES FUNCIONALIDADES DO PLAYER --------------------"""

        """BOTOES TELA MUSICA-------------------------------------------"""
        self.interface.botaoplay.clicked.connect(self.iniciar_reprodutor)
        self.interface.botao_playaleatorio.clicked.connect(self.tocar_musica_aleatoria)
        self.interface.listWidget.clicked.connect(self.tocar_musica_lista_tl_musica)

        """ BOTAOES TELA FAVORITOS """

        """BOTOES TELA PLAYER---------------------------------------------"""
        self.interface.botaoplay_2.clicked.connect(self.iniciar_reprodutor)
        self.interface.botaopassar.clicked.connect(self.passar_musica)
        self.interface.botaovoltar.clicked.connect(self.voltar_musica)
        self.interface.botaoaleatorio.clicked.connect(self.musica_aleatoria)

        self.interface.listmusicas.clicked.connect(self.tocar_musica_lista)  #toca uma musica da lista

        self.interface.volume_2.sliderReleased.connect(self.setvolume1)
        self.interface.volume_2.sliderMoved.connect(self.setvolume1)
        self.interface.botaovolume_2.clicked.connect(self.botao_volume)

        self.interface.progresso.sliderReleased.connect(self.tocar_apartir)
        self.interface.progresso.sliderMoved.connect(self.pausar)

        self.interface.botao_voltar.clicked.connect(self.abrir_tl_musica)

        """BOTOES FRAME 20 O SUB PLAYER------------------------------------------------"""
        self.interface.botao_abrir_2.clicked.connect(self.abrir_player)
        self.interface.botao_fecahr_2.clicked.connect(self.parar_reprodutor)

        self.interface.botao_PLAY_2.clicked.connect(self.iniciar_reprodutor)
        self.interface.botao_passar_2.clicked.connect(self.passar_musica)
        self.interface.botao_volatr_2.clicked.connect(self.voltar_musica)
        self.interface.botao_aleatorio_2.clicked.connect(self.musica_aleatoria)

        self.interface.volume_3.sliderReleased.connect(self.setvolume2)
        self.interface.volume_3.sliderMoved.connect(self.setvolume2)
        self.interface.botaovolume_3.clicked.connect(self.botao_volume)

        """--------------------------CLASSES E VARIAVEIS AUXILIARES --------------------"""

        self.songs = musicas_descktop.songs()      #armacena objeto contendo todos arquivos mp3 do computador

        self.play = tocar(self.songs)              #OBJETO RESPONSAVEL PELA REPRODUÇÃO DAS MUSICAS
        self.sinc = threading.Lock()               #VARIAVEL DE SINCRONISAÇÃO DAS THREADS DO SISTEMA

        #variaveis auxiliares
        self.volumeant = None               #armazena o valor do volume caso o volume seja mutado
        self.set_tempo_de_reproducao = 0    #armazena o tempo em que uma musica sera iniciada

        self.imprimir_lista_musicas()
        self.abrir_tl_musica()  ##ABRE A TELA INICIAL DO SISTEMA
        """-----------------------------------------------------------------------------"""


    """FUNÇÕES REFERENTE A REPRODUÇÃO DE MUSICAS"""

    def iniciar_reprodutor(self):
        threading.Thread(target=self.tocar_musica, args=()).start()


    def tocar_musica(self):

        self.play.player()
        self.interface.progresso.setMaximum(self.play.tempo_total_de_reproducao)
        self.interface.imprimir_tempo_f(formata_tempo(self.play.tempo_total_de_reproducao))

        self.interface.imprimir_titulo_musica(self.play.musicas[self.play.musica_tocando].titulo,self.play.musicas[self.play.musica_tocando].artista)

        if self.play.tocando == True:

            self.interface.troca_imagem_pause()
            self.interface.frame_33.setVisible(True)

        else:
            self.interface.troca_imagem_play()

        print(f"{self.play.musica_tocando} {self.play.musicas[self.play.musica_tocando].titulo}")

        self.progresso()

        self.play.fluxo_de_reproducao()

        if self.play.tocando != False and self.play.proxima != "parar":

            self.set_tempo_de_reproducao = 0

            self.tocar_musica()


        else:
            self.proxima = 'passar'




    def progresso(self):

        while (pygame.mixer.music.get_busy() != False):
            self.imprimir_tempo_progresso()


    def imprimir_tempo_progresso(self):
        self.play.tempo_de_reproducao = int(pygame.mixer.music.get_pos() / 1000) + self.set_tempo_de_reproducao
        self.interface.progresso.setValue(self.play.tempo_de_reproducao)

        self.interface.imprimir_tempo(formata_tempo(self.play.tempo_de_reproducao), self.play.tempo_total_de_reproducao)

    def passar_musica(self):
        self.sinc.acquire()
        self.interface.troca_imagem_play()
        self.interface.imprimir_titulo_musica(self.play.musicas[self.play.musica_tocando].titulo,self.play.musicas[self.play.musica_tocando].artista)
        self.play.passar()

        self.sinc.release()


    def voltar_musica(self):
        self.interface.imprimir_titulo_musica(self.play.musicas[self.play.musica_tocando].titulo,self.play.musicas[self.play.musica_tocando].artista)
        self.interface.troca_imagem_play()
        self.sinc.acquire()
        self.play.voltar()
        self.sinc.release()

    def tocar_musica_lista(self):
        self.play.musica_tocando = self.interface.listmusicas.currentRow()

        if self.play.tocando != True:
            self.play.parar()
            self.iniciar_reprodutor()

        else:
            if self.play.proxima != "aleatorio":
                self.play.proxima = 'musicalista'

            self.play.parar()

    def tocar_musica_lista_tl_musica(self):
        self.play.musica_tocando = self.interface.listWidget.currentRow()


        if self.play.tocando != True:
           self.play.parar()
           self.iniciar_reprodutor()

        else:
            self.play.proxima = 'musicalista'
            self.play.parar()


    def setvolume1(self):
        v = self.interface.volume_2.value()/10
        self.interface.volume_3.setValue(self.interface.volume_2.value())
        self.play.setvolume(v)

        if v > 0:
            self.interface.troca_imagem_voume()
        else:
            self.interface.troca_imagem_mute()

    def setvolume2(self):

        v = self.interface.volume_3.value()/10

        self.interface.volume_2.setValue(self.interface.volume_3.value())
        self.play.setvolume(v)

        if v > 0:
            self.interface.troca_imagem_voume()
        else:
            self.interface.troca_imagem_mute()


    def botao_volume(self):

        if self.play.getvolume() != 0:

            self.interface.troca_imagem_mute()

            self.volumeant = self.play.getvolume()
            self.play.setvolume(0.0)

            self.interface.volume_2.setVisible(False)
            self.interface.volume_3.setVisible(False)

        else:
            self.interface.troca_imagem_voume()
            self.play.setvolume(self.volumeant)
            self.interface.volume_2.setVisible(True)
            self.interface.volume_3.setVisible(True)



    def tocar_apartir(self):  #problema aqui pode ocorrer interrupção da aplicação

        try:
            if self.play.tocando == True:
                self.play.pausar()

            self.sinc.acquire()
            if self.play.tocando != None:

                tempo = self.interface.progresso.value()
                self.play.tocar_apartir(tempo)
                self.set_tempo_de_reproducao = tempo
                self.iniciar_reprodutor()

            self.sinc.release()

        except:
            self.tocar_apartir()



    def pausar(self):

        if self.play.tocando == True:
            self.play.pausar()
            print('pausei')

    def parar_reprodutor(self):
        self.play.proxima = "parar"
        self.play.parar()

        self.interface.troca_imagem_play()
        self.interface.frame_33.setVisible(False)

    def musica_aleatoria(self):

        if self.play.proxima != 'aleatorio':

            self.play.proxima = 'aleatorio'
            self.play.aleatorio = []
            self.interface.botao_aleatorio_ativado()

        else:
            self.interface.botao_aleatorio_desativado()
            self.play.proxima = 'passar'

    def tocar_musica_aleatoria(self):

        from random import randint

        if self.play.tocando != True:
            self.play.musica_tocando = randint(0,len(self.songs)-1)
            self.iniciar_reprodutor()

        self.musica_aleatoria()


    def abrir_tl_musica(self):

        if self.play.tocando != None:
            self.interface.frame_33.setVisible(True)

        else:
            self.interface.frame_33.setVisible(False)

        self.interface.imprimir_info_playlist("Musicas",f"{len(self.songs)}")
        self.interface.stackedWidget.setCurrentWidget(self.interface.tl_musicas)


    def abrir_player(self):

        if self.play.tocando != True:
            self.iniciar_reprodutor()
            self.interface.frame_33.setVisible(True)


        self.interface.stackedWidget.setCurrentWidget(self.interface.tl_player)



    def imprimir_lista_musicas(self):
        """
        :return: devolve uma lista com os titulos das musicas e a quantidade de musicas da lista
        """

        lista = []

        for i in self.songs:
            if i.artista != "None":

                lista.append(f"{i.titulo} - {i.artista}")

            else:
                lista.append(f"{i.titulo}")


        self.interface.adcionar_lista_musica(lista)




if __name__ == '__main__':
    app= QApplication(sys.argv)
    show_main = main()
    sys.exit(app.exec_())
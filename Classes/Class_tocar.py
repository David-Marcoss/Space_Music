import pygame
from random import randint

class tocar:

    def __init__(self, songs):

        """

        :param songs: discionario contendo arquivos mp3
        """

        self.musicas = songs

        self.musica_tocando = 0
        self.tocando = None

        pygame.mixer.init()

        self.proxima = "passar"
        self.volume = 10

        self.aleatorio = []

        self.tempo_de_reproducao = 0
        self.tempo_total_de_reproducao = 0


    def player(self):
        print(self.musica_tocando)
        musica = self.musicas[self.musica_tocando]

        self.tempo_de_reproducao = 0
        self.tempo_total_de_reproducao = musica.duracao

        if self.tocando == None:
            self.tocar_musica(musica.musica)

        elif self.tocando == True:
            self.pausar()

        elif self.tocando == False:
            self.retomar()

        else:
            self.parar()

        return self.tocando


    def tocar_musica(self,musica):
        self.tocando = True
        pygame.mixer.music.load(musica)
        pygame.mixer.music.play()


    def fluxo_de_reproducao(self):

        if self.tocando != False:
            self.parar()

            if self.proxima == 'passar':
                if self.musica_tocando < len(self.musicas) - 1:
                    self.musica_tocando += 1

            elif self.proxima == 'voltar':
                self.proxima = 'passar'
                if self.musica_tocando > 0:
                    self.musica_tocando -= 1

            elif self.proxima == "aleatorio":

                musica = randint(0,len(self.musicas)-1)

                while (musica in self.aleatorio and len(self.aleatorio) < len(self.musicas)):
                    musica = randint(0, len(self.musicas) - 1)

                if (len(self.aleatorio) < len(self.musicas)):

                    self.aleatorio.append(musica)
                    self.musica_tocando = musica

            elif self.proxima == "parar":
                self.tocando = None

            else:
                if self.proxima != 'aleatorio':
                    self.proxima = 'passar'


    def pausar (self):
        if self.tocando != False:
            self.tocando = False
            pygame.mixer.music.pause()

    def retomar (self):
        if self.tocando != True:
            self.tocando = True
            pygame.mixer.music.unpause() #Continua da local pausado

    def parar(self):

        if self.tocando != None:
            #print("parei")
            self.tocando = None
            pygame.mixer.music.stop()

    def passar(self):

        if self.proxima != 'aleatorio':
            self.proxima = 'passar'

        if self.tocando == True:
            self.parar()
        else:
            self.parar()
            if self.musica_tocando < len(self.musicas) - 1:
                self.musica_tocando += 1

            self.player()


    def voltar(self):

        if self.proxima != 'aleatorio':
            self.proxima = 'voltar'

        if self.tocando == True:
            self.parar()
        else:
            self.parar()
            self.player()


    def setvolume(self,valor):
        self.volume = valor
        pygame.mixer.music.set_volume(valor)



    def getvolume(self):
        return pygame.mixer.music.get_volume()


    def tocar_apartir(self,tempo):
        try:
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(tempo)

        except:
            return None





if __name__ == '__main__':
    pay = tocar()

    pay.musica_tocando = 4
    pay.player()




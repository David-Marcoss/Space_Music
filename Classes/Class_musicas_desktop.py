from pathlib import Path
from Classes.Class_musica import musica

class musicas_descktop():
    """
        - Ésta classe busca todos os arquivos de mp3
        do computador e os adiciona em um discionario
    """

    @staticmethod
    def busca_musicas():

        musicas = Path("/home")

        musicas = musicas.glob("**/*.mp3")

        musicas = [str(x) for x in musicas]

        return musicas

    @staticmethod
    def songs():

        mp3 = musicas_descktop.busca_musicas()

        lista = []

        for i in mp3:
            song = musica(i)

            if not musicas_descktop.busca_musica(lista,song):
                lista.append(song)



        return musicas_descktop.sort(lista)

    @staticmethod
    def busca_musica(lista,musica):

        for i in lista:

            if musica.titulo == i.titulo and musica.artista == i.artista:
                return True

        return False


    @staticmethod
    def sort(lista):

        for p in range(0, len(lista)):
            current_element = lista[p]

            while p > 0 and lista[p - 1].titulo > current_element.titulo:
                lista[p] = lista[p - 1]
                p -= 1

            lista[p] = current_element

        return lista


if __name__ == '__main__':

    mu = '/home/david-marcos/Downloads/4KTUBE/youtube/audio/castle-of-glass-official-music-video-linkin-park_audio_good.mp3'

    ms = musicas_descktop.songs()

    for i in ms:
        print(i.titulo)








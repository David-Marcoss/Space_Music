from tinytag import TinyTag


class musica:
    """
        - Ésta classe recebe o caminho de um arquivo mp3
        e extrai as informações importantes do arquivo

    """

    def __init__(self, mp3):

        file_ = TinyTag.get(mp3)

        self._musica = mp3

        self._titulo = self.formata_titulo(str(file_.title))
        self._artista = str(file_.artist)
        self._genero = str(file_.genre)
        self._album = str(file_.albumartist)
        self._duracao = int(file_.duration)
        self._ano = str(file_.year)

    def dados_mp3(self):

        print("Title:" + self.titulo)

        print("Artist:" + self.artista)

        print("Genre:" + self.genero)

        print("Year Released:" + self.ano)

        print("AlbumArtist:" + self.album)

        print("Duration:" + f"{self.duracao}" + " seconds")

    def formata_titulo(self,titulo):

        if titulo == "None":

            titulo = self.musica.split("/")
            titulo = titulo[-1].replace("mp3",'')


        return titulo

    @property
    def titulo(self):
        return self._titulo

    @property
    def artista(self):
        return self._artista

    @property
    def album(self):
        return self._album

    @property
    def ano(self):
        return self._ano

    @property
    def duracao(self):
        return self._duracao

    @property
    def genero(self):
        return self._genero

    @property
    def musica(self):
        return self._musica

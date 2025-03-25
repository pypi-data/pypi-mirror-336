"""
Este es el modulo que incluye la clase
de reproductor de música
"""


class Player:
    """
    Esta clase crea un reproductor
    de música
    """

    def play(self, song):
        """
        Reproduce la canción que recibió
        en el constructor

        Parm:
        song (str): este es un string con el path de la canción

        Out:
        int: devuelve 1 si reproduce con éxito, en caso de fracaso devuelve 0

        """
        print("Reproduciendo canción: " + song)

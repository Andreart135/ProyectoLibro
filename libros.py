from pathlib import Path
from string import punctuation
import nltk
from nltk.corpus import stopwords
class Libro:
    
    def __init__(self, name, filename) -> None:
        # Asignamos a través de las propiedades para activar las validaciones
        self.name = name
        self.filename = filename
        self.CARACTERES_ESPECIALES: str | None = None
        self.STOPWORDS: set[str] | None = None
        # hacer que estos atributos sean de tipo property (al setter hay que
        # incluirle validación)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """Checar que el nombre sea un string"""
        if not isinstance(value, str):
            raise TypeError("El nombre debe ser una cadena de texto.")
        self._name = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        """Checar que el nombre sea un string y que el archivo existe"""
        if not isinstance(value, str):
            raise TypeError("El nombre del archivo debe ser una cadena de texto.")
        if not Path(value).exists():
            raise FileNotFoundError(f"El archivo '{value}' no existe.")
        self._filename = value

    def _limpiar_linea(self, linea):
        """Este método toma una línea de texto (str) y elimina los caracteres
        en `self.CARACTERES_ESPECIALES`.

        """
        if self.CARACTERES_ESPECIALES:
            for caracter in self.CARACTERES_ESPECIALES:
                linea = linea.replace(caracter, "")
        return linea

    def _limpiar_tokens(self, tokens):
        """Este método recibe una lista de palabras (`tokens`) y elimina
        aquellas que se encuentran en `self.STOPWORDS` modificando la lista
        original. (regresa lista de palabras sin stopwords)

        """
        if self.STOPWORDS:
            # Modificamos la lista original usando asignación por rebanado [:]
            tokens[:] = [token for token in tokens if token not in self.STOPWORDS]
        return tokens

    def _preprocesar_linea(self, linea) -> list[str]:
        """Limpia una línea de texto regresando tokens  limpios. La limpieza
        debe considerar eliminar espacios blancos al principio y final de la
        línea, convertir a minúsculas, eliminar caracteres especiales, crear
        tokens y eliminar stopwords en estos tokens.

        Este método debe aplicar los métodos anteriores donde sea necesario.
        Debe regresar tokens limpios (lista de strings).

        """
        # eliminar espacios blancos al principio y final de la línea
        linea = linea.strip()

        # convierte la linea a minúsculas
        linea = linea.lower()

        # elimina los caracteres especiales
        linea = self._limpiar_linea(linea)

        # obten tokens: cada palabra debe aparecer como un elemento de una lista
        tokens = linea.split()

        # limpia la lista de tokens
        tokens = self._limpiar_tokens(tokens)
        
        return tokens

    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista, es decir, debe regresar una lista cuyos
        elementos son las líneas no vacías del libro (el primer elemento es la
        primer línea no vacía y así sucesivamente).

        """
        lineas_no_vacias = []
        with open(self.filename, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                if linea_limpia:
                    lineas_no_vacias.append(linea)
        return lineas_no_vacias

    def preprocesar_libro(self) -> dict[str, int]:
        """Regresa un diccionario de palabras relevantes del libro como llaves
        (los tokens limpios) y sus respectivas frecuencias como valores. Por
        ejemplo, puede regresar:
            {'shrek': 55, 'fiona': 43, 'caminando': 8}

        Para hacer esto, aplica `preprocesar_linea` a cada linea del `libro`
        agregando cada token limpio con un valor de 1 al diccionario si la
        palabra no existe o aumentado el contador de la palabra correspondiente
        en caso contrario.

        """
        frecuencias = {}
        lineas = self.leer_libro()
        for linea in lineas:
            tokens = self._preprocesar_linea(linea)
            for token in tokens:
                if token in frecuencias:
                    frecuencias[token] += 1
                else:
                    frecuencias[token] = 1
        return frecuencias

    def __str__(self) -> str:
        """Regresa la representación de este objeto en forma de un string.

        Esta es una representación informal que tiene como objetivo que el
        objeto sea entendible para el usuario cuando utilizamos `print` (esta
        función se ejecuta cuando utilizamos ese comando).

        Ver archivo: `Codes/clase_grupo.py` para un ejemplo.

        O bien puedes ver:
          https://realpython.com/python-classes/#special-methods-and-protocols

        """
        return f"Libro: {self.name} (Archivo: {self.filename})"

    def __repr__(self) -> str:
        """Regresa la representación formal del objeto.

        En esta función regresamos un string que tome la forma en la que
        creariamos esta instancia.

        Ver archivo: `Codes/clase_grupo.py` para un ejemplo.

        O bien puedes ver:
          https://realpython.com/python-classes/#special-methods-and-protocols

        """
        return f"{self.__class__.__name__}(name='{self.name}', filename='{self.filename}')"


# Los libros del proyecto Gutenberg empiezan dando información sobre el
# copyright y los créditos. El contenido se encuentra después de una línea que
# inicia con `*** START` y antes de la linea `*** END`. Esto debe
# considerarse al momento de leer el libro. Por lo tanto, reescribimos el
# método copprespondiente.
class LibroGutenberg(Libro):
    def leer_libro(self) -> list[str]:
        """Lee cada línea del libro en `self.filename`, agregando aquellas que
        no esten vacías a una lista. Además, empieza a agregar solo despues de
        la línea que comienza con `*** START` y antes de la línea `*** END`.

        (Debe regresar una lista cuyos elementos son las líneas no vacías del
        libro que se encuentran entre las líneas `*** START` y `*** END`.)

        """
        lineas_no_vacias = []
        dentro_del_contenido = False
        
        with open(self.filename, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                
                # Detectar el inicio del contenido
                if linea_limpia.startswith("*** START"):
                    dentro_del_contenido = True
                    continue
                
                # Detectar el fin del contenido
                if linea_limpia.startswith("*** END"):
                    break
                
                # Si estamos en la zona correcta del libro y la línea no está vacía, se guarda
                if dentro_del_contenido and linea_limpia:
                    lineas_no_vacias.append(linea)
                    
        return lineas_no_vacias


# Los libros en distintos idiomas tienen distintos `STOPWORDS`.
class LibroEnglish(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        try:
            self.STOPWORDS = set(nltk.corpus.stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            self.STOPWORDS = set(nltk.corpus.stopwords.words('english'))


class LibroSpanish(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        try:
            self.STOPWORDS = set(nltk.corpus.stopwords.words('spanish'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            self.STOPWORDS = set(nltk.corpus.stopwords.words('spanish'))


class LibroFrench(LibroGutenberg):
    def __init__(self, name, filename) -> None:
        super().__init__(name, filename)
        try:
            self.STOPWORDS = set(nltk.corpus.stopwords.words('french'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            self.STOPWORDS = set(nltk.corpus.stopwords.words('french'))


# La siguiente función asume que todos los libros se encuentran en el
# directorio `directory`, tienen extensión `txt` y todos son en inglés.
def crear_lista_libros_ingles(directory: str, caract_especiales=punctuation):
    """Crea una lista de instancias `LibroEnglish` a partir de libros
    localizados en `directory`.

    No ocupas modificar esta función, se encuentra ya implementada.

    """
    libros = []
    path = Path(directory)
    for file in path.glob('*.txt'):
        filename = str(file.relative_to(path.parent))
        libro = LibroEnglish(file.name, filename)
        libro.CARACTERES_ESPECIALES = caract_especiales
        libros.append(libro)
    return libros
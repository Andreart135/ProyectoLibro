import requests
import nltk

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt",     quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)


def get_links(n: int | list[int] = -1) -> tuple[ list[str], list[str] ]:
    """Obtiene los urls y los nombres de los libros del proyecto de Gutenberg
    deseados.

    Los libros se encuentran en formato txt bajo la sección descargados
    frecuentemente en:
        https://www.gutenberg.org/browse/scores/top.

    Los números `n` deben corresponder a los números en esta lista (empezando
    con uno).

    Parameters
    ----------
    n : int | list[int], optional
        Un entero o lista de enteros con los números de libros deseados.
        Escoge -1 (default) si se desean todos los libros.

    Returns
    -------
    links : list[str]
        Ligas a los archivos txt de los libros.
    titles : list[str]
        Títulos de los libros.
    """
    
    url = "https://www.gutenberg.org/browse/scores/top"
    try:
        response = requests.get(url)

        parser = BeautifulSoup(response.text, 'html.parser')

        header = parser.find("h2", string=lambda text: text and "Top 100 EBooks" in text)

        lista = header.find_next("ol")

        items = lista.find_all("li")

        all_links  = []
        all_titles = []

        for item in items:
            enlace = item.find("a")

            if enlace is None:
                continue

            titulo = enlace.get_text(strip=True)

            pagina_libro = "https://www.gutenberg.org" + enlace["href"]

            txt_url = _get_txt_url(pagina_libro)

            if txt_url is not None:
                all_links.append(txt_url)
                all_titles.append(titulo)

        
        if n == -1:
            links  = all_links
            titles = all_titles
        else:
            if isinstance(n, int):
                indices = [n]
            else:
                indices = list(n)

            links  = []
            titles = []
            for i in indices:
                if 1 <= i <= len(all_links):
                    links.append(all_links[i - 1])
                    titles.append(all_titles[i - 1])

        return links, titles

    except requests.exceptions.RequestException as e:
        print("wrong url for Gutenberg project")


def _get_txt_url(pagina_libro: str) -> str | None:
    """Entra a la página de un libro y busca el enlace directo al archivo .txt.

    Parameters
    ----------
    pagina_libro : str
        URL de la página descriptiva del libro en Gutenberg.

    Returns
    -------
    str | None
        URL del archivo .txt, o None si no se encontró.
    """
    try:
        respuesta = requests.get(pagina_libro, timeout=10)
        soup = BeautifulSoup(respuesta.text, "html.parser")

        for enlace in soup.find_all("a", href=True):
            href = enlace["href"]
        
            if href.endswith(".txt.utf-8") or href.endswith("-0.txt"):
                if href.startswith("http"):
                    return href
                else:
                    return "https://www.gutenberg.org" + href

    except requests.exceptions.RequestException:
        pass

    return None


def get_tokens(texto: str) -> list[str]:
    """Limpia el texto de un libro y lo convierte en una lista de tokens
    usando NLTK. Se eliminan stopwords, signos de puntuación y números.

    Parameters
    ----------
    texto : str
        Texto crudo del libro.

    Returns
    -------
    list[str]
        Lista de palabras relevantes (tokens) en minúsculas.
    """
    texto = texto.lower()

    palabras = word_tokenize(texto)

    palabras_vacias = set(stopwords.words("english"))

    tokens = []
    for palabra in palabras:
        if palabra.isalpha() and palabra not in palabras_vacias:
            tokens.append(palabra)

    return tokens


def download_file(url, name, directory):
    """Guarda un archivo que se encuentra en un `url` bajo el nombre que demos
    en `name` en el directorio deseado.
    """
    response = requests.get(url, stream=True)
    name = directory + name
    with open(name, mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):  #10kb chunks
            file.write(chunk)
    print(f"Downloaded file: {name}")

def store_files(links, names, directory='./'):
    """Guarda cada liga de la lista de ligas `links` en la computadora
    utilizando el directorio deseado y cada uno de los nombres en names.
    """
    for url, name in zip(links, names):
        download_file(url, name, directory)

def main(n = -1, directory='./'):
    links, titles = get_links(n)
    store_files(links, titles, directory)
    print("Done")

if __name__ == '__main__':
    directory = 'Books/'
    n = range(1, 6)
    main(n, directory)
import math

class Recomendador:
    def __init__(self, libros) -> None:
        """
        libros: lista con instancias de tipo `Libro`
        """
        self.libros = libros
        self._pesos = None  # Se calcularan con un setter (ver `set_pesos`)

    def set_pesos(self) -> None:
        """Calcula los pesos del algorítmo TF-IDF requeridos para las
        recomendaciones y los guarda en `self._pesos`.
        """
        N = len(self.libros)

        # Preprocesar todos los libros una sola vez
        frecuencias = [libro.preprocesar_libro() for libro in self.libros]

        # Calcular df (document frequency) para cada término
        df: dict[str, int] = {}
        for freq_dict in frecuencias:
            for palabra in freq_dict:
                df[palabra] = df.get(palabra, 0) + 1

        # Calcular TF-IDF para cada libro
        self._pesos = []
        for freq_dict in frecuencias:
            total_terminos = sum(freq_dict.values())
            tfidf: dict[str, float] = {}
            for palabra, count in freq_dict.items():
                tf = count / total_terminos
                idf = math.log(N / df[palabra])
                tfidf[palabra] = tf * idf
            self._pesos.append(tfidf)

    def get_pesos(self):
        """Regresa los pesos calculados"""
        return self._pesos

    def _producto_punto(self, idx_1: int, idx_2: int) -> float:
        """Producto punto entre los libros con índices idx_1 e idx_2."""
        vec1 = self._pesos[idx_1]
        vec2 = self._pesos[idx_2]
        # Iterar sobre el vector más pequeño para eficiencia
        if len(vec1) > len(vec2):
            vec1, vec2 = vec2, vec1
        return sum(peso * vec2.get(palabra, 0.0) for palabra, peso in vec1.items())

    def _similitud(self, idx_1, idx_2) -> float:
        """Similitud entre los libros con índices idx_1 e idx_2 de acuerdo al
        coseno del ángulo que forman sus vectores.

        similitud = (v1 · v2) / (||v1|| * ||v2||)
        """
        dot = self._producto_punto(idx_1, idx_2)
        norma1 = math.sqrt(self._producto_punto(idx_1, idx_1))
        norma2 = math.sqrt(self._producto_punto(idx_2, idx_2))
        if norma1 == 0 or norma2 == 0:
            return 0.0
        return dot / (norma1 * norma2)

    def mostrar_libros(self):
        """Mostrarle al usuario el índice y nombre para cada libro de acuerdo a
        nuestra lista de libros `self.libros`.
        """
        for idx, libro in enumerate(self.libros):
            print(f"[{idx}] {libro.name}")

    def resumen(self, idx_libro, num_palabras) -> list[str]:
        """Regresa una lista con las palabras más representativas de un libro
        de acuerdo a los pesos.

        idx_libro: índice del libro cuyo resumen deseamos.
        num_palabras: número de palabras en el resumen.
        """
        pesos_libro = self._pesos[idx_libro]
        palabras_ordenadas = sorted(pesos_libro, key=pesos_libro.get, reverse=True)
        return palabras_ordenadas[:num_palabras]

    def libros_similares(self, idx_libro, num_libros) -> list[str]:
        """Regresa una lista con los libros más parecidos a un libro dado.

        idx_libro: índice del libro a partir del cual quiero recomendaciones.
        num_libros: número de libros en mi recomendación.
        """
        similitudes = []
        for idx in range(len(self.libros)):
            if idx == idx_libro:
                continue
            sim = self._similitud(idx_libro, idx)
            similitudes.append((sim, idx))

        similitudes.sort(reverse=True)
        return [self.libros[idx].name for _, idx in similitudes[:num_libros]]
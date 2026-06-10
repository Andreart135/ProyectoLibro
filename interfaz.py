from libros import crear_lista_libros_ingles
from recomendaciones import Recomendador
from get_books import get_links, store_files

def pedir_indice_valido(total):
    while True:
        indice = input(" Ingresa el indice del libro: ")
        if indice.isdigit() and 0 <= int(indice) < total:
            return int(indice)
        print("indice invalido")


def pedir_entero_positivo(mensaje):
    while True:
        n = input(f"  {mensaje}: ").strip()
        if n.isdigit() and int(n) > 0:
            return int(n)
        print("ingresa un numero mayor a 0")


def main():
    print("𖹭" * 60)
    print("\n  ⁺‧₊˚RECOMENDACIONES DE LIBROS DE GUTENBERG˚₊‧⁺˖   \n")
    print("𖹭" * 60)
    print("Este programa analiza libros para darte resumenes ")
    print("o recomendarte libros similares basados en tus gustos \n")
    
    print("𖹭" * 60)
    print(" Ya tienes libros descargados o deseas descargarlos?\n")
    print(" ❥ [1] Ya tengo libros en un directorio")
    print(" ❥ [2] Descargar libros del Proyecto Gutenberg")
    descarga = input("Opcion: ").strip()

    if descarga == "2":
        directorio = input(" Directorio donde guardar los libros (ej: Books): ").strip()
        n_input = input(" ¿Cuántos libros descargar? (numero o 'todos'): ").strip()
        if n_input.lower() == "todos":
            n = -1
        elif n_input.isdigit():
            n = list(range(1, int(n_input) + 1))
        else:
            print(" Entrada inválida, se descargarán los primeros 5.")
            n = list(range(1, 6))
        print(" Descargando libros, espera un momento...")
        links, titles = get_links(n)
        store_files(links, [t + ".txt" for t in titles], directorio)
        print(" Descarga completada! ")
    else:
        directorio = input(" Ingresa la ruta al directorio con los libros: ").strip()
    print("𖹭" * 60)

    print("  Cargando libros...")
    libros = crear_lista_libros_ingles(directorio)

    if not libros:
        print(" No se encontraron archivos .txt en ese directorio.")
        return

    print(" Espera un momento ")
    recomendador = Recomendador(libros)
    recomendador.set_pesos()
    print(f" {len(libros)} libros cargados exitosamente.")

    print("𖹭" * 60)

    print("\n 𖹭 Que deseas hacer? 𖹭 \n")
    print("  ❥ [1] Ver libros disponibles")
    print("  ❥ [2] Ver resumen de un libro")
    print("  ❥ [3] Ver libros similares a uno dado")
    print("  ❥ [4] Salir")
    opcion = input("Opcion: ").strip()

    print("𖹭" * 60)

    if opcion == "1":
        print("𖦹" * 60)
        print("\n  ⋆｡‧˚ʚ LIBROS DISPONIBLES ɞ˚‧｡⋆  \n ")
        recomendador.mostrar_libros()

    elif opcion == "2":
        print("𖦹" * 60)
        print("\n  ⋆｡‧˚ʚ RESUMEN DE PALABRAS CLAVE ɞ˚‧｡⋆  \n ")
        print("Estos son los libros disponibles: ")
        recomendador.mostrar_libros()

        print()
        indice = pedir_indice_valido(len(libros))
        n = pedir_entero_positivo("Cuantas palabras clave deseas ver?")

        palabras = recomendador.resumen(indice, n)
        libro = libros[indice]

        print("𖦹" * 60)
        print(f"  Palabras más representativas de ʚ{libro.name}ɞ:\n")
        for i, palabra in enumerate(palabras, 1):
            print(f"    {i:>2}. {palabra}")

    elif opcion == "3":
        print("𖦹" * 60)
        print("\n ⋆｡‧˚ʚ RECOMENDACIONES DE LIBROS ɞ˚‧｡⋆ \n ")
        print(" Estos son los libros disponibles: ")
        recomendador.mostrar_libros()

        print()
        indice = pedir_indice_valido(len(libros))
        n = pedir_entero_positivo("¿Cuántos libros quieres que te recomendemos?")

        similares = recomendador.libros_similares(indice, n)
        libro = libros[indice]

        print("𖹭" * 60)
        print(f"  Como te gustó «{libro.name}», te recomendamos:\n")
        for i, nombre in enumerate(similares, 1):
            print(f"  {i}. {nombre}")

    elif opcion == "4":
        print("Hasta pronto!! ٩(ˊᗜˋ*)و ")
        return

    else:
        print("Esa opcion no es valida ˙◠˙")
        return

    print("𖹭" * 60)
    print("Gracias por usar este programa ( ˘͈ ᵕ ˘͈♡)")


if __name__ == "__main__":
    main()
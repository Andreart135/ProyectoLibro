from libros import crear_lista_libros_ingles
from recomendaciones import Recomendador


def separador():
    print("\n" + "=" * 50 + "\n")


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
    print("o recomendarte libros similares basados en tus gustos.\n")
    
    print("𖹭" * 60)
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

    separador()
    print("  ¿Qué deseas hacer?\n")
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
        n = pedir_entero_positivo("¿Cuántas palabras clave deseas ver?")

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
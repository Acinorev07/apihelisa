def dividir_texto(texto, limite):
    if texto is None:
        return []

    texto = str(texto)

    fragmentos = []

    for i in range(0, len(texto),limite):

        fragmento = texto[i:i + limite]
        fragmentos.append(fragmento)

        return fragmentos[0]

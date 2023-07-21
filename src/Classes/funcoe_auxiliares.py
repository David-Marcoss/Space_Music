

def formata_tempo(tempo):
    m = tempo // 60
    s = tempo % 60

    if m >= 60:
        h = m // 60
        m = m % 60

        tempo = f'{h}:{m}:{s}'

    else:
        tempo = f'{m}:{s}'

    tempo = tempo.split(':')
    tempof = ''

    for i in range(0, len(tempo)):
        if len(tempo[i]) < 2:
            tempo[i] = '0' + tempo[i]

        tempof += tempo[i]

        if i < len(tempo) - 1:
            tempof += ':'

    return tempof

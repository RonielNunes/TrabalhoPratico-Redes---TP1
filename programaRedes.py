import random
import statistics


def slottedAloha(N):
    maquinasRestantes = N #maqinas que falta enviar
    slots = 100 # pode esprar até mil slots de 51,2u segundos para enviar
    timePrimeiroEnvio = 1 #começa com um pois tem colisão no primeiro slots de tempo
    timeEnvioTotalMedio = 1 #começa com um pois tem colisão no primeiro slots de tempo
    teste = 0

    while( maquinasRestantes > 0 ):

        #Criando o n slots para cada um enviar
        vetorSlots = []
        for i in range(maquinasRestantes):
            vetorSlots.append(random.randint(1,slots))

        #ordena o vetor crescente
        vetorSlots.sort()

        #verifica se tem colisao (tempos iguais)
        if len(set(vetorSlots)) == len(vetorSlots):
            if(maquinasRestantes == N):
                timePrimeiroEnvio = vetorSlots[0]
            maquinasRestantes = 0
            for i in range(len(vetorSlots)):
                timeEnvioTotalMedio +=vetorSlots[i] #sem repetição
        else:
            vetorAux = []
            count = 0  #tem maquinas com slots repetidos
            for i in range(len(vetorSlots)):
                for j in range(len(vetorSlots)):
                    if ((vetorSlots[i]) == (vetorSlots[j])):
                        count +=1

                if (count == 1):
                    vetorAux.append(i) #armazena a posição nos indices de slots que n se tem colisão
                    timeEnvioTotalMedio +=vetorSlots[i] #faz o somatorio do tempo dos slots sem colisão
                count = 0
            if(maquinasRestantes == N and len(vetorAux) != 0):
                for i in range(len(vetorSlots)):
                    if(vetorAux[0] == i):
                        timePrimeiroEnvio += vetorSlots[i]

            maquinasRestantes = maquinasRestantes - len(vetorAux)



    vetorResultado = [timePrimeiroEnvio*51.2,timeEnvioTotalMedio*51.2]
    return vetorResultado

def csma(N):
    #Considerando que houve colisão, o csma calculará um tempo de espera para todas as maquinas.
    totalElementos = N
    slots = 100
    timeEnvioTotalMedio = 1
    timePrimeiroEnvio = 1
    vetorResultado = []


    while (totalElementos > 0):
        vetorSlots = []
        for i in range(totalElementos):
            q = slots - (random.randint(1,slots))
            vetorSlots.append(q)
        vetorSlots.sort()
        #verifica se o canal tá ocupado
        #caso que n tá ocupado
        if len(set(vetorSlots)) == len(vetorSlots):
            for i in range(len(vetorSlots)):
                timeEnvioTotalMedio +=vetorSlots[i]
            if (len(vetorSlots) == N):
                timePrimeiroEnvio = vetorSlots[0]
                break
            totalElementos = 0
        else:#ta ocupado
            #Quais que estão ocupados
            vetorPosica = []
            for i in range(totalElementos):
                count = 0
                for j in range(totalElementos):
                    if (vetorSlots[i] == vetorSlots[j]):
                        count +=1
                if count > 1:
                    vetorPosica.append(i) #guarda a posicao dos elementos que devem ser sorteados novamnete
                else:
                    if (len(vetorSlots) == N):
                        timePrimeiroEnvio = vetorSlots[0]
                    timeEnvioTotalMedio +=vetorSlots[i]


            totalElementos -= (len(vetorSlots) - len(vetorPosica))



    vetorResultado.append(timePrimeiroEnvio*51.2)
    vetorResultado.append(timeEnvioTotalMedio*51.2)
    return vetorResultado

def backoff(N): #limite de tentativas
    i = 1 #formula (0,2^i - 1)
    timeEnvioTotalMedio = 1
    timePrimeiroEnvio = 1
    estacoes = N
    slots = 100
    vetorResultado = []
    while(estacoes > 0 and i < 16):
        vetorSlots = []

        for i in range(estacoes):
            vetorSlots.append(random.randint(0,slots))
        vetorSlots.sort()
        #verificando se tivemos colisao entre as estações
        if len(set(vetorSlots)) == len(vetorSlots):
            for i in range(len(vetorSlots)):
                timeEnvioTotalMedio +=vetorSlots[i]
            if (len(vetorSlots) == N):
                timePrimeiroEnvio = vetorSlots[0]
                break
            estacoes = 0
        else:
            #tivemos colisao
            vetorPosica = []

            #indentifica quias estações se colidiram
            for i in range(estacoes):
                count = 0
                for j in range(estacoes):
                    if (vetorSlots[i] == vetorSlots[j]):
                        count +=1
                if count > 1:
                    vetorPosica.append(i) #guarda a posição de colisão
                else:
                    if (len(vetorSlots) == N):
                        timePrimeiroEnvio = vetorSlots[0] #guarda o primeiro tempo da estação que enviou
                    timeEnvioTotalMedio +=vetorSlots[i]   #guarda o tempo das estações que eviamos

            estacoes -= (len(vetorSlots) - len(vetorPosica))
            slots = (2**i) - 1
            i +=1

    if (i == 16):
        print("tempo maximo atigindo")
        vetorResultado.append(0)
        vetorResultado.append(0)
        return  vetorResultado
    else:
        vetorResultado.append(timePrimeiroEnvio*51.2)
        vetorResultado.append(timeEnvioTotalMedio*51.2)
        return  vetorResultado


if __name__ == '__main__':
    N = 100 #Numero de estamos que vamo tentar transmitir
    print("Numero de estacoes(N):",N)

    vetorAlohaPrimeiro = []
    vetorAlohaTotal = []

    vetorCsmaPrimeiro = []
    vetorCsmaTotal = []

    vetorBackoffPrimeiro = []
    vetorBackoffTotal = []

    for i in range(33):
        vetorAlohaResultado = slottedAloha(N)
        vetorAlohaPrimeiro.append(vetorAlohaResultado[0])
        vetorAlohaTotal.append(vetorAlohaResultado[1])

        vetorCsmaResultado = csma(N)
        vetorCsmaPrimeiro.append(vetorCsmaResultado[0])
        vetorCsmaTotal.append(vetorCsmaResultado[1])


        vetorBackoffResultado = backoff(N)
        vetorBackoffPrimeiro.append(vetorBackoffResultado[0])
        vetorBackoffTotal.append(vetorBackoffResultado[1])

    print("**************************ALOHA**************************")
    print('Tempo do primeiro envio: ',statistics.mean(vetorAlohaPrimeiro))
    print('Desvio padrao do tempo do primeiro envio: ',statistics.pstdev(vetorAlohaPrimeiro))
    print('Tempo envio medio Total: ',statistics.mean(vetorAlohaTotal))
    print('Desvio padrao do tempo de envio medio Total: ',statistics.pstdev(vetorAlohaTotal))

    print("**************************CSMA**************************")
    print('Tempo do primeiro envio: ',statistics.mean(vetorCsmaPrimeiro))
    print('Desvio padrao do tempo do primeiro envio: ',statistics.pstdev(vetorCsmaPrimeiro))
    print('Tempo envio medio Total: ',statistics.mean(vetorCsmaTotal))
    print('Desvio padrao do tempo de envio medio Total: ',statistics.pstdev(vetorCsmaTotal))

    print("**************************BACKOFF**************************")
    print('Tempo do primeiro envio: ',statistics.mean(vetorBackoffPrimeiro))
    print('Desvio padrao do tempo do primeiro envio: ',statistics.pstdev(vetorBackoffPrimeiro))
    print('Tempo envio medio Total: ',statistics.mean(vetorBackoffTotal))
    print('Desvio padrao do tempo de envio medio Total: ',statistics.pstdev(vetorBackoffTotal))

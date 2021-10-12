import numpy.random as rand
import math
import numpy as np
import matplotlib.pyplot as plt
G_arreglo = []
G_i = 0
for i in range(14):
    G_i = 0.10 + G_i
    G_arreglo.append(G_i)
    print( G_arreglo[i])
simulado = []
teorico = []
for G_ in range(len(G_arreglo)):
    
    N = 7# NUMERO DE USUARIOS
    #lmda = 5 # paquetes /s
    T = 1.6e-3 # tiempo de trama
    idle = 0
    tx= 1
    backoff= 2

    tx_exitoso = [0]*N
    Edos = [0]*N
    Paq = [0]*N
    C = [0]*N
    T_espera = [0]*N
    S = [0]*N # trafico cursado con exito

    #G = lmda * T * N #trafico del sistema
    G = G_arreglo[G_]
    lmda = G/(T*N)
    Pnp = 1 - math.exp(-lmda*T) # probabilidad de nuevo paquete
    t_sim = 0; # tiempo inicial de simulacion
    t_fin = 1000; # tiempo final de simulacion


    def t_backoff(C):
        Cw = 16 # tiempo ax generado, no exceder
        if C < 4:        
            sal = rand.randint(2**C)#np.power(2,C)
            
        else:       
            sal = rand.randint(Cw)
        return sal
        

    while t_sim< t_fin:
        #atender backoff
        for n in range(N):
            if Edos[n] is backoff: 
                if T_espera[n] > 0:
                    T_espera[n] -=1
                else:
                    Edos[n] = tx
        #Atender tx
        col = 0
        for n in range(N):
            if Edos[n] is tx:
                col +=1
        for n in range(N):
            if Edos[n] is tx:
                if col<2:
                    Paq[n] -= 1
                    tx_exitoso[n] += 1
                    C[n] = 0
                else:
                    Edos[n] = backoff
                    C[n] +=1
                    T_espera[n] = t_backoff(C[n])

        for n in range(N):
            p = rand.random()
            if p <=Pnp and (Edos[n] is idle):
                Paq[n] +=1
                Edos[n] = tx
            if Paq[n] == 0:
                Edos[n] = idle
        #Actualizar t sim
        t_sim += T
    #Calculo de metricas    
    for n in range(N):
        S[n] = tx_exitoso[n]* T / t_sim
        
    S_general=np.sum(S)
    print(f"Tasa de paquetes tx con exito simulado: {S_general}")

    S_teo = G * math.exp(-G)
    print(f"Tasa de paquetes tx con exito teorico: {S_teo}")
    print(f"Trafico ofrecido {G}")
    simulado.append(S_general)
    teorico.append(S_teo)
    
plt.plot(G_arreglo, simulado, 'bo-', label='Tasa de paquetes simulado')
plt.plot(G_arreglo, teorico, 'r--', label='Tasa de paquetes teorica')
plt.legend(framealpha=1, frameon=True);
plt.xlabel('Trafico ofrecido')
plt.ylabel('Tasa de paquetes')
plt.title('Tasa de paquetes Transmitidos con exito')
plt.show()
    
        


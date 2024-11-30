from dataclasses import dataclass
import numpy as np # type: ignore

@dataclass
class matriz :
    matrizI : list
    a : int

    def inserevalor (self):
        print(self.matrizI)
        for i in range (0,self.a):
         for j in range(0,self.a):
            self.matrizI[i][j] = input('digite o número de linhas e colunos da matriz quadrada(limite de 7): ')
            print(i,j,"\n")
        print(self.matrizI)
        if np.linalg.det(self.matrizI) == 0 :
          print('Matriz singular detectada! determinante = 0! impossivel calcular! tente novamente')
          self.inserevalor() 
        
    def LU (self):
        u = np.zeros((len(self.matrizI[0]), len(self.matrizI[0])))
        l = np.eye((len(self.matrizI[0])))
        print("matriz U inicial:","\n")
        print(u,"\n")
        print("matriz L inicial:","\n")
        print(l,"\n")
        u[0] = self.matrizI[0]
        print("matriz U com valores de A:","\n")
        print(u,"\n")
        n = len(self.matrizI[0])
        for i in range(n):
        # Calcula os elementos da matriz U
         for j in range(i, n):
            u[i] [j] = self.matrizI[i] [j] - sum(l[i] [k] * u[k] [j] for k in range(i))
        # Calcula os elementos da matriz L
         for j in range(i + 1, n):
            l[j] [i] = (self.matrizI[j] [i] - sum(l[j] [k] * u[k] [i] for k in range(i))) / u[i] [i]
        print("matriz U:","\n")
        print(u,"\n")
        print("matriz L:","\n")
        print(l,"\n")


    
        

def criamatriz ():
    x = int(input('digite o número de linhas e colunos da matriz quadrada(limite de 7): '))
    matrizi = matriz(matrizI = np.zeros((x,x)), a = x)
    matrizi.inserevalor()
    matrizi.LU()
criamatriz()
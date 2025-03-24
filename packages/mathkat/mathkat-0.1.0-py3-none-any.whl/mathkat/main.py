import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate



class Funcion:
    def __init__(self,f,grad_f,x_0,v_0,alpha,iteraciones,epsilon,eta):
        self.f = f
        self.grad_f = grad_f
        self.x_0 = x_0
        self.v_0 = v_0
        self.alpha = alpha
        self.iteraciones = iteraciones
        self.epsilon = epsilon
        self.eta = eta
        self.x_historico = [x_0]
        self.headers = ["Iteración", "x", "Norma"]
        self.data_grad_simple = []
        self.data_grad_momentum = []

    
    def imprimir_tabla_tabulate(self,data, headers):
        """
        Imprime una tabla formateada usando la librería tabulate.

        :param headers: Lista con los nombres de las columnas.
        :param data: Lista de filas, donde cada fila es una lista o tupla de valores.
        """
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    def desenso_gradiente_simple(self):
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        lr = self.alpha
        max_iters = self.iteraciones
        epsilon = self.epsilon
        x_historico = [x0]
        
        for i in range(max_iters):
            f_i = f(*x0)
            grad_f_i = grad_f(*x0)
            nomra_grad = np.linalg.norm(grad_f_i)
            if nomra_grad < epsilon: # Criterio de paro 
                break
            xi = x0 - lr * grad_f_i
            x0 = xi.copy()
            x_historico.append(x0)
            self.data_grad_simple.append((i+1, x0.tolist(), nomra_grad))
            
        self.imprimir_tabla_tabulate(self.data_grad_simple, self.headers)
        return x_historico


    def desenso_gradiente_momentum(self):
        f = self.f
        grad_f = self.grad_f
        x0 = self.x_0
        v0 = self.v_0
        lr = self.alpha
        eta = self.eta
        max_iters = self.iteraciones
        epsilon = self.epsilon
        x_historico = [x0]
        
        for i in range(max_iters):
            f_i = f(*x0)
            grad_f_i = grad_f(*x0)
            nomra_grad = np.linalg.norm(grad_f_i)
            if nomra_grad < epsilon: # Criterio de paro 
                break
            vi = eta * v0 + lr * grad_f_i
            xi = x0 - vi
            x0 = xi.copy()
            v0 = vi.copy()
            x_historico.append(x0)
            self.data_grad_momentum.append((i+1, x0.tolist(), nomra_grad, vi.tolist()))
            
        self.imprimir_tabla_tabulate(self.data_grad_momentum, ["Iteración", "x", "Norma", "velocidad"])
        return x_historico
        

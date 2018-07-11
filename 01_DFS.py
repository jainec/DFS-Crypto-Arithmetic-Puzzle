# -*- coding: utf-8 -*-

import itertools
from random import randint
import collections
import time


#####################CÓDIGO HERDADO DAS CODIFICAÇÕES DISPONÍVEIS PELA DISCIPLINA####################

class Problem(object):
    
    def __init__(self, initial):
        self.initial = estado_inicial(initial)
    
    def goal_test(self, equacao, list_chars, estado):
        return is_goal(equacao, list_chars, estado)
    
    def actions(self, nivel, frontier, node, primeiras_letras, list_chars):
        gerar_filhos(nivel, frontier, node, primeiras_letras, list_chars)
  

def tree_search(problem, frontier, list_chars, primeiras_letras):
    nosExpandidos = 0
    frontier.append((problem.initial, 0))    
    while frontier:
        node = frontier.pop()
        nosExpandidos = nosExpandidos + 1
        if problem.goal_test(equacao, list_chars, node[0]):
            imprime_no_objetivo(list_chars, node, nosExpandidos)
            return True
        if tem_null(node[0]):     
            problem.actions(node[1], frontier, node, primeiras_letras, list_chars)        
    return False


def depth_first_tree_search(problem, frontier, list_chars, primeiras_letras):
    return tree_search(problem, frontier, list_chars, primeiras_letras)


##############################FUNÇÕES AUXILIARES################################

#Função que recebe uma equação de strings da forma X1 + X2 + ... + Xn = R
#e retorna uma lista com as letras das strings.
def trata_equacao(equacao):
    list_chars = []
    for char in equacao:
        if(char.isalpha()):
            list_chars.append(char)
    list_chars = list(set(list_chars))    #remove duplicate letters
    return list_chars

#Função que recebe uma lista de tamanho N
#e retorna outra lista com tamanho N e todos elementos iguais a -1
def estado_inicial(lista):
    estado = []
    for i in lista:
        estado.append(-1)
    return estado         

#Função que recebe uma lista de caracteres
#e retorna True se todos os elementos dessa lista são diferentes
def diferentes(lista_chars):
    lista = list(filter(lambda x: x != -1, lista_chars))
    list_chars = sorted(set(lista), key=lambda x: lista.index(x))
    if lista == list_chars:
        return True
    return False

#Função que retorna True se um determinado estado é estado goal do problema
def is_goal(equacao, list_chars, estado):
    if -1 in estado:
        return False
    termos = []
    termos_soma = []
    resultadoSoma = ""
    list_digitos = ",".join(str(i) for i in estado)
    list_digitos = list_digitos.split(",")
    
    #separating terms of sum and result
    aux = ""
    for c in equacao:
        if c.isalpha():
            aux = aux + c
        if c == '+':
            termos.append(aux)
            aux = ""
        if c == '=':
            termos.append(aux)
            aux = ""
    resultadoSoma = aux
    aux = ""

    for c in resultadoSoma:
        index = list_chars.index(c)
        aux = aux + list_digitos[index]
    res = aux
    aux = ""

    for elem in termos:
        for c in elem:
            index = list_chars.index(c)
            aux = aux + list_digitos[index]
        termos_soma.append(aux)
        aux = ""

    for i, val in enumerate(termos_soma):
        val = int(val)
        termos_soma[i] = val

    res = int(res)
   
    soma = 0
    for i in termos_soma:
        soma = soma + i
  
    if abs(soma) == res:
        return True
    else:
        return False
    
#Função que retorna True se alguma das primeiras letras
#das string da equação receberma valor 0 (zero)
def zero_primeiras_letras(list_chars, primeiras_letras, estado):
    for elem in primeiras_letras:
        index = list_chars.index(elem)
        if estado[index] == 0:
            return True
    return False
        
               
def gerar_filhos(nivel, frontier, node, primeiras_letras, list_chars):                
    for i in range(0,10):    
        list_aux = []
        c = 0
        nv = nivel
        for j in node[0]:
            if c == nivel:
                list_aux.append(i)
            else:
                list_aux.append(j)
            c = c + 1
        nv = nv + 1
        if nv >= len(node[0]):
            nv = len(node[0]) - 1
        if diferentes(list_aux) and not zero_primeiras_letras(list_chars, primeiras_letras, node[0]):
            frontier.append((list_aux, nv))
            
#Função que retorna True se algum elemento 
#de uma lista possui valor -1 (nulo)
def tem_null(lista):
    if -1 in lista:
        return True
    return False

#Função que retornas as primeiras letras das
#palavras da equação
def get_primeiras_letras(equacao):
    equacao = equacao.replace(" ", "")
    primeiras_letras = []
    flag = False
    for i, elem in enumerate(equacao):
        if i == 0:
            primeiras_letras.append(elem)
        if flag == True:
            primeiras_letras.append(elem)
            flag = False
        if elem == '+' or elem == '=':
            flag = True
    return primeiras_letras
        
        
def imprime_no_objetivo (list_chars, node, iteracoes): 
    for elem in list_chars:
        index = list_chars.index(elem)
        print(elem + " = " +str(node[0][index]))
    print("Numero de nos expandidos: "+str(iteracoes))


################################## MAIN ###################################
   
if __name__ == "__main__":
    start_time = time.time()
    equacao = "AB + CD = DE"       #inserir aqui a equação que quiser testar
    lista_chars = trata_equacao(equacao)
    problem = Problem(lista_chars)
    print("Para a entrada: " + equacao)
    primeiras_letras = get_primeiras_letras(equacao)
    frontier = []
    depth_first_tree_search(problem, frontier, lista_chars, primeiras_letras)
    print("--- %s seconds ---" % (time.time() - start_time))
    

    
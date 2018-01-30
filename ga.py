#!/usr/bin/env python3
#coding: utf-8

"""
Autor: Ricardo Henrique Remes de Lima <https://rhrlima.github.io/>

Arquivo que descreve um Algoritmo Genético.
"""

import random

problema = None				#Problema a ser resolvido
melhor_fitness = None		#Melhor fitness encontrado global

TAM_POPULACAO = 50			#Quantidade de solucoes criadas
MAX_AVALIACOES = 5000		#Quantidade de avalicoes
T_CROSS = 0.8				#Taxa de cruzamento
T_MUT = 0.3					#Tava de mutacao


class Cromossomo:

	def __init__(self, genes, fitness):
		self.genes = genes
		self.fitness = fitness

	def __str__(self):
		return str(self.fitness)

	def copy(self):
		return Cromossomo(self.genes[:], self.fitness)


def criar_populacao():

	return [Cromossomo(problema.criar_solucao(), -1) for i in range(TAM_POPULACAO)]


def avaliar_populacao(populacao):
	for solucao in populacao:
		avaliar_solucao(solucao)


def avaliar_solucao(solucao):
	global melhor_fitness, melhorou
	solucao.fitness = problema.avaliar_solucao(solucao.genes)
	if melhor_fitness is None or solucao.fitness < melhor_fitness.fitness:
		melhor_fitness = solucao.copy()
		melhorou = True
	else:
		melhorou = False


def selecao(populacao):
	p1 = random.randint(0, len(populacao)-1)
	while True:
		p2 = random.randint(0, len(populacao)-1)
		if p1 != p2:
			break
	return [populacao[p1], populacao[p2]]


def cruzamento(pais):
	if random.uniform(0,1) < T_CROSS:
		filho = []
		corte = random.randint(0, len(pais[0].genes)-1)
		filho.extend(pais[0].genes[:corte])
		filho.extend(pais[1].genes[corte:])
		return Cromossomo(filho, -1)
	return pais[0].copy()


def mutacao(solucao):
	if random.uniform(0,1) < T_MUT:
		solucao.genes = problema.mutacao(solucao.genes)


def reproducao(pais):
	filho = cruzamento(pais)
	mutacao(filho)
	return filho


def reparar(solucao):
	
	solucao.genes = problema.reparar(solucao.genes)


def substituicao(filho, populacao):
	populacao.sort(key=lambda f: f.fitness, reverse=True)
	if filho.fitness < populacao[0].fitness:
		populacao[0] = filho.copy()


def iniciar_processo():
	global avaliacoes
	avaliacoes = TAM_POPULACAO


def atualizar_processo():
	global avaliacoes
	if melhorou:
		avaliacoes = 0
	else:
		avaliacoes += 1


def criterio_parada():

	return avaliacoes < MAX_AVALIACOES


def executar():
	populacao = criar_populacao()
	[reparar(solucao) for solucao in populacao]
	avaliar_populacao(populacao)
	iniciar_processo()
	while(criterio_parada()):
		pais = selecao(populacao)
		filho = reproducao(pais)
		reparar(filho)
		avaliar_solucao(filho)
		substituicao(filho, populacao)
		atualizar_processo()
	populacao.sort(key = lambda f : f.fitness)
	return populacao[0].copy()

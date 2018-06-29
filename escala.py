#!/usr/bin/env python3
#coding: utf-8

"""
Autor: Ricardo Henrique Remes de Lima <https://rhrlima.github.io/>

Arquivo que descreve o Problema da Escala de Portarias.
"""

import math
import re
import random

TURNOS = 4			#Número de Turnos por dia

dias_mes = []		#Lista de dias da escala
candidatos = []		#Lista de candidatos à escala


class Candidato:

	def __init__(self, id, nome, pos):
		self.id = id
		self.nome = nome.lower()
		self.num_possibilidades = pos
		self.num_portarias = 0

	def __str__(self):
		return "{0}\t{1}".format(self.id, self.nome)


class DiaEscala:

	def __init__(self, dia, turnos):
		self.dia = dia
		self.turnos = turnos

	def __str__(self):
		return self.dia


def analisar_turnos(dias, dados):
	turnos = {}
	cont = 0
	for i, dia in enumerate(dias):
		aux = re.findall("(?<=Turno #)[0-9]+", dados[i])
		if aux:
			cont += 1
		turnos[dia.dia] = aux
	return cont, turnos


def ler_escala(arquivo):
	try:
		global dias_mes, candidatos
		dias_mes = []
		candidatos = []
		arquivo_escala = open(arquivo, encoding='utf-8')
		dados = arquivo_escala.readline().split("\t")[4:]
		for dia in dados:
			dia_escala = DiaEscala(int(dia.replace(" ","")[-2:]), [[],[],[],[]])
			dias_mes.append(dia_escala)
		for linha in arquivo_escala:
			aux = linha.split("\t")
			cont, aux2 = analisar_turnos( dias_mes, aux[4:] )
			c = Candidato(-1, aux[2], cont)
			for d in dias_mes:
				for turno in aux2[d.dia]:
					d.turnos[int(turno)-1].append(c)
			candidatos.append(c)
		dias_mes.sort(key = lambda dia: dia.dia)
		candidatos.sort(key = lambda candidato: candidato.nome)
		for i, candidato in enumerate(candidatos):
			candidato.id = i
		return True
	except ValueError as e:
		print(e)
		return False


def ler_escala_de_solucao(arquivo):
	try:
		moradores = {}

		dados = open(arquivo, encoding='utf-8')
		for _ in range(5): #ler apenas 5 linhas (dia, e turnos)
			colunas = dados.readline().replace('\n', '').split('\t')
			if _ != 0:
				for c in colunas:
					if c != '':
						if c not in moradores.keys(): moradores.append(c)

		moradores.sort()
		for i, m in enumerate(moradores):
			print(i+1, m)

		return True
	except ValueError as e:
		print(e)
		return False


def criar_solucao():
	solution = []
	for dia in dias_mes:
		for t in range(TURNOS):
			solution.append(dia.turnos[t][random.randint(0, len(dia.turnos[t])-1)].id)
	return solution


def mutacao(solucao):
	rand = random.randint(0, len(solucao)-1)
	dia = rand // TURNOS
	turno = rand % TURNOS
	novo_valor = random.randint(0, len(dias_mes[dia].turnos[turno])-1)
	solucao[rand] = dias_mes[dia].turnos[turno][novo_valor].id
	return solucao[:]


def atualizar_num_portarias(solucao):
	for c in candidatos:
		c.num_portarias = 0
	for indice in solucao:
		candidatos[indice].num_portarias += 1


def avaliar_solucao(solucao):
	media_turnos_pessoas = len(solucao) // len(candidatos)
	atualizar_num_portarias(solucao)
	aux = 0
	for c in candidatos:
		if c.num_possibilidades >= media_turnos_pessoas:
			aux += (c.num_portarias - media_turnos_pessoas)**2
		else:
			aux += (c.num_portarias - c.num_possibilidades)**2
	return aux / len(candidatos)


def validar_candidato(candidato, indice, solucao):
	#verifica se o candidato possui dois turnos no período de 48hrs
	#dias = (-7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7)
	#verifica se o candidato possui dois turnos no período de 24hrs
	dias = (-3, -2, -1, 1, 2, 3)
	for doff in dias:
		aux_dia = indice + doff
		if aux_dia >= 0 and aux_dia < len(solucao) and solucao[aux_dia] == candidato.id:
			return False
	#verifica se o candidate possui número de portarias acima da média
	media_turnos_pessoas = math.ceil( len(solucao) / len(candidatos) )
	if candidato.num_portarias > media_turnos_pessoas:
		return False
	return True


def reparar(solucao):
	atualizar_num_portarias(solucao)
	min_portarias = 99
	for c in candidatos:
		if c.num_portarias < min_portarias:
			min_portarias = c.num_portarias
	for indice, id in enumerate(solucao):
		valido = validar_candidato(candidatos[id], indice, solucao)
		if not valido: 
			aux_candidatos = dias_mes[indice // TURNOS].turnos[indice % TURNOS][:]
			aux_candidatos.sort(key = lambda p: p.num_portarias)
			candidatos[id].num_portarias -= 1
			aux_candidatos[0].num_portarias += 1
			solucao[indice] = aux_candidatos[0].id
	return solucao[:]
			

def validar_escala(solucao):
	valido = True
	atualizar_num_portarias(solucao)
	temp_cont = [0] * len(candidatos)
	for indice, id in enumerate(solucao):
		temp_cont[id] += 1
		valido = validar_candidato(candidatos[id], indice, solucao)
		if not candidatos[id] in dias_mes[id // TURNOS].turnos[id % TURNOS]:
			valido = False
	for indice, candidato in enumerate(candidatos):
		if candidato.num_portarias != temp_cont[indice]:
			valido = False
	return valido


def exportar(solucao, nome_arquivo):
	try:
		data = [[], [], [], [], []]
		for i, dia in enumerate(dias_mes):
			data[0].append(dia.dia)
			for turno in range(TURNOS):
				data[turno+1].append(candidatos[solucao[i * TURNOS + turno]].nome)
		arquivo_saida = open(nome_arquivo, "w", encoding='utf-8')
		for i in range(len(data)):
			line = ""
			for j in range(len(data[0])):
				line += "{0}\t".format(data[i][j])
			arquivo_saida.write("{0}\n".format(line))
		arquivo_saida.write("\n")
		for i, c in enumerate(candidatos):
			line = "{0}\t=COUNTIF(A$2:AE$5;A{1})\t=CONT.SE(A$2:AE$5;A{1})\n".format(c.nome, i+7)
			arquivo_saida.write(line)
		arquivo_saida.write("\nMin\t=MIN(B{0}:B{1})\t=MÍNIMO(C{0}:C{1})".format(7, i+7))
		arquivo_saida.write("\nMax\t=MAX(B{0}:B{1})\t=MÁXIMO(C{0}:C{1})".format(7, i+7))
		arquivo_saida.write("\n")
		arquivo_saida.write("\n")
		for i in range(10):
			arquivo_saida.write("{0}\t=COUNTIF(B${1}:C${2};A{3})\t=CONT.SE(B${1}:C${2};A{3})\n".format(i, 7, len(candidatos)+7, len(candidatos)+i+11))
		arquivo_saida.close()
		return True
	except:
		return False
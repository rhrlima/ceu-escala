#!/usr/bin/env python3
#coding: utf-8

"""
Autor: Ricardo Henrique Remes de Lima <https://rhrlima.github.io/>

Arquivo principal que executa o Algoritmo Genético para o Problema da Escala de Portarias.
"""

import escala
import ga
import os.path
import sys

MIN_SOLUCOES = 10	#Número mínimo de execuções

def executar(arquivo, rodadas=1):

	nome_aux = arquivo.split('.')[0]
	print("Arquivo carregado: {0}".format(nome_aux))

	for rodada in range(rodadas):

		print("Execução {0}/{1}".format(rodada+1, rodadas))

		escala.ler_escala(arquivo)
		ga.problema = escala

		contador = 0
		melhor = None
		valido = False
		while contador < MIN_SOLUCOES or not valido:
			solucao = ga.executar()
			solucao_aval = escala.validar_escala(solucao.genes)
			print('.', end='')
			if solucao_aval:
				if solucao.fitness == 0.0:
					melhor = solucao
					break
				if (melhor is None or solucao.fitness < melhor.fitness):
					melhor = solucao.copy()
				valido = True
				contador += 1
				print('')
			sys.stdout.flush()
		print('')

		sucesso = escala.exportar(melhor.genes, "{0}_saida_{1}.csv".format(nome_aux, rodada))
		if sucesso:
			print("Melhor solução válida encontrada com fitness {0}".format(melhor))
			print("Exportado para \"{0}_saida_{1}.csv\"".format(nome_aux, rodada))
		else:
			print("Ocorreu um erro ao exportar para o arquivo \"{0}_saida_{1}.csv\"".format(nome_aux, rodada))


if __name__ == "__main__":

	tamanho = len(sys.argv)

	if tamanho == 1:
		print("Gerador de Escala CEU")
		print("Parâmetros:")
		print("gerador_escala.py <arquivo> <rodadas>")
		print("<arquivo>	Nome do arquivo csv ou tsv que contém os dados do formulário")
		print("		filtrado.")
		print("<rodadas>	Quantidade de escalas que serão geradas. Padrão é 1.")
		sys.exit()

	elif tamanho > 3:
		print("Número incorreto de parâmetros.")
		sys.exit()

	else:
		arquivo = sys.argv[1]

		if not os.path.exists(arquivo):
			print("O arquivo \"{0}\" não existe.".format(arquivo))
			sys.exit()
		
		if arquivo[:2] == '.\\': #remove o './' que o power shell inclui no nome dos arquivos 
			arquivo = arquivo[2:]

		extensao = arquivo[arquivo.rfind('.')+1:]
		
		if extensao != 'tsv' and extensao != 'csv':
			print("Formato de arquivo incorreto: {0}".format(arquivo))
			sys.exit()

		if tamanho == 2:
			executar(arquivo)
		else:
			executar(arquivo, int(sys.argv[2]))
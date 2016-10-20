# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def separa_elementos(tag):
    contador = 0
    #Gambiarra para separar os elemetos por topicos. aux=1 -> data; aux=2 -> regime
    aux = 0
    for elemento in tag:
        if aux == 1:
            print "Datonha: " + str(elemento)
            aux = 0
        if aux == 2:
            print "Regimonha: " + str(elemento)
            aux = 0
        if aux == 3:
            print "Quórumonha: " + str(elemento)
            aux = 0
        if aux == 4:
            print "Situaçãozonha: " + str(elemento)
        if aux == 5:
            print "Protocolonha: " + str(elemento)
        if aux == 6:
            print "Remetentonha: " + str(elemento)
        if aux == 7:
            print "Sequencionha: " + str(elemento)
        if aux == 8:
            print "Destinatárionha: " + str(elemento)
        if aux == 9:
            print "Envionha: " + str(elemento)
        if aux == 10:
            print "Objetivonha: " + str(elemento)
            aux = 0
        print str(elemento) + str(contador)
        if str(elemento)==("Data: "):
            aux = 1
        if str(elemento)==("Regime: "):
            aux = 2
        if str(elemento)==("Quórum: "):
            aux = 3
        if str(elemento)==("Situação: "):
            aux = 4
        if str(elemento)==("Protocolo: "):
            aux = 5
        if str(elemento)==("Remetente: "):
            aux = 6
        if str(elemento)==("<strong>Sequência:</strong>"):
            aux = 7
        if str(elemento)==("Destinatário: "):
            aux = 8
        if str(elemento)==("Envio: "):
            aux = 9
        if str(elemento)==("Objetivo: "):
            aux = 10
        contador+=1


def pega_total(aux):
    total = aux
    return total

class CrawlerAmericanas:
    def __init__(self, discount_wanted):
        self.root_url = 'http://consulta.siscam.com.br/'
        self.initial_products = 1
        self.response_msg = []
        self.discount = discount_wanted
        self.pages_to_crawl = [
            ('http://consulta.siscam.com.br/camaraitu/Documentos/Documento/{0}', 'notes')
        ]

    def begin_crawl(self):
        total = 0;
        for page in self.pages_to_crawl:
            while True:
                try:
                    if page[0].find('{0}'):
                        page_url = page[0].format(self.initial_products)
                    else:
                        page_url = page[0]
                    req = requests.get(page_url)
                except :
                    self.response_msg.append("erro ao buscar url " + str(page[0]))
                    print "erro no link" + page[0]
                    continue
                else:
                    print "searching page: " + page_url
                soup = BeautifulSoup(req.text, "html.parser")
                products = soup.find_all("div", {'id': 'main'})
                if len(products) == 0:
                    break
                for product in products:
                    nome = product.find('h2')
                    print "Nome: " + str(nome)

                    #Data, Protocolo, Regime e Situacao
                    data_situacao = product.findAll("div", {'class': 'box'})
                    for elementos in data_situacao:
                        separa_elementos(elementos)

                    #Autoria e Assunto
                    autoria_assunto = product.findAll('div', {'class': 'text-justify'})
                    for elementos in autoria_assunto:
                        print elementos

                    print "\n"
                    # preco_cheio = product.find('del')
                    # if preco_cheio is None:
                    #     continue
                    # produto_nome = product.find('a', {'class': 'prodTitle'})['title']
                    # produto_url = product.find('a', {'class': 'prodTitle'})['href']


                if page[0] == page_url:
                    break
                self.initial_products += 1
            self.initial_products = 0
        print "Achei " + str(total) + " itens."
        return self.response_msg
if __name__ == '__main__':
    americanas_bot = CrawlerAmericanas(30)
    print str(americanas_bot.begin_crawl())

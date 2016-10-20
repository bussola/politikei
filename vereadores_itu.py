# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def separa_elementos(tag):
    aux = 0
    for elem in tag:
        if aux == 1:
            nome = str(elem)
            nome = nome.split("<b>")
            nome = str(nome[1])
            nome = nome.replace("</b>", "")
            nome = nome.replace("</div>", "")
            nome = nome.replace("\n", "")
            print "Nome: " + str(nome)
        if aux == 3:
            partido = str(elem)
            partido = partido.split("</div>")
            partido = str(partido[0])
            partido = partido.split(" ")
            partido = partido[1]
            print "Partido: " + str(partido)
        if aux == 5:
            email = str(elem)
            email = email.split("<b>")
            if len(email)>1:
                email = email[1]
                email = email.split("</b>")
                email = email[0]
                print "Email: " + str(email)
            print "\n"
        aux+=1

def pega_total(aux):
    total = aux
    return total

class CrawlerAmericanas:
    def __init__(self, discount_wanted):
        self.root_url = 'http://consulta.siscam.com.br/'
        self.initial_products = 17085
        self.response_msg = []
        self.discount = discount_wanted
        self.pages_to_crawl = [
            ('http://consulta.siscam.com.br/camaraitu/vereadores', 'vereadores')
        ]

    def begin_crawl(self):
        total = 0;
        for page in self.pages_to_crawl:
            while True:
                try:
                    page_url = page[0]
                    req = requests.get(page_url)
                except :
                    self.response_msg.append("erro ao buscar url " + str(page[0]))
                    print "erro no link" + page[0]
                    continue
                else:
                    print "searching page: " + page_url
                soup = BeautifulSoup(req.text, "html.parser")
                products = soup.find_all("div", {'class': 'container'})
                if len(products) == 0:
                    break
                for product in products:
                    # Nome do vereador
                    # nome0 = product.findAll('b')
                    # for element in nome0:
                    #     print "Nome0: " + str(element)
                    nome1 = product.findAll("div", {'class': 'vereador-info'})
                    for element in nome1:
                        separa_elementos(element)

                    # #Data, Protocolo, Regime e Situacao
                    # data_situacao = product.findAll("div", {'class': 'box'})
                    # for elementos in data_situacao:
                    #     separa_elementos(elementos)
                    #
                    # #Autoria e Assunto
                    # autoria_assunto = product.findAll('div', {'class': 'text-justify'})
                    # for elementos in autoria_assunto:
                    #     print elementos

                    # preco_cheio = product.find('del')
                    # if preco_cheio is None:
                    #     continue
                    # produto_nome = product.find('a', {'class': 'prodTitle'})['title']
                    # produto_url = product.find('a', {'class': 'prodTitle'})['href']


                if page[0] == page_url:
                    break
                self.initial_products += 1
            self.initial_products = 0
        return self.response_msg
if __name__ == '__main__':
    americanas_bot = CrawlerAmericanas(30)
    print str(americanas_bot.begin_crawl())

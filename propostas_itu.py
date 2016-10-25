# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
import psycopg2 #Biblioteca do PostgreSQL
reload(sys)
sys.setdefaultencoding('utf8')

nomeTag = ""
dataTag = ""
protocoloTag = ""
situacaoTag = ""
assuntoTag = ""
autoriaTag = ""
ids = 1

def separa_autor(tag):
    global autoriaTag
    global assuntoTag
    aux = 0
    for elemento in tag:
        if aux == 1:
            autoria = str(elemento)
            autoriaTag = str(autoria)
            print "Autoria: " + autoriaTag
            aux = 0
        if aux == 2:
            assunto = str(elemento)
            assuntoTag = str(assunto)
            print "Assunto: " + assuntoTag
            aux = 0
        if str(elemento)==("<strong>Autoria:</strong>"):
            aux = 1
        if str(elemento)==("<strong>Assunto:</strong>"):
            aux = 2

def separa_elementos(tag):
    global dataTag
    contador = 0
    #Gambiarra para separar os elemetos por topicos. aux=1 -> data; aux=2 -> regime
    aux = 0
    for elemento in tag:
        if aux == 1:
            elemento = str(elemento)
            elemento = elemento.split("<b>")
            elemento = str(elemento[1])
            elemento = elemento.replace("</b>", "")
            dataTag = elemento
            print "Data: " + dataTag
            aux = 0
        if aux == 2:
            elemento = str(elemento)
            elemento = elemento.split("<b>")
            elemento = str(elemento[1])
            elemento = elemento.replace("</b>", "")
            print "Regime: " + elemento
            aux = 0
        if aux == 3:
            elemento = str(elemento)
            elemento = elemento.split("<b>")
            elemento = str(elemento[1])
            elemento = elemento.replace("</b>", "")
            print "Quórum: " + str(elemento)
            aux = 0
        if aux == 4:
            elemento = str(elemento)
            elemento = elemento.split("<b>")
            elemento = str(elemento[1])
            elemento = elemento.replace("</b>", "")
            situacaoTag = elemento
            print "Situação: " + situacaoTag
        if aux == 5:
            elemento = str(elemento)
            elemento = elemento.split("<b>")
            elemento = str(elemento[1])
            elemento = elemento.replace("</b>", "")
            protocoloTag = elemento
            print "Protocolo: " + protocoloTag
        if aux == 6:
            elemento = str(elemento)
            elemento = elemento.split(">")
            elemento = elemento[1]
            elemento = elemento.replace("</strong", "")
            print "Remetente: " + elemento
        if aux == 7:
            print "Sequencia: " + str(elemento)
        if aux == 8:
            print "Destinatárionha: " + str(elemento)
        if aux == 9:
            print "Envionha: " + str(elemento)
        if aux == 10:
            print "Objetivonha: " + str(elemento)
            aux = 0
        # print str(elemento) + str(contador)
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

class CrawlerPropostas:
    conn = ""
    # Se conecta ao Banco de dados
    try:
        conn = psycopg2.connect(
            "dbname='dbvereador' user='postgres' host='localhost' port=5433 password='vereador'")
        cur = conn.cursor()
        cur.execute('DELETE FROM "propostas" ') #Deleta toda a tabela existente
        conn.commit()
        print "Tabela deletada"
    except:
        print("I am unable to delete to the database")

    def __init__(self, discount_wanted):
        self.root_url = 'http://consulta.siscam.com.br/'
        self.initial_products = 14980
        self.response_msg = []
        self.discount = discount_wanted
        self.pages_to_crawl = [
            ('http://consulta.siscam.com.br/camaraitu/Documentos/Documento/{0}', 'notes')
        ]

    def begin_crawl(self):
        total = 0;
        global ids
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
                    print "erro no link: " + page[0]
                    continue
                else:
                    print "searching page: " + page_url
                soup = BeautifulSoup(req.text, "html.parser")
                products = soup.find_all("div", {'id': 'main'})
                if len(products) == 0:
                    pass
                for product in products:
                    nome = product.find('h2')
                    nome = str(nome)
                    nome = nome.split("<h2>")
                    nome = str(nome[1])
                    nome = nome.replace("</h2>", "")
                    nome = nome.replace("</span>", "")
                    nomeTag = str(nome)
                    print "Nome: " + nomeTag

                    #Data, Protocolo, Regime e Situacao
                    data_situacao = product.findAll("div", {'class': 'box'})
                    for elementos in data_situacao:
                        separa_elementos(elementos)

                    #Autoria e Assunto
                    autoria_assunto = product.findAll('div', {'class': 'text-justify'})
                    for elementos in autoria_assunto:
                        separa_autor(elementos)

                    print "A inserir: " + nomeTag + "**" + dataTag + "**" + autoriaTag + "**" + assuntoTag

                    #Se conecta ao Banco de dados
                    try:
                        conn = psycopg2.connect("dbname='dbvereador' user='postgres' host='localhost' port=5433 password='vereador'")
                        cur = conn.cursor()
                        print "conectou"
                    except:
                        print("I am unable to connect to the database")

                    # Preenche o Banco de Dados
                    try:
                        cur.execute('INSERT INTO "propostas" (nome, data, autoria, assunto, ids) '
                                    'VALUES (%s, %s, %s, %s, %s)', (nomeTag, dataTag, autoriaTag, assuntoTag, ids))
                        conn.commit()
                        print "Inserindo na tabela: " + nomeTag + " ** " + dataTag + " ** " + autoriaTag + " ** " + assuntoTag + "\n"
                        ids += 1
                    except psycopg2.Error as e:
                        print "Unable to connect!"
                        print e.pgerror
                        print e.diag.message_detail

                if page[0] == page_url:
                    break
                self.initial_products += 1
            self.initial_products = 0
        print "Achei " + str(total) + " itens."
        return self.response_msg
if __name__ == '__main__':
    propostas_bot = CrawlerPropostas(1)
    print str(propostas_bot.begin_crawl())

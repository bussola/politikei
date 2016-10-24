# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import psycopg2 #Biblioteca do PostgreSQL
import sys
reload(sys)
sys.setdefaultencoding('utf8')

total = 0
def separa_elementos(tag):
<<<<<<< HEAD
    conn = ""
=======
>>>>>>> f5812ec52d4de6f1a327dbcf97124bbb67f76017
    nomeTag = ""
    partidoTag = ""
    emailTag = ""

    #Se conecta ao Banco de dados
    try:
<<<<<<< HEAD
        conn = psycopg2.connect("dbname='dbvereador' user='postgres' host='localhost' port=5433 password='vereador'")
        cur = conn.cursor()
    except:
        print("I am unable to connect to the database")
=======
        conn = psycopg2.connect("dbname='dbvereador' user='postgres' host='localhost' port=5432 password='vereador'")
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
>>>>>>> f5812ec52d4de6f1a327dbcf97124bbb67f76017
    # cur.execute('DELETE FROM "tabela" ') #Deleta toda a tabela existente

    aux = 0
    global total
    print "Vereador " + str(total+1)
    for elem in tag:
        if aux == 1:
            total += 1
            nome = str(elem)
            nome = nome.split("<b>")
            nome = str(nome[1])
            nome = nome.replace("</b>", "")
            nome = nome.replace("</div>", "")
            nome = nome.replace("\n", "")
            nomeTag = nome
            print "Nome: " + str(nomeTag)

        if aux == 3:
            partido = str(elem)
            partido = partido.split("</div>")
            partido = str(partido[0])
            partido = partido.split(" ")
            partido = partido[1]
            partidoTag = partido
            print "Partido: " + str(partidoTag)
        if aux == 5:
            email = str(elem)
            email = email.split("<b>")
            if len(email)>1:
                email = email[1]
                email = email.split("</b>")
                email = email[0]
                emailTag = email
                print "Email: " + str(emailTag)

            # Preenche o Banco de Dados
<<<<<<< HEAD
            try:
                cur.execute('INSERT INTO "tabela" (nome, partido, email, id) '
                            'VALUES (%s, %s, %s, %s)', (nomeTag, str(partidoTag), str(emailTag), total))
                conn.commit()
                print "Inserindo: " + str(total) + str(nomeTag) + str(partidoTag) + str(emailTag)
                print "\n"
            except:
                print "faio"
=======
            cur.execute('INSERT INTO "tabela" (nome, partido, email, id) '
                        'VALUES (%s, %s, %s, %s)', (nomeTag, str(partidoTag), str(emailTag), total))
            print "Inserindo: " + str(total) + str(nomeTag) + str(partidoTag) + str(emailTag)
            print "\n"
            conn.commit()
>>>>>>> f5812ec52d4de6f1a327dbcf97124bbb67f76017
        aux+=1

class CrawlerVereadores:
    conn = ""
    def __init__(self, discount_wanted):
        self.root_url = 'http://consulta.siscam.com.br/'
        self.initial_products = 17085
        self.response_msg = []
        self.discount = discount_wanted
        self.pages_to_crawl = [
            ('http://consulta.siscam.com.br/camaraitu/vereadores', 'vereadores')
        ]

    # Se conecta ao Banco de dados
    try:
        conn = psycopg2.connect(
<<<<<<< HEAD
            "dbname='dbvereador' user='postgres' host='localhost' port=5433 password='vereador'")
        cur = conn.cursor()
        cur.execute('DELETE FROM "tabela" ') #Deleta toda a tabela existente
        conn.commit()
        print "Tabela deletada"
    except:
        print("I am unable to delete to the database")
=======
            "dbname='dbvereador' user='postgres' host='localhost' port=5432 password='vereador'")
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
    cur.execute('DELETE FROM "tabela" ') #Deleta toda a tabela existente
    conn.commit()
>>>>>>> f5812ec52d4de6f1a327dbcf97124bbb67f76017

    def begin_crawl(self):
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
                    nome1 = product.findAll("div", {'class': 'vereador-info'})
                    for element in nome1:
                        separa_elementos(element)
                if page[0] == page_url:
                    break
                self.initial_products += 1
            self.initial_products = 0
        return self.response_msg
if __name__ == '__main__':
    vereadores_bot = CrawlerVereadores(1)
    print str(vereadores_bot.begin_crawl())

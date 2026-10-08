import requests
import hashlib

class HashNode:
    def __init__(self, nome, dados):
        self.nome = nome
        self.dados = dados
        self.next = None
    def add_node(self, nome, dados):
        no_ponteiro = self
        while no_ponteiro.next != None:
            no_ponteiro = no_ponteiro.next
        no_ponteiro.next = HashNode(nome, dados)
        

class HashTable:
    def __init__(self):
        self.size = 64
        self.num_corpos = 0
        self.tabela = [None] * self.size
        self.colisoes = 0
    
    def calcula_hash(self, nome_planeta):
        return abs(hash(nome_planeta)) % self.size
    
    def dobra_tamanho(self):
        tabela_antiga = self.tabela
        
        self.size *= 2
        
        self.tabela = [None] * self.size
        
        self.num_corpos = 0
        self.colisoes = 0
        
        for item in tabela_antiga:
            if item is not None:
                self.add_corpo(item.nome, item.dados)
                pointer = item.next
                while pointer != None:
                    self.add_corpo(pointer.nome, pointer.dados)
                    pointer = pointer.next
    
    def add_corpo(self, nome, dados):
        fator_carga = self.num_corpos / self.size
        if fator_carga >= 0.5:
            self.dobra_tamanho()
        self.num_corpos += 1
        indice = self.calcula_hash(nome)
        if self.tabela[indice] == None:
            self.tabela[indice] = HashNode(nome, dados)
        else:
            self.colisoes += 1
            self.tabela[indice].add_node(nome, dados)
    def procura_corpo(self, nome):
        indice = self.calcula_hash(nome)
        if ( self.tabela[indice] == None ):
            return
        else:
            corpo = self.tabela[indice]
            while corpo != None:
                if ( corpo.nome == nome ):
                    return corpo.dados
                corpo = corpo.next
            return
        

url = "https://api.le-systeme-solaire.net/rest/bodies/"

headers = {
    "Authorization":"Bearer 151ebbcc-8737-402d-9b7d-23fb3abdffb8"
}

response = requests.get(url, headers=headers)

tabela = HashTable()

if response.status_code == 200:

    dados = response.json()
    
    lista_de_corpos = dados.get("bodies", [])
    
    for corpo in lista_de_corpos:
        tabela.add_corpo(corpo.get("englishName"), corpo)
    
    busca = input("Digite o nome do corpo celeste em inglês: ")
    busca = tabela.procura_corpo(busca)
    if ( busca != None ):
        print(f"Nome: {busca.get("englishName")}")
        print(f"Massa: {busca.get("mass")}")
        print(f"Volume: {busca.get("vol")}")
        if ( busca.get("moons") != None ):
             for lua in busca.get("moons"):
                print(f"{lua}")
    print(f"Colisões -> {tabela.colisoes}")
    print(f"Fator de carga -> {tabela.num_corpos/tabela.size}")
    print(f"Tamanho -> {tabela.size}")
    print(f"Número de corpos -> {tabela.num_corpos}")
else:
    # Caso a URL esteja errada ou o servidor fora do ar
    print(f"Erro na requisição. Código: {response.status_code}")
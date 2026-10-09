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

def montaString(corpo_celeste):
    partes = []
    partes.append(f"Nome: {corpo_celeste.get('englishName')}")
 
    massa = corpo_celeste.get("mass") or {}
    partes.append(
        f"Massa: {massa.get('massValue')}"
    )
 
    volume = corpo_celeste.get("vol") or {}
    partes.append(
        f"Volume: {volume.get('volValue')}"
    )
 
    luas = corpo_celeste.get("moons")
    if luas:
        nomes_luas = ", ".join(lua.get("moon", "") for lua in luas)
        partes.append(f"Luas: {nomes_luas}")
    else:
        partes.append("Luas: sem luas")
 
    return "\n".join(partes)
 

class Huffman_node:
    def __init__(self, char, freq, left, right):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

def contaFrequencia (string, frequencia, nodesArr):
    for chares in string:
        if chares in frequencia:
            frequencia[chares] += 1
        else:
            new = Huffman_node(None, None, None, None)
            nodesArr.append(new)
            frequencia[chares] = 1

def pegaInt(item):
    return item[1]

def ordenaDecrescente(dicionario):
    itensOrdenados = sorted(
        dicionario.items(),
        key=pegaInt,
        reverse=True
    )
    return dict(itensOrdenados)

def reordena(nodesArr):
    i = len(nodesArr) - 2
    n = len(nodesArr) - 1

    while i >= 0 and nodesArr[n].freq > nodesArr[i].freq:
        m = nodesArr[n]
        nodesArr[n] = nodesArr[i]
        nodesArr[i] = m
        i = i - 1
        n = n - 1

    return


def monta_arvore(freqDict, nodesArr):
    n = 0

    for i in freqDict:
        nodesArr[n].char = i
        nodesArr[n].freq = freqDict[i]
        n = n + 1

    for i in range(len(nodesArr)):
        print(f"{nodesArr[i].char}: {freqDict[nodesArr[i].char]}")

    while len(nodesArr) > 1:
        new = Huffman_node(None, nodesArr[len(nodesArr) - 1].freq + nodesArr[len(nodesArr) - 2].freq, nodesArr[len(nodesArr) - 1], nodesArr[len(nodesArr) - 2])
        nodesArr.pop()
        nodesArr.pop()
        nodesArr.append(new)
        reordena(nodesArr)

    return nodesArr[0]

def geraCodigo(no, caminho, codigos):
    if no == None:
        return
    elif no.char != None:
        if caminho:
            codigos[no.char] = caminho
        else:
            codigos[no.char] = "0"
        return
    geraCodigo(no.left, caminho + "0", codigos)
    geraCodigo(no.right, caminho + "1", codigos)


url = "https://api.le-systeme-solaire.net/rest/bodies/"

headers = {
    "Authorization":"Bearer 151ebbcc-8737-402d-9b7d-23fb3abdffb8"
}

response = requests.get(url, headers=headers)

tabela = HashTable()

if response.status_code == 200:

    dados = response.json()
    
    lista_de_corpos = dados.get("bodies", [])

    freq = {}
    nodesArr = []
    for corpo in lista_de_corpos:
        string = montaString ( corpo )
        contaFrequencia ( string, freq, nodesArr )
        tabela.add_corpo(corpo.get("englishName"), corpo)

    freqDict = ordenaDecrescente(freq)
    arvore = monta_arvore(freqDict, nodesArr)

    busca = input("Digite o nome do corpo celeste em inglês: ")
    busca = tabela.procura_corpo(busca)
    while (busca != None):
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

            corpoCodificado = {}
            geraCodigo ( arvore,"", corpoCodificado )
            print(corpoCodificado)

            busca = input("Digite o nome do corpo celeste em inglês: ")
            busca = tabela.procura_corpo(busca)
        else:
            # Caso a URL esteja errada ou o servidor fora do ar
            print(f"Erro na requisição. Código: {response.status_code}")
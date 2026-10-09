import requests

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
                    return corpo
                corpo = corpo.next
            return

def calcula_compressao(texto_bruto, codigo_huffman, vetor_caracteres):
    total_caracteres = len(texto_bruto)
    bits_originais = total_caracteres * 8
    
    bits_comprimidos = 0
    for no in vetor_caracteres:
        caractere = no.nome
        frequencia = no.dados
        tamanho_codigo = len(codigo_huffman[caractere])
        bits_comprimidos += frequencia * tamanho_codigo
        
    porcentagem_economia = bits_originais / bits_comprimidos
    print(f"A economia foi de : {porcentagem_economia:.2f}x")
    
    
 

class Huffman_node:
    def __init__(self, char, freq, left, right):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        
def transforma_em_vetor(hash):
    vetor = []
    for item in hash.tabela:
        if item != None:
            vetor.append(item)
            pointer = item.next
            while pointer != None:
                vetor.append(pointer)
                pointer = pointer.next
    return vetor
        

def contaFrequencia (string, hash, nodesArr):
    for chares in string:
        char = hash.procura_corpo(chares)
        if char != None:
            char.dados += 1
        else:
            new = Huffman_node(None, None, None, None)
            nodesArr.append(new)
            hash.add_corpo(chares, 1)

def pegaInt(item):
    return item.dados

def ordenaDecrescente(vetor):  
    vetor = sorted(
        vetor,
        key=pegaInt,
        reverse=True
    )
    return vetor

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
        nodesArr[n].char = i.nome
        nodesArr[n].freq = i.dados
        n = n + 1

    for i in range(len(nodesArr)):
        print(f"{nodesArr[i].char}: {nodesArr[i].freq}")

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

    nodesArr = []
    for corpo in lista_de_corpos:
        tabela.add_corpo(corpo.get('englishName'), corpo)
        
    hash_caracteres = HashTable()

    contaFrequencia(response.text, hash_caracteres, nodesArr)
    
    vetor_caracteres = transforma_em_vetor(hash_caracteres)
    
    freqDict = ordenaDecrescente(vetor_caracteres)
    arvore = monta_arvore(freqDict, nodesArr)
                
    corpoCodificado = {}
    geraCodigo ( arvore,"", corpoCodificado )
    print(corpoCodificado)
    calcula_compressao(response.text, corpoCodificado, vetor_caracteres)

    busca = input("Digite o nome do corpo celeste em inglês: ")
    busca = tabela.procura_corpo(busca)
    while (busca != None):
        print(f"Nome: {busca.dados.get('englishName')}")
        print(f"Massa: {busca.dados.get("mass")}")
        print(f"Volume: {busca.dados.get("vol")}")
        if ( busca.dados.get("moons") != None ):
            for lua in busca.dados.get("moons"):
                print(f"{lua}")

        print(f"Colisões -> {tabela.colisoes}")
        print(f"Fator de carga -> {tabela.num_corpos/tabela.size}")
        print(f"Tamanho -> {tabela.size}")
        print(f"Número de corpos -> {tabela.num_corpos}")

        busca = input("Digite o nome do corpo celeste em inglês: ")
        busca = tabela.procura_corpo(busca)
        print("")
else:
            # Caso a URL esteja errada ou o servidor fora do ar
            print(f"Erro na requisição. Código: {response.status_code}")
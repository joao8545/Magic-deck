import csv
import requests
from bs4 import BeautifulSoup as Soup
import sys
import os

'''
TODO
separa deck do side
usar diretorios feito
fazer uma saida geral e uma saida para cada

any(key.startswith("Brazen") for key in col)
next( (key for key in col if key.startswith("Brazen")), None )

'''

col={}
deck={}
deck2={}
want=dict()
have=dict()
needs=[]
custos=[]
arqCol='hungria.csv'
arqDeck='deck.txt'
arqdeck='deck2.txt'
lands=["Island",'Swamp','Plains','Mountain','Forest','Planície','Montanha','Ilha','Floresta','Pântano']

#soup=''
def main():
    '''
    destino=open("decklist2.txt",'w')
    
    sys.stdout=destino
    '''
    ler_dados_colecao(arqCol)

    for txt in os.listdir():
        if txt.endswith(".txt"):
            nome=txt[:-4]
            print(nome)
            ler_dados_deck_arena(txt)
            calcular_cartas()
            limpar()

 
    
    '''
    print("Novo")
    ler_dados_deck_arena('simic food.txt')
    calcular_cartas()
    limpar()


    '''

    print("\nForam analizados %3.3d decks\no minimo de cartas para montar um deles é %2.2d cartas"%(len(needs),min(needs)))
    print("O mais barato custa %5.2f reais para ser completado"%min(custos))
    print('------------------------------------------------\n')
    #sys.stdout = sys.__stdout__
    #destino.close()
    #print('acabou')
    
def limpar():
    deck.clear()
    deck2.clear()
    want.clear()
    have.clear()
    
def emArquivo():
    pass


def procura(nome):
    ler_dados_deck_arena(nome+'.txt')
    calcular_cartas()
        

def ler_dados_colecao(arq):
    with open(arq) as csvfile:
        colecao=csv.reader(csvfile,quotechar="'")
        
        itercol=iter(colecao)
        next(itercol)
        for carta in itercol:
            cartaEN=''.join(carta[5].split("'"))
            if carta[4] not in col or cartaEN not in col:
                col[carta[4]]=int(carta[6])
                col[cartaEN]=int(carta[6])
            else:
                col[carta[4]]+=int(carta[6])
                col[cartaEN]+=int(carta[6])

            
    


def ler_dados_deck(arq1):
    with open(arq1) as arq:
        col1=arq.readlines()
        aux=1
        len1=len(col1)
        for carta in col1:
            if aux==len1:
                if carta[2:] not in deck:
                    deck[carta[2:]]=int(carta[0])                  
                else:
                    deck[carta[2:]]+=int(carta[0])
            else:
                if carta[0]=='\n':
                    aux+=1
                    continue
                if carta[2:-1] not in deck:
                    deck[carta[2:-1]]=int(carta[0])
                else:
                    deck[carta[2:-1]]+=int(carta[0])
                aux+=1

def ler_dados_deck_arena(arq1):
    with open(arq1) as arq:
        col1=arq.readlines()
        for carta in col1:
           
            if carta[0]=='\n':
                continue
            carta2=" ".join(carta.split(' ')[1:]).split(" (")[0]
            #print(carta2)
           # print(" ".join(carta.split(' ')[1:]).split("(")[0])
            if carta2 not in deck:
                deck[carta2]=int(carta[0])
            else:
                deck[carta2]+=int(carta[0])
    

def calcular_cartas():
    for carta in deck :
        if carta in lands:
            continue
        
        cartaEN=''.join(carta.split("'"))
        if cartaEN in col:
            deck2[carta]=deck[carta]-col[cartaEN]
        elif any(key.startswith(cartaEN) for key in col):
            cartaEN=next( (key for key in col if key.startswith(cartaEN)), None )
            #print(cartaEN)
            
            deck2[carta]=deck[carta]-col[cartaEN]
        else:
            deck2[carta]=deck[carta]

    for carta in deck2:
        cartaEN=''.join(carta.split("'"))
        cartaEN=next( (key for key in col if key.startswith(cartaEN)), None )
        
       
        try:
            
            have[carta]=min(deck[carta],col[cartaEN])
        except:
           
            pass
        finally:
            if deck2[carta]>0:
                want[carta]=deck2[carta]
    need=0
    custo=0
    for card in want:
        need+=want[card]
        
        custo+=(procurarPreco(card)*want[card])
        #print(custo)
    needs.append(need)
    custos.append(custo)
    print("\nPara esse deck faltam %2.2d cartas com o custo de %6.2f\n"%(needs[-1],custos[-1]))
    imprimirTudo(need)
    
    
            
def imprimirTudo(need):
    #print("\nprecisa de %3.3d"%need)
    print("\nO deck:\n")
    imprimir(deck)
    print("\n\nPreciso:\n")
    imprimir(want)
    print("\n\nTenho:\n")
    imprimir(have)
    print()

def imprimir(dic):
    for el in dic:
        print(el,":",dic[el])
def procurarPreco(carta):
    #global soup
    ps=[]
    pagina="https://www.ligamagic.com.br/?view=cards/card&card="
    link="".join((pagina,"%20".join(carta.split(" "))))
    #print(link)
    r=myRequest(link,"erro na carta "+carta)
    soup=Soup(r.text,"html.parser")
    r.close()
    for pr in soup.find_all("font",{'class':'bigger'}):
        ps.append(float(pr.text.replace(".","").replace(",",".")))
        #print(ps)
    if len(ps)==0:
        for pr in soup.find_all("td",{'class':'col-4 preMen'}):
                ps.append(float(pr.text.split('\xa0')[0][3:].replace(".","").replace(",",".")))
                #print(ps)
    try:
        #print("aqui")
        preco=min(ps)
    except:
        
        a=sys.stdout
        sys.stdout = sys.__stdout__
        print(carta)
        sys.stdout = a
    
    #preco=float(soup.find("div",{'id':'mobile-precos-menor'}).text[3:].strip(".").replace(",","."))
    #print(preco)
    return preco


def myRequest(url,erro):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
    while True:
            try:
                r=requests.get(url,headers=headers)
            except Exception:
                a=sys.stdout
                sys.stdout = sys.__stdout__
                print("\a\n\n\n\n",erro,"\n\n\n\n\a")
                sys.stdout = a
                
            else:
                break
            
    return r      
main()

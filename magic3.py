import csv
import requests
from bs4 import BeautifulSoup as Soup
import sys

'''
TODO
separa deck do side
usar diretorios
fazer uma saida geral e uma saida para cada

'''

col={}
deck={}
deck2={}
want=dict()
have=dict()
needs=[]
custos=[]
arqCol='magic.csv'
arqDeck='deck.txt'
arqdeck='deck2.txt'
lands=["Island",'Swamp','Plains','Mountain','Forest','Planície','Montanha','Ilha','Floresta','Pântano']


def main():
    '''
    destino=open("decklist2.txt",'w')
    
    sys.stdout=destino
    '''
    ler_dados_colecao(arqCol)

    for i in range(1,5):
        print("Burn",i)
        ler_dados_deck_arena('burn'+str(i)+'.txt')
        calcular_cartas()
        limpar()
    '''
    print('------------------------------------------------\n')
    for i in range(1,31):
        print("Novo",i)
        ler_dados_deck_arena('novo'+str(i)+'.txt')
        calcular_cartas()
        limpar()
        print('------------------------------------------------\n')
    
  
    
    print('deck1')
    ler_dados_deck('deck.txt')
    calcular_cartas()
    limpar()
    print('------------------------------------------------\n')
    print('deck2')
    ler_dados_deck_arena('deck2.txt')
    calcular_cartas()
    limpar()
    print('------------------------------------------------\n')
    for i in range(1,7):
        print("Simic",i)
        if i==5:
            ler_dados_deck('simic'+str(i)+'.txt')
        else:
            ler_dados_deck_arena('simic'+str(i)+'.txt')
        
        calcular_cartas()
        
        limpar()
        print('------------------------------------------------\n')
    for i in range(1,9):
        print("Dimir",i)
        ler_dados_deck_arena('dimir'+str(i)+'.txt')
        calcular_cartas()
        limpar()
        print('------------------------------------------------\n')
    for i in range(1,8):
        print("Amass",i)
        ler_dados_deck_arena('amass'+str(i)+'.txt')
        calcular_cartas()
        limpar()
        print('------------------------------------------------\n')

    
    for i in range(1,8):
        print("Orzhov",i)
        ler_dados_deck_arena('orzhov'+str(i)+'.txt')
        calcular_cartas()
        limpar()
        print('------------------------------------------------\n')
    
    for i in range(1,4):
        print("Gates",i)
        ler_dados_deck_arena('gates'+str(i)+'.txt')
        calcular_cartas()
        limpar()
        print('------------------------------------------------\n')

    '''
    print("\nForam analizados %3.3d decks\no minimo de cartas para montar um deles é %3.3d cartas"%(len(needs),min(needs)))
    print("O mais barato custa %6.2f reais para ser completado"%min(custos))
    print('------------------------------------------------\n')
    #sys.stdout = sys.__stdout__
    #destino.close()
    print('acabou')
    
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
        else:
            deck2[carta]=deck[carta]

    for carta in deck2:
        cartaEN=''.join(carta.split("'"))
        
       
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
    print("\nPara esse deck faltam %3.3d cartas com o custo de %6.2f\n"%(needs[-1],custos[-1]))
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
    ps=[]
    pagina="https://www.ligamagic.com.br/?view=cards/card&card="
    link="".join((pagina,"%20".join(carta.split(" "))))
    r=myRequest(link,"erro na carta "+carta)
    soup=Soup(r.text,"html.parser")
    r.close()
    for pr in soup.find_all("font",{'class':'bigger'}):
        ps.append(float(pr.text.replace(".","").replace(",",".")))
    try:
        
        preco=min(ps)
    except:
        a=sys.stdout
        sys.stdout = sys.__stdout__
        print(carta)
        sys.stdout = a
    
    #preco=float(soup.find("div",{'id':'mobile-precos-menor'}).text[3:].strip(".").replace(",","."))
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

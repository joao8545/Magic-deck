import requests
from bs4 import BeautifulSoup as Soup


def myRequest(url,erro):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
    while True:
            try:
                r=requests.get(url,headers=headers)
            except Exception:
                print("\a\n\n\n\n",erro,"\n\n\n\n\a")
                
            else:
                break
            
    return r
carta="Gleaming Overseer"
pagina="https://www.ligamagic.com.br/?view=cards/card&card="
link="".join((pagina,"%20".join(carta.split(" "))))
r=myRequest(link,"erro na carta "+carta)
soup=Soup(r.text,"html.parser")
r.close()
preco=float(soup.find("div",{'id':'mobile-precos-menor'}).text[3:].replace(",","."))

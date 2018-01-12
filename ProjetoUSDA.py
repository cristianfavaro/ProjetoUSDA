#Relatório Mensal do USDA

import requests
import time
from bs4 import BeautifulSoup as bs

#Função para corrigir error nas chaves importadas

def porcento(A3, B3):
    #B3 é o novo e A3 é o que vai ser comparado
    dife = (B3 - A3)/A3*100
    dife = "%.2f" % dife
    dife = dife.replace(".", ",")
    return dife


def arruma_html(x):
    for tag in x():
        tag.attrs = {
            attr: [" ".join(attr_value.replace("\n", " ").split() for attr_value in value)]
            if isinstance(value, list)
            else " ".join(value.replace("\n", " ").split())
        for attr, value in tag.attrs.items()
        }

# Começa programa
ativar_email = False
piscas = []

base_novo_relatorio = str(input("digite a data do novo relatório (form. (mês)xx-(dia)xx-(ano)xxxx): "))
enviar_email = input("Deja enviar o resultado por e-mail? (digite 's' ou 'n')")

if enviar_email == "s":
    ativar_email = True
    seu_endereço = input("Digite seu e-mail (precisa ser Gmail): ")
    sua_senha = input("Digite sua senha: " )
    destinatario = input("Digite o destinatário: ")


#base_compara_relatorio = str(input("digite a data do relatório para comparar (form. [mes]-xx-xxxx"))

ano_base = base_novo_relatorio.split("-")[-1]

novo_relatorio_url = requests.get(f"http://usda.mannlib.cornell.edu/usda/waob/wasde//2010s/{ano_base}/wasde-{base_novo_relatorio}.xml")


#Busca Novo Relatório

while True:
    novo_relatorio_url = requests.get(f"http://usda.mannlib.cornell.edu/usda/waob/wasde//2010s/{ano_base}/wasde-{base_novo_relatorio}.xml")
    if novo_relatorio_url.status_code == 200:
        break
        print(f"Relatório {base_novo_relatorio} encontrado!!")
    else: 
        print(f"Relatório {base_novo_relatorio} ainda não disponível... tentando novamente em 10 segundos!")
        time.sleep(10)


### Pegando página novo relatório

xpto_novo_relatorio = bs(novo_relatorio_url.text, "html5lib")
#xpto_compara_relatorio = bs(compara_relatorio_url.text, "html5lib")

### DADOS EUA

#######Soja


soja_EUA_novo_relatorio = xpto_novo_relatorio.sr15
arruma_html(soja_EUA_novo_relatorio)

#Estoques

soja_EUA_EstoqueFinal_novo_relatorio = soja_EUA_novo_relatorio.find("attribute4", {"attribute4":"Ending Stocks"}).findAll('m1_year_group') #com isso eu consigo todos.

soja_EUA_EstoqueFinal_novo_relatorio_update = soja_EUA_EstoqueFinal_novo_relatorio[-1].find("cell")["cell_value4"]
soja_EUA_EstoqueFinal_novo_relatorio_compara = soja_EUA_EstoqueFinal_novo_relatorio[-2].find("cell")["cell_value4"]
soja_EUA_EstoqueFinal_novo_relatorio_update = int(soja_EUA_EstoqueFinal_novo_relatorio_update.split(" ")[0])
soja_EUA_EstoqueFinal_novo_relatorio_compara = int(soja_EUA_EstoqueFinal_novo_relatorio_compara.split(" ")[0])

safra_desejada = str(soja_EUA_EstoqueFinal_novo_relatorio[-1]["market_year4"].split(" ")[0])

if soja_EUA_EstoqueFinal_novo_relatorio_update > soja_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA eleva projeção de estoque final em {safra_desejada} para {soja_EUA_EstoqueFinal_novo_relatorio_update} milhões de bushels ({porcento(soja_EUA_EstoqueFinal_novo_relatorio_compara, soja_EUA_EstoqueFinal_novo_relatorio_update)}%)")
elif soja_EUA_EstoqueFinal_novo_relatorio_update < soja_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA reduz projeção de estoque final em {safra_desejada} para {soja_EUA_EstoqueFinal_novo_relatorio_update} milhões de bushels ({porcento(soja_EUA_EstoqueFinal_novo_relatorio_compara, soja_EUA_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja/EUA: USDA mantém projeção de estoque final em {safra_desejada} em {soja_EUA_EstoqueFinal_novo_relatorio_update} milhões de bushels")

#Produção

soja_EUA_Production_novo_relatorio = soja_EUA_novo_relatorio.find("attribute4", {"attribute4":"Production"}).findAll('m1_year_group') #com isso eu consigo todos.

soja_EUA_Production_novo_relatorio_update = soja_EUA_Production_novo_relatorio[-1].find("cell")["cell_value4"]
soja_EUA_Production_novo_relatorio_compara = soja_EUA_Production_novo_relatorio[-2].find("cell")["cell_value4"]
soja_EUA_Production_novo_relatorio_update = float(soja_EUA_Production_novo_relatorio_update.replace(",", ".").split(" ")[0])
soja_EUA_Production_novo_relatorio_compara = float(soja_EUA_Production_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(soja_EUA_Production_novo_relatorio[-1]["market_year4"].split(" ")[0])

if soja_EUA_Production_novo_relatorio_update > soja_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA eleva projeção de produção em {safra_desejada} para {soja_EUA_Production_novo_relatorio_update} bilhões de bushels ({porcento(soja_EUA_Production_novo_relatorio_compara, soja_EUA_Production_novo_relatorio_update)}%)")
elif soja_EUA_Production_novo_relatorio_update < soja_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA reduz projeção de produção em {safra_desejada} para {soja_EUA_Production_novo_relatorio_update} bilhões de bushels ({porcento(soja_EUA_Production_novo_relatorio_compara, soja_EUA_Production_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja/EUA: USDA mantém projeção de produção em {safra_desejada} em {soja_EUA_Production_novo_relatorio_update} bilhões de bushels")

#Consumo

soja_EUA_Consumo_novo_relatorio = soja_EUA_novo_relatorio.find("attribute4", {"attribute4":"Use, Total"}).findAll('m1_year_group') #com isso eu consigo todos.

soja_EUA_Consumo_novo_relatorio_update = soja_EUA_Consumo_novo_relatorio[-1].find("cell")["cell_value4"]
soja_EUA_Consumo_novo_relatorio_compara = soja_EUA_Consumo_novo_relatorio[-2].find("cell")["cell_value4"]
soja_EUA_Consumo_novo_relatorio_update = float(soja_EUA_Consumo_novo_relatorio_update.replace(",", ".").split(" ")[0])
soja_EUA_Consumo_novo_relatorio_compara = float(soja_EUA_Consumo_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(soja_EUA_Consumo_novo_relatorio[-1]["market_year4"].split(" ")[0])

if soja_EUA_Consumo_novo_relatorio_update > soja_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA eleva projeção de consumo em {safra_desejada} para {soja_EUA_Consumo_novo_relatorio_update} bilhões de bushels ({porcento(soja_EUA_Consumo_novo_relatorio_compara, soja_EUA_Consumo_novo_relatorio_update)}%)")
elif soja_EUA_Consumo_novo_relatorio_update < soja_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA reduz projeção de consumo em {safra_desejada} para {soja_EUA_Consumo_novo_relatorio_update} bilhões de bushels ({porcento(soja_EUA_Consumo_novo_relatorio_compara, soja_EUA_Consumo_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja/EUA: USDA mantém projeção de consumo em {safra_desejada} em {soja_EUA_Consumo_novo_relatorio_update} bilhões de bushels")

#Rendimentos

soja_EUA_Rendimento_novo_relatorio = soja_EUA_novo_relatorio.find("attribute4", {"attribute4":"Yield per Harvested Acre"}).findAll('m1_year_group') #com isso eu consigo todos.

soja_EUA_Rendimento_novo_relatorio_update = soja_EUA_Rendimento_novo_relatorio[-1].find("cell")["cell_value4"]
soja_EUA_Rendimento_novo_relatorio_compara = soja_EUA_Rendimento_novo_relatorio[-2].find("cell")["cell_value4"]
soja_EUA_Rendimento_novo_relatorio_update = float(soja_EUA_Rendimento_novo_relatorio_update.replace(",", ".").split(" ")[0])
soja_EUA_Rendimento_novo_relatorio_compara = float(soja_EUA_Rendimento_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(soja_EUA_Rendimento_novo_relatorio[-1]["market_year4"].split(" ")[0])

if soja_EUA_Rendimento_novo_relatorio_update > soja_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA eleva projeção de rendimento em {safra_desejada} para {soja_EUA_Rendimento_novo_relatorio_update} bushels/acre ({porcento(soja_EUA_Rendimento_novo_relatorio_compara, soja_EUA_Rendimento_novo_relatorio_update)}%)")
elif soja_EUA_Rendimento_novo_relatorio_update < soja_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--Soja/EUA: USDA reduz projeção de rendimento em {safra_desejada} para {soja_EUA_Rendimento_novo_relatorio_update} bushels/acre ({porcento(soja_EUA_Rendimento_novo_relatorio_compara, soja_EUA_Rendimento_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja/EUA: USDA mantém projeção de rendimento em {safra_desejada} em {soja_EUA_Rendimento_novo_relatorio_update} bushels/acre")
 

#######Milho

milho_EUA_novo_relatorio = xpto_novo_relatorio.sr12
arruma_html(milho_EUA_novo_relatorio)

#Estoques

milho_EUA_EstoqueFinal_novo_relatorio = milho_EUA_novo_relatorio.find("attribute2", {"attribute2":"Ending Stocks"}).findAll('m2_year_group') #com isso eu consigo todos.

milho_EUA_EstoqueFinal_novo_relatorio_update = milho_EUA_EstoqueFinal_novo_relatorio[-1].find("cell")["cell_value2"]
milho_EUA_EstoqueFinal_novo_relatorio_compara = milho_EUA_EstoqueFinal_novo_relatorio[-2].find("cell")["cell_value2"]
milho_EUA_EstoqueFinal_novo_relatorio_update = float(milho_EUA_EstoqueFinal_novo_relatorio_update.replace(",", ".").split(" ")[0])
milho_EUA_EstoqueFinal_novo_relatorio_compara = float(milho_EUA_EstoqueFinal_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(milho_EUA_EstoqueFinal_novo_relatorio[-1]["market_year2"].split(" ")[0])

if milho_EUA_EstoqueFinal_novo_relatorio_update > milho_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA eleva projeção de estoque final em {safra_desejada} para {milho_EUA_EstoqueFinal_novo_relatorio_update} bilhões de bushels ({porcento(milho_EUA_EstoqueFinal_novo_relatorio_compara, milho_EUA_EstoqueFinal_novo_relatorio_update)}%)")
elif milho_EUA_EstoqueFinal_novo_relatorio_update < milho_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA reduz projeção de estoque final em {safra_desejada} para {milho_EUA_EstoqueFinal_novo_relatorio_update} bilhões de bushels ({porcento(milho_EUA_EstoqueFinal_novo_relatorio_compara, milho_EUA_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--milho/EUA: USDA mantém projeção de estoque final em {safra_desejada} em {milho_EUA_EstoqueFinal_novo_relatorio_update} bilhões de bushels")


#Produção

milho_EUA_Production_novo_relatorio = milho_EUA_novo_relatorio.find("attribute2", {"attribute2":"Production"}).findAll('m2_year_group') #com isso eu consigo todos.

milho_EUA_Production_novo_relatorio_update = milho_EUA_Production_novo_relatorio[-1].find("cell")["cell_value2"]
milho_EUA_Production_novo_relatorio_compara = milho_EUA_Production_novo_relatorio[-2].find("cell")["cell_value2"]
milho_EUA_Production_novo_relatorio_update = float(milho_EUA_Production_novo_relatorio_update.replace(",", ".").split(" ")[0])
milho_EUA_Production_novo_relatorio_compara = float(milho_EUA_Production_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(milho_EUA_Production_novo_relatorio[-1]["market_year2"].split(" ")[0])

if milho_EUA_Production_novo_relatorio_update > milho_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA eleva projeção de produção em {safra_desejada} para {milho_EUA_Production_novo_relatorio_update} bilhões de bushels ({porcento(milho_EUA_Production_novo_relatorio_compara, milho_EUA_Production_novo_relatorio_update)}%)")
elif milho_EUA_Production_novo_relatorio_update < milho_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA reduz projeção de produção em {safra_desejada} para {milho_EUA_Production_novo_relatorio_update} bilhões de bushels ({porcento(milho_EUA_Production_novo_relatorio_compara, milho_EUA_Production_novo_relatorio_update)}%)")
else:
    piscas.append(f"--milho/EUA: USDA mantém projeção de produção em {safra_desejada} em {milho_EUA_Production_novo_relatorio_update} bilhões de bushels")

#Consumo

milho_EUA_Consumo_novo_relatorio = milho_EUA_novo_relatorio.find("attribute2", {"attribute2":"Use, Total"}).findAll('m2_year_group') #com isso eu consigo todos.

milho_EUA_Consumo_novo_relatorio_update = milho_EUA_Consumo_novo_relatorio[-1].find("cell")["cell_value2"]
milho_EUA_Consumo_novo_relatorio_compara = milho_EUA_Consumo_novo_relatorio[-2].find("cell")["cell_value2"]
milho_EUA_Consumo_novo_relatorio_update = float(milho_EUA_Consumo_novo_relatorio_update.replace(",", ".").split(" ")[0])
milho_EUA_Consumo_novo_relatorio_compara = float(milho_EUA_Consumo_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(milho_EUA_Consumo_novo_relatorio[-1]["market_year2"].split(" ")[0])

if milho_EUA_Consumo_novo_relatorio_update > milho_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA eleva projeção de consumo em {safra_desejada} para {milho_EUA_Consumo_novo_relatorio_update} bilhões de bushels ({porcento(milho_EUA_Consumo_novo_relatorio_compara, milho_EUA_Consumo_novo_relatorio_update)}%)")
elif milho_EUA_Consumo_novo_relatorio_update < milho_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA reduz projeção de consumo em {safra_desejada} para {milho_EUA_Consumo_novo_relatorio_update} bilhões de bushels ({porcento(milho_EUA_Consumo_novo_relatorio_compara, milho_EUA_Consumo_novo_relatorio_update)}%)")
else:
    piscas.append(f"--milho/EUA: USDA mantém projeção de consumo em {safra_desejada} em {milho_EUA_Consumo_novo_relatorio_update} bilhões de bushels")

#Rendimentos

milho_EUA_Rendimento_novo_relatorio = milho_EUA_novo_relatorio.find("attribute2", {"attribute2":"Yield per Harvested Acre"}).findAll('m2_year_group') #com isso eu consigo todos.

milho_EUA_Rendimento_novo_relatorio_update = milho_EUA_Rendimento_novo_relatorio[-1].find("cell")["cell_value2"]
milho_EUA_Rendimento_novo_relatorio_compara = milho_EUA_Rendimento_novo_relatorio[-2].find("cell")["cell_value2"]
milho_EUA_Rendimento_novo_relatorio_update = float(milho_EUA_Rendimento_novo_relatorio_update.replace(",", ".").split(" ")[0])
milho_EUA_Rendimento_novo_relatorio_compara = float(milho_EUA_Rendimento_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(milho_EUA_Rendimento_novo_relatorio[-1]["market_year2"].split(" ")[0])

if milho_EUA_Rendimento_novo_relatorio_update > milho_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA eleva projeção de rendimento em {safra_desejada} para {milho_EUA_Rendimento_novo_relatorio_update} bushels/acre ({porcento(milho_EUA_Rendimento_novo_relatorio_compara, milho_EUA_Rendimento_novo_relatorio_update)}%)")
elif milho_EUA_Rendimento_novo_relatorio_update < milho_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--milho/EUA: USDA reduz projeção de rendimento em {safra_desejada} para {milho_EUA_Rendimento_novo_relatorio_update} bushels/acre ({porcento(milho_EUA_Rendimento_novo_relatorio_compara, milho_EUA_Rendimento_novo_relatorio_update)}%)")
else:
    piscas.append(f"--milho/EUA: USDA mantém projeção de rendimento em {safra_desejada} em {milho_EUA_Rendimento_novo_relatorio_update} bushels/acre")

######Trigo

trigo_EUA_novo_relatorio = xpto_novo_relatorio.sr11
arruma_html(trigo_EUA_novo_relatorio)


trigo_EUA_EstoqueFinal_novo_relatorio = trigo_EUA_novo_relatorio.find("attribute1", {"attribute1":"Ending Stocks"}).findAll('m1_year_group') #com isso eu consigo todos.

#Estoques

trigo_EUA_EstoqueFinal_novo_relatorio = trigo_EUA_novo_relatorio.find("attribute1", {"attribute1":"Ending Stocks"}).findAll('m1_year_group') #com isso eu consigo todos.

trigo_EUA_EstoqueFinal_novo_relatorio_update = trigo_EUA_EstoqueFinal_novo_relatorio[-1].find("cell")["cell_value1"]
trigo_EUA_EstoqueFinal_novo_relatorio_compara = trigo_EUA_EstoqueFinal_novo_relatorio[-2].find("cell")["cell_value1"]
trigo_EUA_EstoqueFinal_novo_relatorio_update = float(trigo_EUA_EstoqueFinal_novo_relatorio_update.replace(",", ".").split(" ")[0])
trigo_EUA_EstoqueFinal_novo_relatorio_compara = float(trigo_EUA_EstoqueFinal_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(trigo_EUA_EstoqueFinal_novo_relatorio[-1]["market_year1"].split(" ")[0])

if trigo_EUA_EstoqueFinal_novo_relatorio_update > trigo_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA eleva projeção de estoque final em {safra_desejada} para {trigo_EUA_EstoqueFinal_novo_relatorio_update} milhões de bushels ({porcento(trigo_EUA_EstoqueFinal_novo_relatorio_compara, trigo_EUA_EstoqueFinal_novo_relatorio_update)}%)")
elif trigo_EUA_EstoqueFinal_novo_relatorio_update < trigo_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA reduz projeção de estoque final em {safra_desejada} para {trigo_EUA_EstoqueFinal_novo_relatorio_update} milhões de bushels ({porcento(trigo_EUA_EstoqueFinal_novo_relatorio_compara, trigo_EUA_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--trigo/EUA: USDA mantém projeção de estoque final em {safra_desejada} em {trigo_EUA_EstoqueFinal_novo_relatorio_update} milhões de bushels")


#Produção

trigo_EUA_Production_novo_relatorio = trigo_EUA_novo_relatorio.find("attribute1", {"attribute1":"Production"}).findAll('m1_year_group') #com isso eu consigo todos.

trigo_EUA_Production_novo_relatorio_update = trigo_EUA_Production_novo_relatorio[-1].find("cell")["cell_value1"]
trigo_EUA_Production_novo_relatorio_compara = trigo_EUA_Production_novo_relatorio[-2].find("cell")["cell_value1"]
trigo_EUA_Production_novo_relatorio_update = float(trigo_EUA_Production_novo_relatorio_update.replace(",", ".").split(" ")[0])
trigo_EUA_Production_novo_relatorio_compara = float(trigo_EUA_Production_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(trigo_EUA_Production_novo_relatorio[-1]["market_year1"].split(" ")[0])

if trigo_EUA_Production_novo_relatorio_update > trigo_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA eleva projeção de produção em {safra_desejada} para {trigo_EUA_Production_novo_relatorio_update} bi de bushels ({porcento(trigo_EUA_Production_novo_relatorio_compara, trigo_EUA_Production_novo_relatorio_update)}%)")
elif trigo_EUA_Production_novo_relatorio_update < trigo_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA reduz projeção de produção em {safra_desejada} para {trigo_EUA_Production_novo_relatorio_update} bi de bushels ({porcento(trigo_EUA_Production_novo_relatorio_compara, trigo_EUA_Production_novo_relatorio_update)}%)")
else:
    piscas.append(f"--trigo/EUA: USDA mantém projeção de produção em {safra_desejada} em {trigo_EUA_Production_novo_relatorio_update} bi de bushels")

#Consumo 

trigo_EUA_Consumo_novo_relatorio = trigo_EUA_novo_relatorio.find("attribute1", {"attribute1":"Use, Total"}).findAll('m1_year_group') #com isso eu consigo todos.

trigo_EUA_Consumo_novo_relatorio_update = trigo_EUA_Consumo_novo_relatorio[-1].find("cell")["cell_value1"]
trigo_EUA_Consumo_novo_relatorio_compara = trigo_EUA_Consumo_novo_relatorio[-2].find("cell")["cell_value1"]
trigo_EUA_Consumo_novo_relatorio_update = float(trigo_EUA_Consumo_novo_relatorio_update.replace(",", ".").split(" ")[0])
trigo_EUA_Consumo_novo_relatorio_compara = float(trigo_EUA_Consumo_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(trigo_EUA_Consumo_novo_relatorio[-1]["market_year1"].split(" ")[0])

if trigo_EUA_Consumo_novo_relatorio_update > trigo_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA eleva projeção de consumo em {safra_desejada} para {trigo_EUA_Consumo_novo_relatorio_update} bilhões de bushels ({porcento(trigo_EUA_Consumo_novo_relatorio_compara, trigo_EUA_Consumo_novo_relatorio_update)}%)")
elif trigo_EUA_Consumo_novo_relatorio_update < trigo_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA reduz projeção de consumo em {safra_desejada} para {trigo_EUA_Consumo_novo_relatorio_update} bilhões de bushels ({porcento(trigo_EUA_Consumo_novo_relatorio_compara, trigo_EUA_Consumo_novo_relatorio_update)}%)")
else:
    piscas.append(f"--trigo/EUA: USDA mantém projeção de consumo em {safra_desejada} em {trigo_EUA_Consumo_novo_relatorio_update} bilhões de bushels")


#Rendimentos

trigo_EUA_Rendimento_novo_relatorio = trigo_EUA_novo_relatorio.find("attribute1", {"attribute1":"Yield per Harvested Acre"}).findAll('m1_year_group') #com isso eu consigo todos.

trigo_EUA_Rendimento_novo_relatorio_update = trigo_EUA_Rendimento_novo_relatorio[-1].find("cell")["cell_value1"]
trigo_EUA_Rendimento_novo_relatorio_compara = trigo_EUA_Rendimento_novo_relatorio[-2].find("cell")["cell_value1"]
trigo_EUA_Rendimento_novo_relatorio_update = float(trigo_EUA_Rendimento_novo_relatorio_update.replace(",", ".").split(" ")[0])
trigo_EUA_Rendimento_novo_relatorio_compara = float(trigo_EUA_Rendimento_novo_relatorio_compara.replace(",", ".").split(" ")[0])


safra_desejada = str(trigo_EUA_Rendimento_novo_relatorio[-1]["market_year1"].split(" ")[0])

if trigo_EUA_Rendimento_novo_relatorio_update > trigo_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA eleva projeção de rendimento em {safra_desejada} de {trigo_EUA_Rendimento_novo_relatorio_compara} para {trigo_EUA_Rendimento_novo_relatorio_update} bushels/acre ({porcento(trigo_EUA_Rendimento_novo_relatorio_compara, trigo_EUA_Rendimento_novo_relatorio_update)}%)")
elif trigo_EUA_Rendimento_novo_relatorio_update < trigo_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--trigo/EUA: USDA reduz projeção de rendimento em {safra_desejada} de {trigo_EUA_Rendimento_novo_relatorio_compara} para {trigo_EUA_Rendimento_novo_relatorio_update} bushels/acre ({porcento(trigo_EUA_Rendimento_novo_relatorio_compara, trigo_EUA_Rendimento_novo_relatorio_update)}%)")
else:
    piscas.append(f"--trigo/EUA: USDA mantém projeção de rendimento em {safra_desejada} em {trigo_EUA_Rendimento_novo_relatorio_update} bushels/acre")


######Algodão

algodao_EUA_novo_relatorio = xpto_novo_relatorio.sr17
arruma_html(algodao_EUA_novo_relatorio)


algodao_EUA_EstoqueFinal_novo_relatorio = algodao_EUA_novo_relatorio.find("attribute4", {"attribute4":"Ending Stocks"}).findAll('m1_year_group') #com isso eu consigo todos.


algodao_EUA_EstoqueFinal_novo_relatorio = algodao_EUA_novo_relatorio.find("attribute4", {"attribute4":"Ending Stocks"}).findAll('m1_year_group') #com isso eu consigo todos.

algodao_EUA_EstoqueFinal_novo_relatorio_update = algodao_EUA_EstoqueFinal_novo_relatorio[-1].find("cell")["cell_value4"]
algodao_EUA_EstoqueFinal_novo_relatorio_compara = algodao_EUA_EstoqueFinal_novo_relatorio[-2].find("cell")["cell_value4"]
algodao_EUA_EstoqueFinal_novo_relatorio_update = float(algodao_EUA_EstoqueFinal_novo_relatorio_update.replace(",", ".").split(" ")[0])
algodao_EUA_EstoqueFinal_novo_relatorio_compara = float(algodao_EUA_EstoqueFinal_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(algodao_EUA_EstoqueFinal_novo_relatorio[-1]["market_year4"].split(" ")[0])

if algodao_EUA_EstoqueFinal_novo_relatorio_update > algodao_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA eleva projeção de estoque final em {safra_desejada} de {algodao_EUA_EstoqueFinal_novo_relatorio_compara} para {algodao_EUA_EstoqueFinal_novo_relatorio_update} milhões de fardos ({porcento(algodao_EUA_EstoqueFinal_novo_relatorio_compara, algodao_EUA_EstoqueFinal_novo_relatorio_update)}%)")
elif algodao_EUA_EstoqueFinal_novo_relatorio_update < algodao_EUA_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA reduz projeção de estoque final em {safra_desejada} de {algodao_EUA_EstoqueFinal_novo_relatorio_compara} para {algodao_EUA_EstoqueFinal_novo_relatorio_update} milhões de fardos ({porcento(algodao_EUA_EstoqueFinal_novo_relatorio_compara, algodao_EUA_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--algodao/EUA: USDA mantém projeção de estoque final em {safra_desejada} em {algodao_EUA_EstoqueFinal_novo_relatorio_update} milhões de fardos")


#Produção

algodao_EUA_Production_novo_relatorio = algodao_EUA_novo_relatorio.find("attribute4", {"attribute4":"Production"}).findAll('m1_year_group') #com isso eu consigo todos.

algodao_EUA_Production_novo_relatorio_update = algodao_EUA_Production_novo_relatorio[-1].find("cell")["cell_value4"]
algodao_EUA_Production_novo_relatorio_compara = algodao_EUA_Production_novo_relatorio[-2].find("cell")["cell_value4"]
algodao_EUA_Production_novo_relatorio_update = float(algodao_EUA_Production_novo_relatorio_update.replace(",", ".").split(" ")[0])
algodao_EUA_Production_novo_relatorio_compara = float(algodao_EUA_Production_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(algodao_EUA_Production_novo_relatorio[-1]["market_year4"].split(" ")[0])

if algodao_EUA_Production_novo_relatorio_update > algodao_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA eleva projeção de produção em {safra_desejada} para {algodao_EUA_Production_novo_relatorio_update} milhões de fardos ({porcento(algodao_EUA_Production_novo_relatorio_compara, algodao_EUA_Production_novo_relatorio_update)}%)")
elif algodao_EUA_Production_novo_relatorio_update < algodao_EUA_Production_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA reduz projeção de produção em {safra_desejada} para {algodao_EUA_Production_novo_relatorio_update} milhões de fardos ({porcento(algodao_EUA_Production_novo_relatorio_compara, algodao_EUA_Production_novo_relatorio_update)}%)")
else:
    piscas.append(f"--algodao/EUA: USDA mantém projeção de produção em {safra_desejada} em {algodao_EUA_Production_novo_relatorio_update} milhões de fardos")

#Consumo 

algodao_EUA_Consumo_novo_relatorio = algodao_EUA_novo_relatorio.find("attribute4", {"attribute4":"Use, Total"}).findAll('m1_year_group') #com isso eu consigo todos.

algodao_EUA_Consumo_novo_relatorio_update = algodao_EUA_Consumo_novo_relatorio[-1].find("cell")["cell_value4"]
algodao_EUA_Consumo_novo_relatorio_compara = algodao_EUA_Consumo_novo_relatorio[-2].find("cell")["cell_value4"]
algodao_EUA_Consumo_novo_relatorio_update = float(algodao_EUA_Consumo_novo_relatorio_update.replace(",", ".").split(" ")[0])
algodao_EUA_Consumo_novo_relatorio_compara = float(algodao_EUA_Consumo_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(algodao_EUA_Consumo_novo_relatorio[-1]["market_year4"].split(" ")[0])

if algodao_EUA_Consumo_novo_relatorio_update > algodao_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA eleva projeção de consumo em {safra_desejada} para {algodao_EUA_Consumo_novo_relatorio_update} milhões de fardos ({porcento(algodao_EUA_Consumo_novo_relatorio_compara, algodao_EUA_Consumo_novo_relatorio_update)}%)")
elif algodao_EUA_Consumo_novo_relatorio_update < algodao_EUA_Consumo_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA reduz projeção de consumo em {safra_desejada} para {algodao_EUA_Consumo_novo_relatorio_update} milhões de fardos ({porcento(algodao_EUA_Consumo_novo_relatorio_compara, algodao_EUA_Consumo_novo_relatorio_update)}%)")
else:
    piscas.append(f"--algodao/EUA: USDA mantém projeção de consumo em {safra_desejada} em {algodao_EUA_Consumo_novo_relatorio_update} milhões de fardos")


#Rendimentos

algodao_EUA_Rendimento_novo_relatorio = algodao_EUA_novo_relatorio.find("attribute4", {"attribute4":"Yield per Harvested Acre"}).findAll('m1_year_group') #com isso eu consigo todos.

algodao_EUA_Rendimento_novo_relatorio_update = algodao_EUA_Rendimento_novo_relatorio[-1].find("cell")["cell_value4"]
algodao_EUA_Rendimento_novo_relatorio_compara = algodao_EUA_Rendimento_novo_relatorio[-2].find("cell")["cell_value4"]
algodao_EUA_Rendimento_novo_relatorio_update = float(algodao_EUA_Rendimento_novo_relatorio_update.replace(",", ".").split(" ")[0])
algodao_EUA_Rendimento_novo_relatorio_compara = float(algodao_EUA_Rendimento_novo_relatorio_compara.replace(",", ".").split(" ")[0])

safra_desejada = str(algodao_EUA_Rendimento_novo_relatorio[-1]["market_year4"].split(" ")[0])

if algodao_EUA_Rendimento_novo_relatorio_update > algodao_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA eleva projeção de rendimento em {safra_desejada} para {algodao_EUA_Rendimento_novo_relatorio_update} fardos/acre ({porcento(algodao_EUA_Rendimento_novo_relatorio_compara, algodao_EUA_Rendimento_novo_relatorio_update)}%)")
elif algodao_EUA_Rendimento_novo_relatorio_update < algodao_EUA_Rendimento_novo_relatorio_compara:
    piscas.append(f"--algodao/EUA: USDA reduz projeção de rendimento em {safra_desejada} para {algodao_EUA_Rendimento_novo_relatorio_update} fardos/acre ({porcento(algodao_EUA_Rendimento_novo_relatorio_compara, algodao_EUA_Rendimento_novo_relatorio_update)}%)")
else:
    piscas.append(f"--algodao/EUA: USDA mantém projeção de rendimento em {safra_desejada} em {algodao_EUA_Rendimento_novo_relatorio_update} fardos/acre")


###### DADOS MUNDO #########

####Soja

### SOja Total

soja_MUNDO_novo_relatorio = xpto_novo_relatorio.sr28
arruma_html(soja_MUNDO_novo_relatorio)

soja_MUNDO_Total_novo_relatorio_update = soja_MUNDO_novo_relatorio.find("matrix3").find("m1_region_group3", {"region2":"World 2/"})


#Estoques Finais Mundo
soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update = float(soja_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-1].find("m1_attribute_group3", {"attribute2":"Ending Stocks"}).find("cell")["cell_value2"].split(" ")[0])
soja_MUNDO_Total_EstoqueFinal_novo_relatorio_compara = float(soja_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-2].find("m1_attribute_group3", {"attribute2":"Ending Stocks"}).find("cell")["cell_value2"].split(" ")[0])

safra_desejada = str(soja_MUNDO_novo_relatorio.find("matrix3")["region_header2"].split(" ")[0])

if soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update > soja_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--Soja: USDA eleva projeção de estoque final global em {safra_desejada} para {soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update} bilhões de bushels ({porcento(soja_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
elif soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update < soja_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--Soja: USDA reduz projeção de estoque final em {safra_desejada} para {soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update} bilhões de bushels ({porcento(soja_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja: USDA mantém projeção de estoque final em {safra_desejada} em {soja_MUNDO_Total_EstoqueFinal_novo_relatorio_update} bilhões de bushels")



#Consumo Mundo 

soja_MUNDO_Total_Consumo_novo_relatorio_update = float(soja_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-1].find("m1_attribute_group3", {"attribute2":"Domestic Crush"}).find("cell")["cell_value2"].split(" ")[0])
soja_MUNDO_Total_Consumo_novo_relatorio_compara = float(soja_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-2].find("m1_attribute_group3", {"attribute2":"Domestic Crush"}).find("cell")["cell_value2"].split(" ")[0])

safra_desejada = str(soja_MUNDO_novo_relatorio.find("matrix3")["region_header2"].split(" ")[0])

if soja_MUNDO_Total_Consumo_novo_relatorio_update > soja_MUNDO_Total_Consumo_novo_relatorio_compara:
    piscas.append(f"--Soja: USDA eleva projeção de consumo global em {safra_desejada} para {soja_MUNDO_Total_Consumo_novo_relatorio_update} milhões de bushels ({porcento(soja_MUNDO_Total_Consumo_novo_relatorio_compara, soja_MUNDO_Total_Consumo_novo_relatorio_update)}%)")
elif soja_MUNDO_Total_Consumo_novo_relatorio_update < soja_MUNDO_Total_Consumo_novo_relatorio_compara:
    piscas.append(f"--Soja: USDA reduz projeção de consumo global em {safra_desejada} para {soja_MUNDO_Total_Consumo_novo_relatorio_update} milhões de bushels ({porcento(soja_MUNDO_Total_Consumo_novo_relatorio_compara, soja_MUNDO_Total_Consumo_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja: USDA mantém projeção de consumo global em {safra_desejada} em {soja_MUNDO_Total_Consumo_novo_relatorio_update} milhões de bushels")


#Importação China - Soja


soja_China_Importacao_novo_relatorio_update = float(soja_MUNDO_novo_relatorio.find("matrix3").find("m1_region_group3", {"region2":"China"}).find("m1_month_group2_collection").findAll("m1_month_group2")[-1].find("m1_attribute_group3", {"attribute2":"Ending Stocks"}).find("cell")["cell_value2"].split(" ")[0])
soja_China_Importacao_novo_relatorio_compara = float(soja_MUNDO_novo_relatorio.find("matrix3").find("m1_region_group3", {"region2":"China"}).find("m1_month_group2_collection").findAll("m1_month_group2")[-2].find("m1_attribute_group3", {"attribute2":"Ending Stocks"}).find("cell")["cell_value2"].split(" ")[0])

safra_desejada = str(soja_MUNDO_novo_relatorio.find("matrix3")["region_header2"].split(" ")[0])

if soja_China_Importacao_novo_relatorio_update > soja_China_Importacao_novo_relatorio_compara:
    piscas.append(f"--Soja/China: USDA eleva projeção de importação em {safra_desejada} para {soja_China_Importacao_novo_relatorio_update} milhões de bushels ({porcento(soja_China_Importacao_novo_relatorio_compara, soja_China_Importacao_novo_relatorio_update)}%)")
elif soja_China_Importacao_novo_relatorio_update < soja_China_Importacao_novo_relatorio_compara:
    piscas.append(f"--Soja/China: USDA reduz projeção de importação em {safra_desejada} para {soja_China_Importacao_novo_relatorio_update} milhões de bushels ({porcento(soja_China_Importacao_novo_relatorio_compara, soja_China_Importacao_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja/China: USDA mantém projeção de importação em {safra_desejada} em {soja_China_Importacao_novo_relatorio_update} milhões de bushels")


#Exportação Brasil - Soja 

soja_Brasil_Exportacao_novo_relatorio_update = float(soja_MUNDO_novo_relatorio.find("matrix3").find("m1_region_group3", {"region2":"Brazil"}).find("m1_month_group2_collection").findAll("m1_month_group2")[-1].find("m1_attribute_group3", {"attribute2":"Exports"}).find("cell")["cell_value2"].split(" ")[0])
soja_Brasil_Exportacao_novo_relatorio_compara = float(soja_MUNDO_novo_relatorio.find("matrix3").find("m1_region_group3", {"region2":"Brazil"}).find("m1_month_group2_collection").findAll("m1_month_group2")[-2].find("m1_attribute_group3", {"attribute2":"Exports"}).find("cell")["cell_value2"].split(" ")[0])

safra_desejada = str(soja_MUNDO_novo_relatorio.find("matrix3")["region_header2"].split(" ")[0])

if soja_Brasil_Exportacao_novo_relatorio_update > soja_Brasil_Exportacao_novo_relatorio_compara:
    piscas.append(f"--Soja/Brasil: USDA eleva projeção de exportação em {safra_desejada} para {soja_Brasil_Exportacao_novo_relatorio_update} milhões de bushels ({porcento(soja_Brasil_Exportacao_novo_relatorio_compara, soja_Brasil_Exportacao_novo_relatorio_update)}%)")
elif soja_Brasil_Exportacao_novo_relatorio_update < soja_Brasil_Exportacao_novo_relatorio_compara:
    piscas.append(f"--Soja/Brasil: USDA reduz projeção de exportação em {safra_desejada} para {soja_Brasil_Exportacao_novo_relatorio_update} milhões de bushels ({porcento(soja_Brasil_Exportacao_novo_relatorio_compara, soja_Brasil_Exportacao_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja/Brasil: USDA mantém projeção de exportação em {safra_desejada} em {soja_Brasil_Exportacao_novo_relatorio_update} milhões de bushels")


#Produção Argentina
 
soja_Argentina_Producao_novo_relatorio_update = float(soja_MUNDO_novo_relatorio.find("matrix3").find("m1_region_group3", {"region2":"Argentina"}).find("m1_month_group2_collection").findAll("m1_month_group2")[-1].find("m1_attribute_group3", {"attribute2":"Production"}).find("cell")["cell_value2"].split(" ")[0])
soja_Argentina_Producao_novo_relatorio_compara = float(soja_MUNDO_novo_relatorio.find("matrix3").find("m1_region_group3", {"region2":"Argentina"}).find("m1_month_group2_collection").findAll("m1_month_group2")[-2].find("m1_attribute_group3", {"attribute2":"Production"}).find("cell")["cell_value2"].split(" ")[0])

safra_desejada = str(soja_MUNDO_novo_relatorio.find("matrix3")["region_header2"].split(" ")[0])

if soja_Argentina_Producao_novo_relatorio_update > soja_Argentina_Producao_novo_relatorio_compara:
    piscas.append(f"--Soja/Argentina: USDA eleva projeção de produção em {safra_desejada} para {soja_Argentina_Producao_novo_relatorio_update} milhões de bushels ({porcento(soja_Argentina_Producao_novo_relatorio_compara, soja_Argentina_Producao_novo_relatorio_update)}%)")
elif soja_Argentina_Producao_novo_relatorio_update < soja_Argentina_Producao_novo_relatorio_compara:
    piscas.append(f"--Soja/Argentina: USDA reduz projeção de produção em {safra_desejada} para {soja_Argentina_Producao_novo_relatorio_update} milhões de bushels ({porcento(soja_Argentina_Producao_novo_relatorio_compara, soja_Argentina_Producao_novo_relatorio_update)}%)")
else:
    piscas.append(f"--Soja/Argentina: USDA mantém projeção de produção em {safra_desejada} em {soja_Argentina_Producao_novo_relatorio_update} milhões de bushels")



#####Milho Global

#Estoque Final

milho_MUNDO_novo_relatorio = xpto_novo_relatorio.sr23
arruma_html(milho_MUNDO_novo_relatorio)

milho_MUNDO_Total_novo_relatorio_update = milho_MUNDO_novo_relatorio.find("matrix1").find("m1_region_group", {"region1":"World 3/"})


milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update = float(milho_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-1].find("m1_attribute_group", {"attribute1":"Ending Stocks"}).find("cell")["cell_value1"].split(" ")[0])
milho_MUNDO_Total_EstoqueFinal_novo_relatorio_compara = float(milho_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-2].find("m1_attribute_group", {"attribute1":"Ending Stocks"}).find("cell")["cell_value1"].split(" ")[0])


safra_desejada = str(milho_MUNDO_novo_relatorio.find("matrix1")["region_header1"].split(" ")[0])

if milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update > milho_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--milho: USDA eleva projeção de estoque final global em {safra_desejada} para {milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de t ({porcento(milho_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
elif milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update < milho_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--milho: USDA reduz projeção de estoque final global em {safra_desejada} para {milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de t ({porcento(milho_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--milho: USDA mantém projeção de estoque final global em {safra_desejada} em {milho_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de t")


#Produção

milho_MUNDO_Total_Producao_novo_relatorio_update = float(milho_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-1].find("m1_attribute_group", {"attribute1":"Production"}).find("cell")["cell_value1"].replace(",", "").split(" ")[0])
milho_MUNDO_Total_Producao_novo_relatorio_compara = float(milho_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-2].find("m1_attribute_group", {"attribute1":"Production"}).find("cell")["cell_value1"].replace(",", "").split(" ")[0])

safra_desejada = str(milho_MUNDO_novo_relatorio.find("matrix1")["region_header1"].split(" ")[0])

if milho_MUNDO_Total_Producao_novo_relatorio_update > milho_MUNDO_Total_Producao_novo_relatorio_compara:
    piscas.append(f"--milho: USDA eleva projeção de Producao global em {safra_desejada} para {milho_MUNDO_Total_Producao_novo_relatorio_update} bilhòes de t ({porcento(milho_MUNDO_Total_Producao_novo_relatorio_compara, milho_MUNDO_Total_Producao_novo_relatorio_update)}%)")
elif milho_MUNDO_Total_Producao_novo_relatorio_update < milho_MUNDO_Total_Producao_novo_relatorio_compara:
    piscas.append(f"--milho: USDA reduz projeção de Producao global em {safra_desejada} para {milho_MUNDO_Total_Producao_novo_relatorio_update} bilhòes de t ({porcento(milho_MUNDO_Total_Producao_novo_relatorio_compara, milho_MUNDO_Total_Producao_novo_relatorio_update)}%)")
else:
    piscas.append(f"--milho: USDA mantém projeção de Producao global em {safra_desejada} em {milho_MUNDO_Total_Producao_novo_relatorio_update} bilhòes de t")


# Milho argentina

milho_Argentina_Producao_novo_relatorio_update = float(milho_MUNDO_novo_relatorio.find("matrix1").find("m1_region_group", {"region1":"Argentina"}).find("m1_month_group_collection").findAll("m1_month_group")[-1].find("m1_attribute_group", {"attribute1":"Production"}).find("cell")["cell_value1"].split(" ")[0].split(" ")[0])
milho_Argentina_Producao_novo_relatorio_compara = float(milho_MUNDO_novo_relatorio.find("matrix1").find("m1_region_group", {"region1":"Argentina"}).find("m1_month_group_collection").findAll("m1_month_group")[-2].find("m1_attribute_group", {"attribute1":"Production"}).find("cell")["cell_value1"].split(" ")[0].split(" ")[0])


safra_desejada = str(milho_MUNDO_novo_relatorio.find("matrix1")["region_header1"].split(" ")[0])

if milho_Argentina_Producao_novo_relatorio_update > milho_Argentina_Producao_novo_relatorio_compara:
    piscas.append(f"--milho/Argentina: USDA eleva projeção de produção em {safra_desejada} para {milho_Argentina_Producao_novo_relatorio_update} milhões de t ({porcento(milho_Argentina_Producao_novo_relatorio_compara, milho_Argentina_Producao_novo_relatorio_update)}%)")
elif milho_Argentina_Producao_novo_relatorio_update < milho_Argentina_Producao_novo_relatorio_compara:
    piscas.append(f"--milho/Argentina: USDA reduz projeção de produção em {safra_desejada} para {milho_Argentina_Producao_novo_relatorio_update} milhões de t ({porcento(milho_Argentina_Producao_novo_relatorio_compara, milho_Argentina_Producao_novo_relatorio_update)}%)")
else:
    piscas.append(f"--milho/Argentina: USDA mantém projeção de produção em {safra_desejada} em {milho_Argentina_Producao_novo_relatorio_update} milhões de t")


###Trigo Mundo

#Estoque Final
trigo_MUNDO_novo_relatorio = xpto_novo_relatorio.sr19
arruma_html(trigo_MUNDO_novo_relatorio)

trigo_MUNDO_Total_novo_relatorio_update = trigo_MUNDO_novo_relatorio.find("matrix1").find("m1_region_group", {"region1":"World 3/"})


#Estoque Final

trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update = float(trigo_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-1].find("m1_attribute_group", {"attribute1":"Ending Stocks"}).find("cell")["cell_value1"].split(" ")[0])
trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_compara = float(trigo_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-2].find("m1_attribute_group", {"attribute1":"Ending Stocks"}).find("cell")["cell_value1"].split(" ")[0])


safra_desejada = str(trigo_MUNDO_novo_relatorio.find("matrix1")["region_header1"].split(" ")[0])

if trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update > trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--trigo: USDA eleva projeção de estoque final global em {safra_desejada} para {trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de t ({porcento(trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
elif trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update < trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--trigo: USDA reduz projeção de estoque final global em {safra_desejada} para {trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de t ({porcento(trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--trigo: USDA mantém projeção de estoque final global em {safra_desejada} em {trigo_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de t")

#Produção

trigo_MUNDO_Total_Producao_novo_relatorio_update = float(trigo_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-1].find("m1_attribute_group", {"attribute1":"Production"}).find("cell")["cell_value1"].split(" ")[0])
trigo_MUNDO_Total_Producao_novo_relatorio_compara = float(trigo_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group")[-2].find("m1_attribute_group", {"attribute1":"Production"}).find("cell")["cell_value1"].split(" ")[0])


safra_desejada = str(trigo_MUNDO_novo_relatorio.find("matrix1")["region_header1"].split(" ")[0])

if trigo_MUNDO_Total_Producao_novo_relatorio_update > trigo_MUNDO_Total_Producao_novo_relatorio_compara:
    piscas.append(f"--trigo: USDA eleva projeção de produção global em {safra_desejada} para {trigo_MUNDO_Total_Producao_novo_relatorio_update} milhões de t ({porcento(trigo_MUNDO_Total_Producao_novo_relatorio_compara, trigo_MUNDO_Total_Producao_novo_relatorio_update)}%)")
elif trigo_MUNDO_Total_Producao_novo_relatorio_update < trigo_MUNDO_Total_Producao_novo_relatorio_compara:
    piscas.append(f"--trigo: USDA reduz projeção de produção global em {safra_desejada} para {trigo_MUNDO_Total_Producao_novo_relatorio_update} milhões de t ({porcento(trigo_MUNDO_Total_Producao_novo_relatorio_compara, trigo_MUNDO_Total_Producao_novo_relatorio_update)}%)")
else:
    piscas.append(f"--trigo: USDA mantém projeção de produção global em {safra_desejada} em {trigo_MUNDO_Total_Producao_novo_relatorio_update} milhões de t")


###Algodao Mundo

algodao_MUNDO_novo_relatorio = xpto_novo_relatorio.sr27
arruma_html(algodao_MUNDO_novo_relatorio)

algodao_MUNDO_Total_novo_relatorio_update = algodao_MUNDO_novo_relatorio.find("matrix2").find("m1_region_group2", {"region2":"World"})


#Estoque Final

algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update = float(algodao_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-1].find("m1_attribute_group2", {"attribute2":"Ending Stocks"}).find("cell")["cell_value2"].split(" ")[0])
algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_compara = float(algodao_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-2].find("m1_attribute_group2", {"attribute2":"Ending Stocks"}).find("cell")["cell_value2"].split(" ")[0])


safra_desejada = str(algodao_MUNDO_novo_relatorio.find("matrix2")["region_header2"].split(" ")[0])

if algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update > algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--algodao: USDA eleva projeção de estoque final global em {safra_desejada} para {algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de fardos ({porcento(algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
elif algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update < algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_compara:
    piscas.append(f"--algodao: USDA reduz projeção de estoque final global em {safra_desejada} para {algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de fardos ({porcento(algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_compara, algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update)}%)")
else:
    piscas.append(f"--algodao: USDA mantém projeção de estoque final global em {safra_desejada} em {algodao_MUNDO_Total_EstoqueFinal_novo_relatorio_update} milhões de fardos")

#Produção

algodao_MUNDO_Total_Producao_novo_relatorio_update = float(algodao_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-1].find("m1_attribute_group2", {"attribute2":"Production"}).find("cell")["cell_value2"].split(" ")[0])
algodao_MUNDO_Total_Producao_novo_relatorio_compara = float(algodao_MUNDO_Total_novo_relatorio_update.findAll("m1_month_group2")[-2].find("m1_attribute_group2", {"attribute2":"Production"}).find("cell")["cell_value2"].split(" ")[0])


safra_desejada = str(algodao_MUNDO_novo_relatorio.find("matrix2")["region_header2"].split(" ")[0])

if algodao_MUNDO_Total_Producao_novo_relatorio_update > algodao_MUNDO_Total_Producao_novo_relatorio_compara:
    piscas.append(f"--algodao: USDA eleva projeção de produção global em {safra_desejada} para {algodao_MUNDO_Total_Producao_novo_relatorio_update} milhões de fardos ({porcento(algodao_MUNDO_Total_Producao_novo_relatorio_compara, algodao_MUNDO_Total_Producao_novo_relatorio_update)}%)")
elif algodao_MUNDO_Total_Producao_novo_relatorio_update < algodao_MUNDO_Total_Producao_novo_relatorio_compara:
    piscas.append(f"--algodao: USDA reduz projeção de produção global em {safra_desejada} para {algodao_MUNDO_Total_Producao_novo_relatorio_update} milhões de fardos ({porcento(algodao_MUNDO_Total_Producao_novo_relatorio_compara, algodao_MUNDO_Total_Producao_novo_relatorio_update)}%)")
else:
    piscas.append(f"--algodao: USDA mantém projeção de produção global em {safra_desejada} em {algodao_MUNDO_Total_Producao_novo_relatorio_update} milhões de fardos")

for item in piscas:
    print(item)


if ativar_email == True:
    msg = "Segue lista com os piscas, \n\n\n"
    for linha in piscas:
        msg+= f"{linha}\n"

    import smtplib

    gmail_sender = '{seu_endereço}'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('seu_endereço', 'sua_senha')

    para = 'destinatario'
    corpo = msg.encode('utf8')

    server.sendmail(gmail_sender, para, corpo)
    server.quit()
##ProjetoUSDA

    O Departamento de Agricultura dos Estados Unidos (USDA) divulga, mensalmente, o World Agricultural Supply and Demand Estimates, com perspectivas de oferta e demanda para a safra global e norte-americana de diversas commodities agrícolas (como soja, milho, trigo e algodão). 

    Agilidade e precisão na divulgação dos dados são fundamentais para os leitores de serviço em tempo real (como Bloomberg, Reuters e Broadcast), que precisam dessas informações para operar no mercado financeiro. O programa foi desenvolvido para automatizar a publicação dos principais pontos do relatório. 

    A cada mês, a agência faz modificações nas suas previsões de safra, que podem ser alteradas ou mantida na comparação com o relatório do mês imediatamente anterior. 
    
    Os relatórios podem ser encontrados no link: http://usda.mannlib.cornell.edu/MannUsda/viewDocumentInfo.do?documentID=1194

#Como usar

    Para conseguir baixar os dados dos relatórios, basta rodar o programa e digitar a data do documento desejado (datas podem ser encontradas no link acima). 

    Precisa ser no formato mês, dia e ano (xx-xx-xxxx) / separado com "-"

    Por fim, é possível ativar a função de enviar os resultados por e-mail. É preciso fornecer conta Gmail para conseguir enviar.

    PS: O USDA passou a divulgar os dados no formato XML (formato utilizado para baixar a base) a partir de 2010. Logo, resultados mais antigos não podem ser capturados por este programa.

#Novo relatório

	Além de puxar os dados de relatórios anteior, o programa foi desenvolvido para procurar pelo novo relatório. Basta ligá-lo próximo do horário da publicação e digitar a data do dia. O programa vai ficar procurando o documento e, quando ele for divulgado e já estiver disponível no site do USDA, realizará o restante do processo. 

#Modelo de resposta

--Soja/EUA: USDA eleva projeção de estoque final em 2017/18 para 445 milhões de bushels (4,71%)
--Soja/EUA: USDA mantém projeção de produção em 2017/18 em 4.425 bilhões de bushels
--Soja/EUA: USDA reduz projeção de consumo em 2017/18 para 4.306 bilhões de bushels (-0,46%)
--Soja/EUA: USDA mantém projeção de rendimento em 2017/18 em 49.5 bushels/acre
--milho/EUA: USDA reduz projeção de estoque final em 2017/18 para 2.437 bilhões de bushels (-2,01%)
--milho/EUA: USDA mantém projeção de produção em 2017/18 em 14.578 bilhões de bushels
--milho/EUA: USDA eleva projeção de consumo em 2017/18 para 14.485 bilhões de bushels (0,35%)
--milho/EUA: USDA mantém projeção de rendimento em 2017/18 em 175.4 bushels/acre
--trigo/EUA: USDA eleva projeção de estoque final em 2017/18 para 960.0 milhões de bushels (2,67%)


#Dados disponíveis

	O programa vai buscar as seguintes projeções, comparando porcentualmente com a estimativa divulgada no relatório anterior:
	-EUA
		- Soja EUA:
			- Estoques
			- Produção
			- Consumo
			- Rendimentos
		- Milho EUA:
			- Estoques
			- Produção
			- Consumo
			- Rendimentos
		- Trigo EUA:
			- Estoques
			- Produção
			- Consumo
			- Rendimentos
		- Algodão EUA:
			- Estoques
			- Produção
			- Consumo
			- Rendimentos
	-Mundo
		- Soja
			- Estoque final global
			- Consumo global
			- China
				- Importação
			- Brasil
				- Exportação
			- Argentina
				- Produção
		- Milho
			- Estoque final global
			- Produção global
			- Argentina
				- Produção
		- Trigo
			- Estoque final global
			- Produção global
		- Algodão
			- Estoque final global
			- Produção global

#Dúvidas? 

e-mail para:
cfc.jornalista@gmail.com

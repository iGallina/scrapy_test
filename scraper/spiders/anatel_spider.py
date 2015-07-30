import scrapy
import time
import re

class AnatelSpider(scrapy.Spider):
	name = "anatel"
	http_quinhentos = []
	allowed_domains = ["http://sistemas.anatel.gov.br"]
	url = "http://sistemas.anatel.gov.br/siacco/_Novo_Siacco/Relatorios/PerfilDasEmpresas/tela.asp?acao=w&indtiposociedade=An%F4nima&chave="

	def is_cpf_cnpj(lixo, number):
		cpf_cnpj = ''.join(re.findall("\d", number.strip()))
		if len(cpf_cnpj) == 11 or len(cpf_cnpj) == 14:
			return 1
		else:
			return 0

	def parse(self, response):
		count = 0
		if response.css('.campoesquerda > label:nth-child(1)::text') == 'Erro inesperado, entre em contato com o administrador do sistema.':
			print('<<erro>>')
			time.sleep(1)
			Request(response.url[:243], callback=self.parse)
		else:
			for sel in response.css('#divconsulta table'):
				table_len = len(sel.css('th'))
				tds = sel.css('tr td::text').extract()
				if table_len in [3,4,6]:
					if self.is_cpf_cnpj(tds[0]):
						print tds[0].strip()
				    #tds = sel.css('tr td::text').extract()
					#if len(tds) > 1:
						#print tds[0].strip() +  " " + tds[1].strip() 
				## table = sel.css('label::text').extract()
				count = count + 1
				## print table

	def generate_urls(url, parameters):
		urls = []
		for parameter in parameters:
			urls.append(url+parameter) 
		return urls

	def read_file():
		f = open('input2.txt', 'r')
		lines = []
		for line in f:
			lines.append(line.rstrip())
		return lines

	start_urls = generate_urls(url, read_file())


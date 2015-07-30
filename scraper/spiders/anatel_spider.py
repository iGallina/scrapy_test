import scrapy
import time
import re
import pymssql

class AnatelSpider(scrapy.Spider):
	server = "10.209.64.146:1433"
	user = "usr_grafo"
	password = "pwd_grafo"
	conn = pymssql.connect(server, user, password, "GRAFO")

	name = "anatel"
	allowed_domains = ["http://sistemas.anatel.gov.br"]
	url = "http://sistemas.anatel.gov.br/siacco/_Novo_Siacco/Relatorios/PerfilDasEmpresas/tela.asp?acao=w&indtiposociedade=An%F4nima&chave="
	current_cnpj = 0
	def get_digits(garbage, number):
		cpf_cnpj = ''.join(re.findall("\d", number.strip()))
		return cpf_cnpj

	def parse(self, response):
		count = 0
		if response.css('.campoesquerda > label:nth-child(1)::text') == 'Erro inesperado, entre em contato com o administrador do sistema.':
			print('<<erro>>')
			time.sleep(1)
			Request(response.url[:243], callback=self.parse)
		else:
			fs = open("quadro_societarios.txt", "ab")
			fd = open("quadro_diretivos.txt", "ab")
			for sel in response.css('#divconsulta table'):
				table_len = len(sel.css('th'))
				trs = sel.css('tr')
				for tr in trs:
					tds = tr.css('td::text').extract()
					if len(tds):
						# Socio
						if count == 4:
							fs.write(self.get_digits(tds[0].encode('utf-8')) + "," + tds[1].encode('utf-8').strip() + "," + self.vector[self.current_cnpj] + "\n")
						# Diretoria
						elif count == 9:
							fd.write(self.get_digits(tds[0].encode('utf-8')) + "," + tds[1].encode('utf-8').strip() + "," + self.vector[self.current_cnpj] + "\n")
				count = count + 1
			fs.close()
			fd.close()
			self.current_cnpj = self.current_cnpj + 1

	def generate_urls(url, parameters):
		urls = []
		for parameter in parameters:
			urls.append(url+parameter) 
		return urls

	def read_file():
		f = open('input.txt', 'r')
		lines = []
		for line in f:
			lines.append(line.rstrip())
		return lines

	start_urls = generate_urls(url, read_file())
	vector = read_file()

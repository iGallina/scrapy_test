import scrapy
import time

class AnatelSpider(scrapy.Spider):
	name = "anatel"
	http_quinhentos = []
	allowed_domains = ["http://sistemas.anatel.gov.br"]
	url = "http://sistemas.anatel.gov.br/siacco/_Novo_Siacco/Relatorios/PerfilDasEmpresas/tela.asp?acao=w&indtiposociedade=An%F4nima&chave="

	def parse(self, response):
		count = 0
		if response.css('.campoesquerda > label:nth-child(1)::text') == 'Erro inesperado, entre em contato com o administrador do sistema.':
			print('<<erro>>')
			time.sleep(1)
			Request(response.url[:243], callback=self.parse)
		else:
			for sel in response.css('#divconsulta table'):
				if count == 4:
					tds = sel.css('tr td::text').extract()
					for td in tds:
						print td.strip()
				## table = sel.css('label::text').extract()
				count = count + 1
				## print table
		print("PAGE: %d" % count)


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

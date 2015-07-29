import scrapy

class AnatelSpider(scrapy.Spider):
	name = "anatel"
	allowed_domains = ["http://sistemas.anatel.gov.br"]
	url = "http://sistemas.anatel.gov.br/siacco/_Novo_Siacco/Relatorios/PerfilDasEmpresas/tela.asp?acao=w&indtiposociedade=An%F4nima&chave="
	start_urls = return_url(url, read_file())

	def parse(self, response):
		filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
    
    def generate_urls(url, parameters):
    	urls = []
    	for parameter in parameters:
    		urls.append(url+parameter) 
    	return urls

    def read_file():
    	f = open('input.txt', 'r')
    	lines = []
    	for line in f:
        	lines.append(line)
        return lines

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregar variaveis de ambiente
load_dotenv()

class WeatherExtractor:
    """Classe responsavel pela extracao de dados da API OpenWeatherMap"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        if not self.api_key:
            raise ValueError("API Key do OpenWeatherMap nao encontrada no arquivo .env")
    
    def extrair_dados_cidade(self, cidade, pais='BR'):
        """
        Extrai dados climaticos de uma cidade especifica
        
        Args:
            cidade (str): Nome da cidade
            pais (str): Codigo do pais (padrao: BR)
            
        Returns:
            dict: Dados climaticos extraidos ou None em caso de erro
        """
        try:
            # Parametros da requisicao
            params = {
                'q': f'{cidade},{pais}',
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            # Fazer requisicao
            print(f"Buscando dados climaticos de {cidade}...")
            response = requests.get(self.base_url, params=params, timeout=10)
            
            # Verificar se foi bem-sucedido
            response.raise_for_status()
            
            # Processar resposta
            dados = response.json()
            
            dados_estruturados = {
                'cidade': dados['name'],
                'pais': dados['sys']['country'],
                'latitude': dados['coord']['lat'],
                'longitude': dados['coord']['lon'],
                'temperatura': dados['main']['temp'],
                'sensacao_termica': dados['main']['feels_like'],
                'temperatura_min': dados['main']['temp_min'],
                'temperatura_max': dados['main']['temp_max'],
                'pressao': dados['main']['pressure'],
                'umidade': dados['main']['humidity'],
                'velocidade_vento': dados['wind']['speed'],
                'direcao_vento': dados['wind'].get('deg', None),
                'nebulosidade': dados['clouds']['all'],
                'descricao_clima': dados['weather'][0]['description'],
                'data_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"Dados de {cidade} extraidos com sucesso!")
            return dados_estruturados
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados de {cidade}: {e}")
            return None
        except KeyError as e:
            print(f"Erro ao processar resposta da API: {e}")
            return None
    
    def extrair_multiplas_cidades(self, cidades):
        """
        Extrai dados de multiplas cidades
        
        Args:
            cidades (list): Lista de tuplas (cidade, pais)
            
        Returns:
            list: Lista de dicionarios com dados extraidos
        """
        resultados = []
        
        for cidade, pais in cidades:
            dados = self.extrair_dados_cidade(cidade, pais)
            if dados:
                resultados.append(dados)
        
        print(f"\nTotal de cidades extraidas: {len(resultados)}/{len(cidades)}")
        return resultados


# Funcao para testar o extrator
if __name__ == "__main__":
    # Testar extracao
    extractor = WeatherExtractor()
    
    # Lista de cidades para extrair
    cidades = [
        ('Recife', 'BR'),
        ('Sao Paulo', 'BR'),
        ('Rio de Janeiro', 'BR'),
        ('Brasilia', 'BR')
    ]
    
    # Extrair dados
    dados = extractor.extrair_multiplas_cidades(cidades)
    
    # Mostrar resultado de uma cidade como exemplo
    if dados:
        print("\n" + "="*50)
        print("Exemplo de dados extraidos (primeira cidade):")
        print("="*50)
        for chave, valor in dados[0].items():
            print(f"{chave}: {valor}")
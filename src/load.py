import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

# Carregar variaveis de ambiente
load_dotenv()

class WeatherLoader:
    """Classe responsavel pela carga de dados no Supabase"""
    
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            raise ValueError("Credenciais do Supabase nao encontradas no arquivo .env")
        
        self.supabase: Client = create_client(url, key)
        print("Conexao com Supabase estabelecida!")
    
    def inserir_cidade(self, cidade, pais, latitude, longitude):
        """
        Insere uma cidade na tabela dim_cidades se nao existir
        
        Args:
            cidade (str): Nome da cidade
            pais (str): Codigo do pais
            latitude (float): Latitude
            longitude (float): Longitude
            
        Returns:
            int: ID da cidade inserida ou existente
        """
        try:
            # Verificar se cidade ja existe
            response = self.supabase.table('dim_cidades')\
                .select('id_cidade')\
                .eq('nome_cidade', cidade)\
                .eq('pais', pais)\
                .execute()
            
            if response.data:
                # Cidade ja existe
                return response.data[0]['id_cidade']
            
            # Inserir nova cidade
            nova_cidade = {
                'nome_cidade': cidade,
                'pais': pais,
                'latitude': latitude,
                'longitude': longitude
            }
            
            response = self.supabase.table('dim_cidades')\
                .insert(nova_cidade)\
                .execute()
            
            print(f"Cidade {cidade} inserida com sucesso!")
            return response.data[0]['id_cidade']
            
        except Exception as e:
            print(f"Erro ao inserir cidade {cidade}: {e}")
            return None
    
    def inserir_dados_clima(self, df):
        """
        Insere dados climaticos na tabela fato_clima
        
        Args:
            df (pandas.DataFrame): DataFrame com dados transformados
            
        Returns:
            int: Numero de registros inseridos
        """
        if df.empty:
            print("Nenhum dado para carregar!")
            return 0
        
        registros_inseridos = 0
        
        print(f"\nIniciando carga de {len(df)} registros...")
        
        for index, row in df.iterrows():
            try:
                # Inserir ou obter ID da cidade
                id_cidade = self.inserir_cidade(
                    row['cidade'],
                    row['pais'],
                    row['latitude'],
                    row['longitude']
                )
                
                if not id_cidade:
                    print(f"Erro ao obter ID da cidade {row['cidade']}")
                    continue
                
                # Preparar dados do clima
                dados_clima = {
                    'id_cidade': id_cidade,
                    'data_coleta': row['data_coleta'],
                    'temperatura': float(row['temperatura']),
                    'sensacao_termica': float(row['sensacao_termica']),
                    'temperatura_min': float(row['temperatura_min']),
                    'temperatura_max': float(row['temperatura_max']),
                    'pressao': int(row['pressao']),
                    'umidade': int(row['umidade']),
                    'velocidade_vento': float(row['velocidade_vento']),
                    'direcao_vento': int(row['direcao_vento']) if pd.notna(row['direcao_vento']) else None,
                    'nebulosidade': int(row['nebulosidade']),
                    'descricao_clima': row['descricao_clima']
                }
                
                # Inserir dados do clima
                self.supabase.table('fato_clima').insert(dados_clima).execute()
                
                registros_inseridos += 1
                print(f"Dados de {row['cidade']} carregados! ({registros_inseridos}/{len(df)})")
                
            except Exception as e:
                print(f"Erro ao inserir dados de {row['cidade']}: {e}")
                continue
        
        print(f"\nCarga concluida! {registros_inseridos}/{len(df)} registros inseridos.")
        return registros_inseridos
    
    def verificar_dados(self):
        """
        Verifica quantos registros existem nas tabelas
        
        Returns:
            dict: Dicionario com contagem de registros
        """
        try:
            # Contar cidades
            cidades = self.supabase.table('dim_cidades').select('*', count='exact').execute()
            
            # Contar registros de clima
            clima = self.supabase.table('fato_clima').select('*', count='exact').execute()
            
            resultado = {
                'total_cidades': cidades.count,
                'total_registros_clima': clima.count
            }
            
            print("\n" + "="*50)
            print("DADOS NO BANCO")
            print("="*50)
            print(f"Total de cidades: {resultado['total_cidades']}")
            print(f"Total de registros climaticos: {resultado['total_registros_clima']}")
            print("="*50 + "\n")
            
            return resultado
            
        except Exception as e:
            print(f"Erro ao verificar dados: {e}")
            return {}


# Funcao para testar o loader
if __name__ == "__main__":
    print("Testando o modulo de carga...")
    print("="*60)
    
    # Carregar dados transformados do CSV
    df = pd.read_csv('dados_transformados.csv')
    print(f"Carregados {len(df)} registros do arquivo CSV")
    
    # Criar loader e carregar dados
    loader = WeatherLoader()
    loader.inserir_dados_clima(df)
    
    # Verificar dados no banco
    loader.verificar_dados()
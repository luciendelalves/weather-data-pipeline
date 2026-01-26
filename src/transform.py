import pandas as pd
from datetime import datetime

class WeatherTransformer:
    """Classe responsavel pela transformacao e limpeza dos dados climaticos"""
    
    def __init__(self):
        pass
    
    def validar_temperatura(self, temp):
        """
        Valida se a temperatura esta em um range razoavel
        
        Args:
            temp: Temperatura em Celsius
            
        Returns:
            bool: True se valida, False caso contrario
        """
        if temp is None:
            return False
        # Temperatura entre -50 e 60 graus Celsius (extremos mundiais)
        return -50 <= temp <= 60
    
    def validar_umidade(self, umidade):
        """
        Valida se a umidade esta entre 0 e 100%
        
        Args:
            umidade: Umidade relativa em %
            
        Returns:
            bool: True se valida, False caso contrario
        """
        if umidade is None:
            return False
        return 0 <= umidade <= 100
    
    def validar_pressao(self, pressao):
        """
        Valida se a pressao atmosferica esta em um range razoavel
        
        Args:
            pressao: Pressao em hPa
            
        Returns:
            bool: True se valida, False caso contrario
        """
        if pressao is None:
            return False
        # Pressao entre 870 e 1085 hPa (extremos registrados)
        return 870 <= pressao <= 1085
    
    def transformar_dados(self, dados_brutos):
        """
        Transforma e valida os dados extraidos
        
        Args:
            dados_brutos (list): Lista de dicionarios com dados brutos
            
        Returns:
            pandas.DataFrame: DataFrame com dados limpos e validados
        """
        if not dados_brutos:
            print("Nenhum dado para transformar!")
            return pd.DataFrame()
        
        # Converter para DataFrame
        df = pd.DataFrame(dados_brutos)
        
        print(f"\nIniciando transformacao de {len(df)} registros...")
        
        # Registros antes da limpeza
        total_inicial = len(df)
        
        # Validar temperaturas
        df_valido = df[df['temperatura'].apply(self.validar_temperatura)]
        removidos_temp = total_inicial - len(df_valido)
        if removidos_temp > 0:
            print(f"Removidos {removidos_temp} registros com temperatura invalida")
        
        # Validar umidade
        df_valido = df_valido[df_valido['umidade'].apply(self.validar_umidade)]
        removidos_umidade = total_inicial - removidos_temp - len(df_valido)
        if removidos_umidade > 0:
            print(f"Removidos {removidos_umidade} registros com umidade invalida")
        
        # Validar pressao
        df_valido = df_valido[df_valido['pressao'].apply(self.validar_pressao)]
        removidos_pressao = total_inicial - removidos_temp - removidos_umidade - len(df_valido)
        if removidos_pressao > 0:
            print(f"Removidos {removidos_pressao} registros com pressao invalida")
        
        # Remover duplicatas (mesma cidade e horario muito proximo)
        df_valido = df_valido.drop_duplicates(subset=['cidade', 'pais'], keep='last')
        
        # Padronizar nomes de cidades (capitalizar)
        df_valido['cidade'] = df_valido['cidade'].str.title()
        
        # Garantir que descricao_clima nao seja nula
        df_valido['descricao_clima'] = df_valido['descricao_clima'].fillna('Sem descricao')
        
        # Arredondar valores numericos
        colunas_numericas = ['temperatura', 'sensacao_termica', 'temperatura_min', 
                            'temperatura_max', 'velocidade_vento']
        for col in colunas_numericas:
            df_valido[col] = df_valido[col].round(2)
        
        # Ordenar por cidade
        df_valido = df_valido.sort_values('cidade').reset_index(drop=True)
        
        print(f"Transformacao concluida!")
        print(f"Registros validos: {len(df_valido)}/{total_inicial}")
        
        return df_valido
    
    def gerar_estatisticas(self, df):
        """
        Gera estatisticas basicas dos dados transformados
        
        Args:
            df (pandas.DataFrame): DataFrame com dados transformados
            
        Returns:
            dict: Dicionario com estatisticas
        """
        if df.empty:
            return {}
        
        estatisticas = {
            'total_registros': len(df),
            'temperatura_media': df['temperatura'].mean(),
            'temperatura_min': df['temperatura'].min(),
            'temperatura_max': df['temperatura'].max(),
            'umidade_media': df['umidade'].mean(),
            'cidades_unicas': df['cidade'].nunique(),
            'lista_cidades': df['cidade'].unique().tolist()
        }
        
        return estatisticas
    
    def exibir_resumo(self, df):
        """
        Exibe um resumo dos dados transformados
        
        Args:
            df (pandas.DataFrame): DataFrame com dados transformados
        """
        if df.empty:
            print("\nNenhum dado para exibir!")
            return
        
        print("\n" + "="*60)
        print("RESUMO DOS DADOS TRANSFORMADOS")
        print("="*60)
        
        stats = self.gerar_estatisticas(df)
        
        print(f"\nTotal de registros: {stats['total_registros']}")
        print(f"Cidades unicas: {stats['cidades_unicas']}")
        print(f"Cidades: {', '.join(stats['lista_cidades'])}")
        print(f"\nTemperatura media: {stats['temperatura_media']:.2f}°C")
        print(f"Temperatura minima: {stats['temperatura_min']:.2f}°C")
        print(f"Temperatura maxima: {stats['temperatura_max']:.2f}°C")
        print(f"Umidade media: {stats['umidade_media']:.1f}%")
        
        print("\n" + "="*60)
        print("PREVIEW DOS DADOS (primeiras 3 linhas):")
        print("="*60)
        print(df[['cidade', 'temperatura', 'umidade', 'descricao_clima']].head(3).to_string(index=False))
        print("="*60 + "\n")


# Funcao para testar o transformer
if __name__ == "__main__":
    # Importar o extractor para pegar dados reais
    from extract import WeatherExtractor
    
    print("Testando o modulo de transformacao...")
    print("="*60)
    
    # Extrair dados
    extractor = WeatherExtractor()
    cidades = [
        ('Recife', 'BR'),
        ('Sao Paulo', 'BR'),
        ('Rio de Janeiro', 'BR'),
        ('Brasilia', 'BR'),
        ('Salvador', 'BR')
    ]
    
    dados_brutos = extractor.extrair_multiplas_cidades(cidades)
    
    # Transformar dados
    transformer = WeatherTransformer()
    df_transformado = transformer.transformar_dados(dados_brutos)
    
    # Exibir resumo
    transformer.exibir_resumo(df_transformado)
    
    # Salvar para verificacao
    print("Salvando dados transformados em 'dados_transformados.csv'...")
    df_transformado.to_csv('dados_transformados.csv', index=False)
    print("Arquivo salvo com sucesso!")
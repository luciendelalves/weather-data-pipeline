from extract import WeatherExtractor
from transform import WeatherTransformer
from load import WeatherLoader
from datetime import datetime
import sys

class WeatherPipeline:
    """Pipeline completo de ETL para dados climaticos"""
    
    def __init__(self):
        self.extractor = WeatherExtractor()
        self.transformer = WeatherTransformer()
        self.loader = WeatherLoader()
    
    def executar(self, cidades):
        """
        Executa o pipeline completo de ETL
        
        Args:
            cidades (list): Lista de tuplas (cidade, pais)
            
        Returns:
            dict: Resultado da execucao
        """
        print("\n" + "="*70)
        print("WEATHER DATA PIPELINE - INICIANDO")
        print("="*70)
        print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Cidades a processar: {len(cidades)}")
        print("="*70 + "\n")
        
        resultado = {
            'sucesso': False,
            'registros_extraidos': 0,
            'registros_transformados': 0,
            'registros_carregados': 0,
            'erros': []
        }
        
        try:
            # ETAPA 1: EXTRACT
            print("\n" + "-"*70)
            print("ETAPA 1/3: EXTRACAO DE DADOS")
            print("-"*70)
            
            dados_brutos = self.extractor.extrair_multiplas_cidades(cidades)
            resultado['registros_extraidos'] = len(dados_brutos)
            
            if not dados_brutos:
                resultado['erros'].append("Nenhum dado foi extraido")
                return resultado
            
            print(f"\nResultado: {len(dados_brutos)} registros extraidos com sucesso!")
            
            # ETAPA 2: TRANSFORM
            print("\n" + "-"*70)
            print("ETAPA 2/3: TRANSFORMACAO E VALIDACAO")
            print("-"*70)
            
            df_transformado = self.transformer.transformar_dados(dados_brutos)
            resultado['registros_transformados'] = len(df_transformado)
            
            if df_transformado.empty:
                resultado['erros'].append("Nenhum dado passou pela validacao")
                return resultado
            
            # Exibir resumo da transformacao
            self.transformer.exibir_resumo(df_transformado)
            
            # ETAPA 3: LOAD
            print("\n" + "-"*70)
            print("ETAPA 3/3: CARGA NO BANCO DE DADOS")
            print("-"*70)
            
            registros_carregados = self.loader.inserir_dados_clima(df_transformado)
            resultado['registros_carregados'] = registros_carregados
            
            # Verificar dados no banco
            self.loader.verificar_dados()
            
            # Pipeline concluido com sucesso
            resultado['sucesso'] = True
            
            # RESUMO FINAL
            print("\n" + "="*70)
            print("PIPELINE CONCLUIDO COM SUCESSO!")
            print("="*70)
            print(f"Registros extraidos: {resultado['registros_extraidos']}")
            print(f"Registros transformados: {resultado['registros_transformados']}")
            print(f"Registros carregados: {resultado['registros_carregados']}")
            print(f"Taxa de sucesso: {(resultado['registros_carregados']/len(cidades)*100):.1f}%")
            print("="*70 + "\n")
            
        except Exception as e:
            resultado['erros'].append(f"Erro critico no pipeline: {str(e)}")
            print(f"\nERRO CRITICO: {e}")
            print("Pipeline interrompido!")
            
        return resultado


def main():
    """Funcao principal para executar o pipeline"""
    
    # Lista de cidades para monitorar
    cidades = [
        ('Recife', 'BR'),
        ('Sao Paulo', 'BR'),
        ('Rio de Janeiro', 'BR'),
        ('Brasilia', 'BR'),
        ('Salvador', 'BR'),
        ('Fortaleza', 'BR'),
        ('Belo Horizonte', 'BR'),
        ('Curitiba', 'BR'),
        ('Porto Alegre', 'BR'),
        ('Manaus', 'BR')
    ]
    
    # Criar e executar pipeline
    pipeline = WeatherPipeline()
    resultado = pipeline.executar(cidades)
    
    # Retornar codigo de saida
    if resultado['sucesso']:
        print("Pipeline finalizado com sucesso!")
        sys.exit(0)
    else:
        print("Pipeline finalizado com erros:")
        for erro in resultado['erros']:
            print(f"  - {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()
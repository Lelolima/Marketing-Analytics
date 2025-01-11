import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
from datetime import datetime
import os
import json
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

class MarketingAnalyticsPipeline:
    def __init__(self, config_path=None):
        """
        Inicializa a pipeline com configurações
        """
        # Configurar logging
        self.setup_logging()
        
        # Carregar configurações
        self.config = self.load_config(config_path)
        
        # Inicializar conexão com banco de dados
        self.db_engine = self.init_database()
        
        # Inicializar processador de dados
        self.scaler = StandardScaler()
        
    def setup_logging(self):
        """
        Configura sistema de logging
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('marketing_pipeline.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('MarketingPipeline')

    def load_config(self, config_path):
        """
        Carrega configurações do sistema
        """
        default_config = {
            'database_url': 'sqlite:///marketing_analytics.db',
            'data_source': 'data/leads.csv',
            'export_path': 'output/',
            'profile_mapping': {
                'Transição de carreira': 'C1',
                'Estudante': 'D1',
                'Sem experiência': 'E1',
                'Profissional': 'P1'
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config

    def init_database(self):
        """
        Inicializa conexão com banco de dados
        """
        try:
            return create_engine(self.config['database_url'])
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def extract_data(self, source=None):
        """
        Extrai dados da fonte especificada
        """
        self.logger.info("Iniciando extração de dados")
        
        try:
            # Dados simulados para demonstração
            data = {
                'id': range(1, 101),
                'idade': np.random.randint(18, 60, 100),
                'perfil': np.random.choice(
                    ['Transição de carreira', 'Estudante', 'Sem experiência', 'Profissional'],
                    100
                ),
                'recursos_disponiveis': np.random.choice([True, False], 100),
                'preferencia_pagamento': np.random.choice(
                    ['PIX', 'Cartão', 'Boleto', 'Parcelado'],
                    100
                ),
                'valor_investimento': np.random.uniform(1000, 5000, 100),
                'tempo_decisao_dias': np.random.randint(1, 30, 100)
            }
            
            df = pd.DataFrame(data)
            self.logger.info(f"Extraídos {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro na extração de dados: {e}")
            raise

    def transform_data(self, df):
        """
        Aplica transformações nos dados
        """
        self.logger.info("Iniciando transformação dos dados")
        
        try:
            # Categorização de perfis
            df['categoria'] = df['perfil'].map(self.config['profile_mapping'])
            
            # Análise de faixa etária
            df['faixa_etaria'] = pd.cut(
                df['idade'],
                bins=[17, 25, 35, 45, 60],
                labels=['18-25', '26-35', '36-45', '46-60']
            )
            
            # Score de potencial
            df['score_potencial'] = (
                (df['recursos_disponiveis'].astype(int) * 0.4) +
                (df['valor_investimento'].apply(lambda x: min(x/5000, 1)) * 0.4) +
                (1 - (df['tempo_decisao_dias'] / 30) * 0.2)
            )
            
            # Normalização de valores numéricos
            num_cols = ['valor_investimento', 'tempo_decisao_dias']
            df[num_cols] = self.scaler.fit_transform(df[num_cols])
            
            # Análise de segmentação
            df['segmento'] = df.apply(self.categorizar_segmento, axis=1)
            
            self.logger.info("Transformação concluída com sucesso")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro na transformação dos dados: {e}")
            raise

    def categorizar_segmento(self, row):
        """
        Categoriza leads em segmentos
        """
        if row['score_potencial'] >= 0.8:
            return 'Premium'
        elif row['score_potencial'] >= 0.5:
            return 'Intermediário'
        else:
            return 'Básico'

    def analyze_data(self, df):
        """
        Realiza análises nos dados transformados
        """
        self.logger.info("Iniciando análise dos dados")
        
        analysis = {
            'total_leads': len(df),
            'distribuicao_perfis': df['perfil'].value_counts().to_dict(),
            'media_idade': df['idade'].mean(),
            'distribuicao_segmentos': df['segmento'].value_counts().to_dict(),
            'score_medio': df['score_potencial'].mean(),
            'preferencia_pagamento': df['preferencia_pagamento'].value_counts().to_dict()
        }
        
        # Gerar visualizações
        self.generate_visualizations(df)
        
        return analysis

    def generate_visualizations(self, df):
        """
        Gera visualizações dos dados
        """
        # Configuração visual
        plt.style.use('seaborn')
        
        # Distribuição de scores
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='score_potencial', hue='segmento')
        plt.title('Distribuição de Scores por Segmento')
        plt.savefig('output/score_distribution.png')
        
        # Relação idade vs valor
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='idade', y='valor_investimento', hue='segmento')
        plt.title('Idade vs Valor de Investimento')
        plt.savefig('output/age_value_relation.png')

    def load_data(self, df):
        """
        Carrega dados processados
        """
        self.logger.info("Iniciando carregamento dos dados")
        
        try:
            # Salvar no banco de dados
            df.to_sql('leads_processed', self.db_engine, if_exists='replace', index=False)
            
            # Exportar análises
            analysis = self.analyze_data(df)
            with open('output/analysis_report.json', 'w') as f:
                json.dump(analysis, f, indent=4)
            
            self.logger.info("Dados carregados com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro no carregamento dos dados: {e}")
            raise

    def run_pipeline(self):
        """
        Executa pipeline completa
        """
        self.logger.info("Iniciando pipeline de marketing analytics")
        
        try:
            # Criar diretório de output se não existir
            os.makedirs('output', exist_ok=True)
            
            # Executar pipeline
            data = self.extract_data()
            transformed_data = self.transform_data(data)
            self.load_data(transformed_data)
            
            self.logger.info("Pipeline concluída com sucesso")
            
        except Exception as e:
            self.logger.error(f"Erro na execução da pipeline: {e}")
            raise

if __name__ == "__main__":
    # Executar pipeline
    pipeline = MarketingAnalyticsPipeline()
    pipeline.run_pipeline()

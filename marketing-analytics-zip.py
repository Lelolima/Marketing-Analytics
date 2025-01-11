import zipfile
import os

def criar_projeto_marketing():
    # Criar diretório temporário
    temp_dir = "./marketing_analytics_project"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Definir conteúdo dos arquivos
    files_content = {
        "etl_pipeline.py": """
import pandas as pd
from sqlalchemy import create_engine

class MarketingETL:
    def extract_data(self):
        # Dados de exemplo
        data = {
            'id': [1, 2, 3, 4, 5],
            'idade': [28, 35, 22, 40, 30],
            'perfil': ['Transição de carreira', 'Estudante', 'Sem experiência', 
                      'Transição de carreira', 'Estudante'],
            'recursos_disponiveis': [False, True, False, False, True],
            'preferencia_pagamento': ['PIX', 'Cartão', 'PIX', 'PIX', 'Parcelado']
        }
        return pd.DataFrame(data)

    def transform_data(self, df):
        # Transformações
        df['categoria'] = df['perfil'].map({
            'Transição de carreira': 'C1',
            'Estudante': 'D1',
            'Sem experiência': 'E1'
        })
        df['faixa_etaria'] = pd.cut(df['idade'], 
                                   bins=[18, 25, 35, 55],
                                   labels=['18-25', '25-35', '35-55'])
        return df

    def load_data(self, df):
        # Carregamento em banco SQLite
        engine = create_engine('sqlite:///marketing.db')
        df.to_sql('leads', con=engine, index=False, if_exists='replace')

def main():
    etl = MarketingETL()
    data = etl.extract_data()
    transformed = etl.transform_data(data)
    etl.load_data(transformed)

if __name__ == "__main__":
    main()
""",
        "requirements.txt": """
pandas==2.0.0
sqlalchemy==1.4.46
""",
        ".gitignore": """
*.pyc
__pycache__/
.env
*.db
venv/
""",
        "README.md": """
# Marketing Analytics ETL

Sistema de análise de dados de marketing com pipeline ETL integrada.

## Funcionalidades

- Extração de dados de leads
- Transformação e categorização de perfis
- Carregamento em banco de dados SQLite
- Análise de perfil de clientes

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python etl_pipeline.py
```

## Estrutura

- `etl_pipeline.py`: Pipeline ETL principal
- `requirements.txt`: Dependências
- `.gitignore`: Arquivos ignorados
- `README.md`: Documentação

## Autor
Seu Nome
"""
    }
    
    # Criar arquivos no diretório temporário
    for filename, content in files_content.items():
        with open(os.path.join(temp_dir, filename), 'w') as f:
            f.write(content)
    
    # Criar arquivo ZIP
    zip_path = "marketing_analytics.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname=arc_name)
    
    # Limpar arquivos temporários
    for file in files_content.keys():
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)
    
    return zip_path

if __name__ == "__main__":
    zip_file = criar_projeto_marketing()
    print(f"Projeto criado em: {zip_file}")

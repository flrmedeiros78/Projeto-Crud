import pandas as pd
from utils.fmt_valor import fmt_valor

#--------------------------------------------------- 
#Função : Converte lista de dict para dataframe
#---------------------------------------------------  
def dict_para_dataframe(prods):
  """
  Recebe a lista de Produtos (list de discts) retornada pela API e devolve um Dataframe formatado para visualização
  
  Por que usar pandas :
  - st.dataframe() com DataFrame suporta ordenação clicando na coluna
  - Permite renomear colunas para usuário final
  - É mais performático que loop + st.markdown para centenas de registros
  """
# Cria o DatafRAME a partir da lista de dicionários
  df = pd.DataFrame(prods)
  
# Renomeia as colunas (nomes tecnicos -> nomes legíveis)
  df = df.rename(columns={
    "id": "ID",
    "name": "Nome",
    "descricao": "Descrição",
    "valor": "Valor",
    "categoria": "Categoria",
    "email_fornecedor": "Fornecedor",
    "dt_procs": "Data de Inclusão",
  }).sort_values("ID")
  # Ordena exibição das colunas no GRID do DataFrame
  df = df[["ID", "Nome", "Descrição", "Valor", "Categoria", "Fornecedor", "Data de Inclusão"]]
# Aplica a formatação de moeda na coluna Valor
  df["Valor"] = df["Valor"].apply(fmt_valor)
# Formata a data para dd/mm/aaaa hh:mm
  df["Data de Inclusão"] = pd.to_datetime(df["Data de Inclusão"]).dt.strftime("%d/%m/%Y %H:%M")
# Remove a coluna de Indice interno do DataFrame não vou precisar
  return df.reset_index(drop=True)
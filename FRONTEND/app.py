import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import math
#--------------------------------------------------- 
# URL base da API FastAPI (backend)
#--------------------------------------------------- 
API = "http://localhost:8000"

st.set_page_config(page_title="CRUD Produtos", layout="wide")
st.title("Projeto CRUD de Produtos")

#--------------------------------------------------- 
#Caminho dp arquivo de logo
#--------------------------------------------------- 
#LOGO_PATH = Path(__file__).parent / "assets" / "logo.png"

#--------------------------------------------------- 
# Configuração da página
#--------------------------------------------------- 
# st.set_page_config(
#   page_title="Crud de Produtos", 
#   layout="wide")

#--------------------------------------------------- 
# Carrega e exibe o logo no topo(largura de 120px)
#--------------------------------------------------- 
# if LOGO_PATH.exists():
#   st.image(str(LOGO_PATH),width=120)
# else:
#   st.warning("Logo não encontrado em assets/logo.img")  

# Titulo principal da aplicação
# st.title("Crud de Produtos")
#Linha divisória entre o cabeçalho e o conteúdo
st.divider()

#--------------------------------------------------- 
# Função para pesquisar a API
#--------------------------------------------------- 
def api(method, path, data=None):
  """ 
    Envia uma requisição HTTP para a API FastAPI.
  
  Parâmetros:
    method: 'GET-(Select)', 'POST-(inserir)', 'PUT-(Atualiza)', 'DELETE-(Exclui)'
    path: caminho do endpoint (ex:'/products/')
  
  Retorna: JSON da resposta, ou dict com chave'error' em caso de falha.
  """
  try:
    # requests.request(0) aceita qualquer HTTP
    r = requests.request(method, f"{API}{path}", json=data, timeout=10)
    # Se o status for 4xx/5xx,  HTTPError
    r.raise_for_status()
    # Converte a resposta em bytes para dict/list Python
    return r.json()

  # Backend não está no ar
  except requests.exceptions.ConnectionError:
    st.error("API Indisponível, Verfique se o backend esá rodando")
    st.stop() # para a execução do script

  # Error HTTP(404,422 etc..)
  except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
      return {"error": "Produto não encontrado."}
    if e.response.status_code == 422: # 422 = erro de validação do Pydantic
      return {"error": f"Validação: {e.response.json()}"}
    return {"error": str(e)}

#--------------------------------------------------- 
# FUNÇÃO AUXILIAR: FORMATAR VALOR MONETÁRIO
#--------------------------------------------------- 
def fmt_valor(v):
    """Converte um número para formato brasileiro: 1500.50 -> 'R$ 1.500,50'"""
    num = float(v)
    # Proteção: se o valor é irrealmente grande, não tenta formatar
    if num > 1_000_000_000:  # acima de 1 bilhão, algo está errado
        return "Valor corrompido"
    s = f"{num:,.2f}"
    s = s.replace(",", "x").replace(".", ",").replace("x", ".")
    return f"R$ {s}"
 
def parse_valor(v: str) -> float:
    """'1.500,00' → 1500.00"""
    result = float(v.replace(".", "").replace(",", "."))
    if not math.isfinite(result):
        raise ValueError(f"Valor inválido: '{v}'")
    # Proteção: impede salvar valores absurdos
    if result > 1_000_000_000:
        raise ValueError(f"Valor muito alto: {result:,.2f}")
    return result 
 
 
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


#--------------------------------------------------- 
# Selecina todos os produtos
#--------------------------------------------------- 
# st.expander cria um painel recolhível (a setinha da sua imagem)
# expanded=True faz ele abrir já expandido por padrão
with st.expander("Lista todos os Produtos"):#, expander=True):
  st.subheader("Produto Cadastrado")
  # Botão que carrega a busca
  if st.button("Seleciar Produtos"):
    # Chama a API GET produtos
    prods = api("GET", "/products/")
    # Verifica se a lista de produto existe
    if isinstance(prods, list) and len(prods) > 0:
      st.success(f"({len(prods)}) - Produtos Encontrados")
      
      # Converte para DataFrame e exibe a tabela
      # use_container_width=True -> tabela ocupa 100% da largura
      # hide_index=True -> esconde a coluna de índice
      st.dataframe(
        dict_para_dataframe(prods),
        use_container_width=True,
        hide_index=True,
      )
    else:
      st.info("Nenhum Produto Cadastrado !")

#--------------------------------------------------- 
# Seleciona um produto
#---------------------------------------------------
with st.expander("Visualizar produto por ID", expanded=False):
  # Campo numérico para digiar o ID
  # min_value=1: pois o ID começa do 1 (auto imcremento do banco)
  # step=1 : ID é um inteiro
  pid = st.number_input("Digite o ID do Produto:", min_value=1, step=1)
  # Botão que faz a busca pelo produto
  if st.button("Seleciar Produto"):
    # Chama a API GET produtos
    prod = api("GET", f"/products/{int(pid)}")
    # Se a API retornou erro (404, 422 etc..)
    if "error" in prod:
      st.error(prod["error"])
    # Se retornar com sucesso
    else:
      # mosra num grid
      st.dataframe(dict_para_dataframe([prod]), use_container_width=True, hide_index=True)
      # mostra o formato json
      st.json(prod)

#--------------------------------------------------- 
# Adicionar produto
#---------------------------------------------------
with st.expander("Adicionar produto", expanded=False):
  # st.form : agrupa os campos e só envia quendo o usuário clica em "Enviar"
  # clear_on_submit=True : Limpa os campos após o envio
  with st.form("form_adicionar", clear_on_submit=True):
    #Calunas: 2 campos lado a lado
    col1, col2 = st.columns(2)
    with col1:
      name = st.text_input("Nome *", placeholder="Ex: Violão Tagima T130")
      descricao = st.text_input("Descrição *", placeholder="Descreva o produto")
      valor =st.number_input("Valor *", min_value=0.01, step=0.01, format="%.2f",)
  
    with col2:
      categoria = st.text_input("Categoria *", placeholder="Ex: Cordas")
      email_fornecedor = st.text_input("E-mail do Fronecedor *", placeholder="fornecedor@exemplo.com",)
    
    # Botão de submit : type="primary" par destacar o botão
    enviado = st.form_submit_button("Salvar Produto", type="primary")
    #só executa se clicar no botão
    if enviado:
      #validação básica nenhum campo pode estar vazio:
      if not all([name, descricao, valor, categoria, email_fornecedor]):
        st.error("Preencher todos os campos Obrigatórios.")
      else:
        # requisição POST
        # Valor é uma str pois a API espera Decimal como str
        data = {
          "name": name,
          "descricao": descricao,
          "valor": str(valor),
          "categoria": categoria,
          "email_fornecedor": email_fornecedor,          
        }
        # Chama a API: POST /products/
        res = api("POST", "/products/", data)
        if "error" in res:
          st.error(res["error"])
        else:
          st.success(f"Produto criado com ID: {res["id"]}")
#--------------------------------------------------- 
# Excluir produto 
#---------------------------------------------------
with st.expander("Deletar Produto", expanded=False):
  # Monta lista de todos os produtos
  prods = api("GET","/products")
  #  Verifica se a API retornou erro ou lista vazio
  if not isinstance(prods, list) or len(prods) == 0:
    st.info("Nenhum Produto para Excluir.")
  else:
    # Monta do Dicionário para selecionar produtos
    # chave = testo exibido | valor = ID do produto
    opcoes = {f"ID {p['id']} - {p['name']}": p["id"] for p in prods}
    # Selecbox para o usuário escolher qual produto quer excluir
    sel = st.selectbox("Selecione o Produto:", list(opcoes.keys()))
    pid = opcoes[sel]
    # Mostra o produto antes de excluir
    prod = api("GET",f"/products/{pid}")
    st.text(f"**Nome:** {prod['name']}")
    st.text(f"**Categoria:** {prod['categoria']}")
    st.text(f"**Valor:** {fmt_valor(prod['valor'])}")
    # Aviso de que a ação é irreversível
    st.warning("A exclusão será permanente !")
    # Botão de Confirmação : type="primary" par destacar o botão
    if st.button("Excluir Produto", type="primary"):
      # Chama a API : DELETE /products/{id}
      res = api("DELETE", f"/products/{pid}")
      
      if "error" in res:
        st.error(res['error'])
      else:
        st.success(f"Produto id {pid} excluido com sucesso.")
        # st.rerun() reinicia a o script para atualizar a lista
        # (sem ele, o selectbox ainda mostraria o produto excluído)
        st.rerun()
        
#--------------------------------------------------- 
# Atualizar produto 
#---------------------------------------------------
with st.expander("Atualiza Produto", expanded=False):
  # Busca todos os produtos para selecionar
  prods = api("GET", "/products/")
  if not isinstance(prods, list) or len(prods) == 0:
    st.info("Nenhum produto para atualização")
  else:
    # Monta o dicionário para o selectbox
    opcoes = {f"ID {p['id']} - {p['name']}": p["id"] for p in prods}
    # Seleciona para saber qual produto editar
    sel = st.selectbox("Selecione o produto", list(opcoes.keys()))
    pid = opcoes[sel]
    # Preenche formulário
    prod = api("GET", f"/products/{pid}")
    
    if "error" in prod:
      st.error(prod['error'])
    else:
      #st.form com clear_on_submit=False
      # não limpa os campos após o envio.. caso o usuário queira corrigir algum dado
      with st.form("from_atualizar"):
        col1, col2 = st.columns(2)
        
        with col1:
          name = st.text_input("Nome *", value=prod["name"],)
          descricao = st.text_area("Descrição *", value=prod["descricao"],)
          # Verifica se o valor está corrompido antes de exibir
          _valor_bruto = float(prod["valor"])git stat
          if _valor_bruto > 1_000_000_000:
            valor = st.text_input(
            "valor (R$)*",
            value="",
            help="O valor salvo está corrompido. Digite o valor correto.",
          )
            st.warning("O valor atual no banco está corrompido. Corrija antes de salvar.")
          else:
            valor = st.text_input(
            "valor (R$)*",
            value=fmt_valor(prod["valor"]).replace("R$ ", ""),
            help="Formato: 0.000,00",)
          #valor = st.text_input("valor (R$)*", value=prod["valor"].replace("R$",""), help = "Formato: 0.000,00",)
          
        with col2:
          categoria = st.text_input("Categoria *", value=prod["categoria"],)
          email_fornecedor = st.text_input("Fornecedor *", value=prod["email_fornecedor"],)
          
        # deixa o botão com visibilidade 
        enviado = st.form_submit_button("Atualiza Produto", type="primary")

      if enviado:
        if not all([name, descricao, valor, categoria, categoria, email_fornecedor]):
          st.error("Preencha todos os campos obrigatórios")
        else:
          try:
            val = parse_valor(valor)
          except ValueError:
            st.error(f"Valor inválido: '{valor}'. use o formato 0.000,00")
          else:
            if val <= 0:
              st.error("O valor deve ser maior que zero")
            else:
              data = {
                "name": name,
                "descricao": descricao,
                "valor": str(val),
                "categoria": categoria,
                "email_fornecedor": email_fornecedor,
              }
              res = api("PUT", f"/products/{pid}", data)
              if "error" in res:
                st.error(res['error'])
              else:
                st.success(f"Produto ID {pid} atualização com sucesso")
                      # st.rerun()
                
        
    
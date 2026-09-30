import os
import streamlit as st
import requests
#--------------------------------------------------- 
# URL base da API FastAPI (backend)
#--------------------------------------------------- 
API = os.getenv("API_URL", "http://localhost:8000")

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
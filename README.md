# Projeto 2 SQL

## Roteiro de inicialização do projeto
1. Execute o script 'create_db.sql' para criar o banco de dados;
2. Crie um arquivo com o nome '.env' na pasta do projeto com as seguintes variáveis:

  USER_SQL = "Seu usuário (não o root) do MySQL"
  
  PASSWORD_SQL = "Sua senha do MySQL"

3. No terminal rode:

  $ uvicorn api_rest.main:app --reload

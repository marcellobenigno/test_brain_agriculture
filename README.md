# Test Brain Agriculture - Backend

## Descrição Geral:

O teste tem como objetivo acurar as habilidades do candidato em resolver alguns problemas relacionados à lógica de
programação, regra de negócio e orientação à objetos.

O mesmo consiste em um cadastro de produtor rural com os seguintes dados:

1. CPF ou CNPJ
2. Nome do produtor
3. Nome da Fazenda
4. Cidade
5. Estado
6. Área total em hectares da fazenda
7. Área agricultável em hectares
8. Área de vegetação em hectares
9. Culturas plantadas (Soja, Milho, Algodão, Café, Cana de Açúcar)

## Requisitos de negócio:

* O usuário deverá ter a possibilidade de cadastrar, editar, e excluir produtores rurais.
* O sistema deverá validar CPF e CNPJ digitados incorretamente.
* A soma de área agrícultável e vegetação, não deverá ser maior que a área total da fazenda
* Cada produtor pode plantar mais de uma cultura em sua Fazenda.
* A plataforma deverá ter um Dashboard que exiba:
    * Total de fazendas em quantidade
    * Total de fazendas em hectares (área total)
    * Gráfico de pizza por estado.
    * Gráfico de pizza por cultura.
    * Gráfico de pizza por uso de solo (Área agricultável e vegetação)

## Requisitos Técnicos:

* Python >= 3.11
* PostgreSQL >= 12

## Configurações do Banco de Dados:

É necessário criar um banco **PostgreSQL**, no terminal, faça:

```
createdb test_brain_agriculture
```

## Ambiente de desenvolvimento:

Para rodar a aplicação em ambiente de desenvolvimento, é necessário:

* Clonar o repositório;
* Crie um virtualenv com Python  >= 3.11 ;
* Ativar a virtualenv;
* Instalar as dependências do ambiente de desenvolvimento;

```
git clone https://github.com/marcellobenigno/test_brain_agriculture.git
cd test_brain_agriculture
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

* Renomeie o arquivo `env-sample` para `.env`:

```
mv env-sample .env
```

* Preencha as informações do `.env` e rode os seguintes comandos:

```
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

## Adicionando dados à aplicação:

Foi criado um custom manager no projeto (`core/management/commands/add_data.py`), para adicionar dados fake, faça:

```
python manage.py add_data <numero-de-proprietarios-e-propriedades-rurais>
```

Caso não seja passado nenhum argumento, serão criados 50 proprietátios e 50 propriedades
rurais (`python manage.py add_data`).

Crie um superusuário para acessar o painel administrativo:

```
python manage.py createsuperuser
```

Por último, acesse a aplicação, iniciando o servidor:

```
python manage.py runserver
```

O sistema ficará disponível no endereço http://localhost:8000/ 🎉

https://github.com/viniciusgferreira/brain-ag-backend-api

<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png" alt="Pikachu" width="120">
  <h1>⚡ PokeVault</h1>
  <p><strong>O e-commerce definitivo para treinadores colecionadores</strong></p>
  <p>De Bulbassaur a Rayquaza — todos os 384 Pokémon das 3 primeiras gerações</p>
  
  <!-- Badges -->
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
  <img src="https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge">
</div>

---

## 📖 Sobre o Projeto

**PokeVault** é um e-commerce fictício desenvolvido para treinadores que desejam adquirir Pokémon das regiões de **Kanto**, **Johto** e **Hoenn** (1ª à 3ª geração). 

A jornada de desenvolvimento foi:
1. **Coleta de Dados:** Através de requisições à [PokeAPI](https://pokeapi.co/), obtivemos informações detalhadas de todos os 384 Pokémon.
2. **Curadoria Manual:** Criamos arquivos JSON separados (`pokemons.json` e `pokemons_pt.json`) para editar informações específicas (preços, descrições personalizadas, nomes em português, etc.) que não estavam disponíveis ou precisavam de ajustes na API.
3. **Banco de Dados:** Inserimos todos os dados tratados em um banco MySQL, garantindo performance e consistência.
4. **Integração:** O backend (Flask) consome o banco e entrega os dados para o frontend, que utiliza Jinja para renderização dinâmica e JavaScript para interatividade.

---

## 🚀 Funcionalidades

- ✅ **Catálogo Completo** — Listagem com todos os 384 Pokémon, incluindo sprites oficiais.
- 🔍 **Filtros e Busca** — Por nome, tipo, geração ou raridade.
- 🛒 **Carrinho de Compras** — Gerenciado com JavaScript (localStorage + sessões).
- ⭐ **Sistema de Avaliação** — Usuários podem avaliar produtos com estrelas.
- 👤 **Autenticação** — Cadastro e login com sessões Flask (`session`).
- 💾 **Persistência de Dados** — Tudo salvo no banco de dados (pedidos, avaliações, usuários).

---

## 🛠️ Tecnologias Utilizadas

| Camada          | Tecnologias                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| **Backend**     | Python 3.9+, Flask, MySQL, Jinja2                                           |
| **Frontend**    | HTML5, CSS3, JavaScript (ES6)                                               |
| **API**         | Requisições HTTP à PokeAPI (tratamento com `requests`)                      |
| **Ferramentas** | Git, pip (venv), JSON para dados customizados                               |

### Bibliotecas Python principais:
```python
flask, mysql-connector-python, requests, json

### 📂 Estrutura do Projeto

POKEVAULT/
├── app.py                      # Arquivo principal do Flask
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
├── .gitignore                  # Arquivos ignorados pelo Git
│
├── database/                   # Conexão com o banco de dados
│   └── conexao.py              # Configuração e conexão MySQL
│
├── migrate/                    # Migrações e população do banco
│   ├── diagrama_finalizado_pokevault.sql  # Script para criar as tabelas
│   └── pokemons.py             # Script para inserir os Pokémon no banco
│
├── model/                      # Models (camada de negócio)
│   ├── carrinho.py             # Lógica do carrinho de compras
│   ├── comentarios.py          # Gerenciamento de avaliações/comentários
│   ├── pokemons_select.py      # Queries para selecionar Pokémon
│   ├── tipos.py                # Gerenciamento de tipos dos Pokémon
│   └── usuario.py              # Autenticação e gerenciamento de usuários
│
├── static/                     # Arquivos estáticos (CSS, JS, imagens)
│   ├── img/                    # Imagens do projeto
│   ├── script/                 # Scripts JavaScript
│   │   └── JS aside.js         # Funcionalidades do menu lateral
│   ├── catalogo.css            # Estilos da página de catálogo
│   ├── index.css               # Estilos da página inicial
│   ├── layout.css              # Estilos do layout base
│   ├── novidades_contato.css   # Estilos das páginas de novidades e contato
│   ├── reset.css               # Reset de estilos CSS
│   └── unitario.css            # Estilos da página individual do Pokémon
│
├── templates/                  # Templates HTML (Jinja2)
│   ├── layout.html             # Layout base (navbar, footer)
│   ├── index.html              # Página inicial
│   ├── catalogo.html           # Catálogo com filtros
│   ├── unitario.html           # Página individual do Pokémon
│   ├── cadastro.html           # Página de cadastro de usuário
│   ├── login.html              # Página de login
│   ├── contato.html            # Página de contato
│   ├── novidades.html          # Página de novidades
│   ├── sobre-nos.html          # Página sobre nós
│   └── sobre.html              # Página sobre o projeto
│
└── data/                       # Arquivos de dados
    ├── pokemons.json           # Dados brutos da PokeAPI
    ├── pokemons_pt.json        # Dados com traduções e customizações
    ├── requisicao_pokemons.py  # Script para requisição à PokeAPI
    ├── traducao_pokemons.py    # Script para tradução dos dados
    └── swap.txt                # Arquivo auxiliar (swap de dados)
```

## 🧪 Como Rodar o Projeto Localmente

### 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Python 3.9+** — [Download aqui](https://www.python.org/downloads/)
- **MySQL Server 8.0+** — [Download aqui](https://dev.mysql.com/downloads/mysql/)
  - ⚠️ *Certifique-se de que o serviço MySQL esteja rodando antes de prosseguir*
- **Git** (opcional, mas recomendado) — [Download aqui](https://git-scm.com/downloads)

---

### 🚀 Passo a Passo

Siga os passos abaixo para rodar o projeto localmente:

---

#### 1️⃣ Clone o repositório


```
git clone https://github.com/seu-usuario/pokevault.git
cd pokevault
```
**2. Crie e ative um ambiente virtual:**

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
# ou
venv\Scripts\activate      # Windows
```
**3. Instale as dependências:**

```
pip install -r requirements.txt
```
**4. Configure o banco de dados MySQL:**

> 💡 Crie um banco de dados (ex: pokevault)

> 📋 Execute o script SQL para criar as tabelas:

**5. Popule o banco com os Pokémon:**

```
python migrate/pokemons.py
```
> ⚡ Este script irá inserir todos os **384 Pokémon** no banco de dados.

**6. Execute a aplicação:**

```
python app.py
```
**7. Acesse no navegador:**


http://localhost:5000


---

## 🤝 Como Contribuir

> 🍴 Faça um **fork** do projeto

> 🌿 Crie uma branch para sua feature: `git checkout -b minha-feature`

> 💾 Commit suas mudanças: `git commit -m 'feat: adiciona filtro por tipo'`

> 📤 Push para a branch: `git push origin minha-feature`

> 🔀 Abra um **Pull Request**

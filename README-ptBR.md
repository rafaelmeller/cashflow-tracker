<h1 align="center" style="font-weight: bold;">Projeto Cashflow Tracker</h1>

<div align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python Badge">
</div>

<div align="center">
    <img src="https://img.shields.io/badge/pytest-tested-brightgreen" alt="Pytest: tested">
</div>

<h4 align="center"> 
         <b>Status:</b> Completo
</h4>

<p align="center">
 <a href="#sobre-ℹ️">Sobre</a> •
 <a href="#objetivos-🎯">Objetivos</a> •
 <a href="#funcionalidades-🌟">Funcionalidades</a> • 
 <a href="#demonstração-do-projeto-🖥️">Demonstração do Projeto</a> •
 <a href="#fluxo-de-trabalho-🔄">Fluxo de Trabalho</a> •
 <a href="#arquitetura-🏗️">Arquitetura</a> •
 <a href="#setup-⚙️">Setup</a> • 
<a href="#proximos-passos-e-desafios-📈">Próximos Passos e Desafios</a> •
 <a href="#autor-👨🏻‍💻">Autor</a> • 
 <a href="#licença-📝">Licença</a>
</p>

###### _Outras versões:_ [_Click here for English_](./README.md)

## Sobre ℹ️

Este projeto foi criado como o projeto final para o CS50P, o curso de Introdução à Programação com Python de Harvard. É uma aplicação CLI que permite aos usuários importar extratos bancários em formato CSV e manipular esses dados, filtrando transações, gerando resumos e criando relatórios de orçamento e metas para períodos específicos.

A aplicação foi projetada com uma abordagem modular, separando a interação do usuário, processamento de dados e funções de relatório, para garantir clareza e fácil manuntenção.

Devido aos requisitos do CS50P para projetos finais, esta aplicação não pôde ser totalmente Orientada a Objetos (já que pelo menos três funções independentes eram necessárias para testes).

Baseado nesses requisitos, o design inclui:
- **funções de I/O e auxiliares** testáveis para suportar recursos como validação de dados e gerenciamento de arquivos.
- **Funções auxiliares de UI** para simplificar a função `main()`, tornando-a mais curta, clara e menos repetitiva.

#
## Objetivos 🎯

Esta aplicação foi desenvolvida para aprimorar a compreensão do autor sobre conceitos chave de Python, incluindo:
- **Classes**: Implementação de estruturas de dados personalizadas como `Transaction` e `CashFlowTracker`.
- **File Handling**: Gerenciamento de importações e exportações de CSV.
- **Regular Expressions**: Validação e processamento de entradas do usuário.
- **Unit Testing**: Escrita e execução de testes usando Pytest.

#
## Funcionalidades 🌟

- **Importação de arquivo CSV**: Importar transações de um arquivo CSV contendo dados de receitas e despesas.
- **Entrada Manual de Transações**: Adicionar transações diretamente via CLI.
- **Editar e Excluir Transações**: Modificar ou remover transações existentes.
- **Categorização**: Agrupar e editar categorias com base nas descrições das transações.
- **Rastreamento de Orçamento e Metas**: Definir limites de gastos (orçamentos) e metas de receita para categorias, com acompanhamento de progresso.
- **Relatórios e Exportação**: Gerar resumos, relatórios de orçamento/metas ou conjuntos de dados filtrados e salvá-los como arquivos CSV ou TXT.

#
## Demo do Projeto 🖥️
[Clique aqui para assistir a demo do projeto](https://youtu.be/086DNvuLR84)

#
## Fluxo de Trabalho 🔄 

1. **Importar Transações**: 
     - Carregar um arquivo `.csv` contendo dados de transações.
     - Checar se o arquivo corresponde ao formato exigido: `date, category, description, value`. Caso não corresponda, apontar as colunas a serem designadas para cada campo.

2. **Adicionar ou Editar Transações**:
     - Adicionar novas transações manualmente ou editar as existentes através do menu.

3. **Categorizar**:
    - Definir categorias para cada transação, agrupando por descrição se necessário, para que os orçamentos e metas para cada categoria possam ser definidos.

4. **Definir Orçamentos e Metas**:
     - Definir limites de gastos (orçamentos) ou metas de receita para categorias específicas.

5. **Gerar Relatórios**:
     - Visualizar resumos de receitas e despesas por categoria ou período.
     - Exportar relatórios como arquivos `.csv` ou `.txt` para registro.

#
## Arquitetura 🏗️

1. **Uso de Classes**:  
     - `Transaction`: Representa uma transação individual com atributos como data, tipo (receita/despesa), categoria, descrição e valor.
     - `Budget` e `Goal`: Acompanham metas financeiras para categorias específicas.
     - `CashFlowTracker`: Gerencia as transações, orçamentos e metas, oferecendo métodos para filtragem, relatórios e categorização de dados.
     
2. **Funções de I/O**:  
     - **Manipulação de Arquivos**: Funções como `read_csv()` e `export_data()` permitem importar e exportar dados financeiros.
     - **Validação**: A validação de entrada garante compatibilidade com os formatos esperados.

3. **Funções de UI**:  
     - Funções modulares como `get_valid_date()` e `choose_data_set()` simplificam a interação do usuário e evitam código redundante na função `main()`.

4. **Função main()**:  
     - Implementa um fluxo de trabalho baseado em CLI que guia o usuário pelas funcionalidades do programa.

#
## Setup ⚙️

```bash
# Clone o repositório
git clone <repository-url>

# Navegue até o diretório do projeto
cd <project-directory>

# Crie um ambiente virtual (certifique-se de que o Python já está instalado em sua máquina)
python3 -m venv venv

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python3 project.py
```
##### _**Observação:**_ _Lembre-se que, para trabalhar com qualquer arquivo .csv, você precisa tê-lo no mesmo diretório que project.py_

#
## Próximos Passos e Desafios 📈

- **Criar identificadores únicos para cada transação:**
Identificadores únicos seriam interessantes para facilitar a edição das transações, aumentar o controle e diminuir a probabilidade de duplicidade.

- **Incluir arquivos Excel:**
Estender a manipulação de arquivos para suportar arquivos `.xlsx`, para melhor compatibilidade com formatos de planilhas comumente usados. Também tornaria mais fácil adicionar análises gráficas aos resumos e relatórios.

- **Adicionar Relatórios em PDF:**
Gerar resumos detalhados em PDF para relatórios mais profissionais.

- **Expandir Testes:**
Adicionar testes para métodos de classe e "edge cases", tornando a testagem mais ampla e robusta.

- **Otimização de Desempenho e Escalabilidade:**
Em grandes datasets, alguns métodos (como `filter` ou `summary`) se tornariam lentos. Para armazenar dados permanentemente e ter melhoria de desempenho, substituir o armazenamento em disco por um banco de dados (como SQLite ou PostgreSQL) auxiliaria na gestão e consulta de transações de forma mais eficiente.

- **Adicionar uma GUI:**
Usar Tkinter ou um framework similar para criar uma interface gráfica, visando uma experiência mais amigável ao usuário.

#
## Autor 👨🏻‍💻

Este projeto foi projetado e desenvolvido por **Rafael Meller**.

[![Linkedin Badge](https://img.shields.io/badge/-Rafael_Meller-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/tgmarinho/)](https://www.linkedin.com/in/rafaelmeller/) 
[![Gmail Badge](https://img.shields.io/badge/-rafaelmeller.dev@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=rafaelmeller.dev@gmail.com)](mailto:rafaelmeller.dev@gmail.com)
#
## Licença 📝

Este projeto é licenciado sob a licença [MIT](./LICENSE).

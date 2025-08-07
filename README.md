# Análise de Ocorrências Aeronáuticas no Brasil

## Visão Geral

Este projeto apresenta um banco de dados e uma plataforma de visualização interativa para a análise de ocorrências aeronáuticas na aviação civil brasileira. Utilizando dados oficiais do CENIPA
(Centro de Investigação e Prevenção de Acidentes Aeronáuticos), o sistema permite explorar eventos, identificar tendências e obter insights sobre a segurança da aviação no país através de um mapa interativo e consultas estatísticas detalhadas.

---

## ✨ Principais Funcionalidades

- **Mapa Interativo**: Visualize a localização geográfica de acidentes e incidentes em todo o Brasil. Os eventos são codificados por cores para indicar o tipo de ocorrência (Vermelho para Acidente, Azul para Incidente).  

- **Relatórios Detalhados**: Clique em qualquer ocorrência no mapa para obter informações detalhadas, incluindo aeronaves envolvidas, data, local e fatores contribuintes.  

- **Análises Estatísticas**: Acesse consultas pré-configuradas para identificar as aeronaves e fabricantes com maior número de acidentes, a data da ocorrência mais recente por fabricante, e mais.  

- **Filtro por Fator Contribuinte**: Investigue ocorrências associadas a fatores específicos, como "julgamento de pilotagem" ou "condições meteorológicas adversas".

---

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python, Flask  
- **Banco de Dados**: MySQL  
- **Conector Python-MySQL**: PyMySQL  
- **Frontend**: HTML, CSS, JavaScript (com bibliotecas de mapeamento)

---

## 🗃️ Estrutura do Projeto

### Fonte e Curadoria dos Dados

O projeto é fundamentado em um dataset público e atualizado do CENIPA, disponibilizado pelo Portal de Dados Abertos do Governo Federal.  
Realizamos um processo de curadoria para focar nas informações mais relevantes para a análise, removendo colunas que não seriam utilizadas na aplicação final.

### Modelagem do Banco de Dados

A arquitetura dos dados foi estruturada em um modelo relacional para garantir a integridade e a eficiência das consultas.  
As principais entidades do sistema são:  

- **Ocorrencia**  
- **Aeronave**  
- **Fabricante**  
- **Fator_contribuinte**  
- **Recomendacao**

Essas tabelas são interligadas por meio de chaves primárias e estrangeiras, permitindo a construção de uma visão completa de cada evento aeronáutico.

### Capacidades Analíticas

O sistema foi projetado para transformar dados brutos em insights através de consultas SQL.  
As análises permitem gerar estatísticas e rankings, como:

- Identificação das aeronaves e fabricantes com maior histórico de acidentes  
- Data da ocorrência mais recente por fabricante  
- Correlação entre eventos e fatores contribuintes  

---

## 🖼️ Screenshots da Aplicação

*(Insira aqui screenshots da aplicação, como o mapa, a janela de detalhes e os resultados das consultas)*

---

## 👥 Equipe

- **Bruno Rodrigues** - 123691601  
- **Lucas Rodrigues** - 123693132  
- **Lucas Vargas** - 123698433  
- **Renan Guedes** - 12109416

# Análise de Ocorrências Aeronáuticas no Brasil

## Visão Geral

Este projeto foi desenvolvido na disciplina Banco de Dados I e apresenta uma plataforma de visualização interativa para a análise de ocorrências aeronáuticas na aviação civil brasileira. Utilizando dados oficiais do CENIPA
(Centro de Investigação e Prevenção de Acidentes Aeronáuticos), o sistema permite explorar eventos, identificar tendências e obter insights sobre a segurança da aviação no país através de um mapa interativo e consultas estatísticas detalhadas. Neste trabalho foi feito o modelo conceitual, lógico e físico do banco de dados e a aplicação com suas devidas consultas.  

---

## Principais Funcionalidades

- **Mapa Interativo**: Visualize a localização geográfica de acidentes e incidentes em todo o Brasil. Os eventos são codificados por cores para indicar o tipo de ocorrência (Vermelho para Acidente, Azul para Incidente).  

- **Relatórios Detalhados**: Clique em qualquer ocorrência no mapa para obter informações detalhadas, incluindo aeronaves envolvidas, data, local e fatores contribuintes.  

- **Análises Estatísticas**: Acesse consultas pré-configuradas para identificar as aeronaves e fabricantes com maior número de acidentes, a data da ocorrência mais recente por fabricante, e mais.  

- **Filtro por Fator Contribuinte**: Investigue ocorrências associadas a fatores específicos, como "julgamento de pilotagem" ou "condições meteorológicas adversas".

---

## Tecnologias Utilizadas

- **Backend**: Python, microframework Flask  
- **Banco de Dados**: MySQL  
- **Conector Python-MySQL**: PyMySQL  
- **Frontend**: HTML, CSS, JavaScript

---

## Fonte dos Dados

O projeto é fundamentado em um dataset público e atualizado do CENIPA, disponibilizado pelo Portal de Dados Abertos do Governo Federal.  
Realizamos um processo de filtragem para focar nas informações mais relevantes para a análise, removendo colunas que não seriam utilizadas na aplicação final.

### Modelagem do Banco de Dados

A arquitetura dos dados foi estruturada em um modelo relacional.  
As principais entidades do sistema são:  

- **Ocorrencia**  
- **Aeronave**  
- **Fabricante**  
- **Fator_contribuinte**  
- **Recomendacao**

Essas tabelas são interligadas por meio de chaves primárias e estrangeiras, permitindo a construção de uma visão completa de cada evento aeronáutico.

O sistema foi projetado para transformar dados brutos em insights através de consultas SQL.  
As análises permitem gerar estatísticas e rankings, como:

- Identificação das aeronaves e fabricantes com maior histórico de acidentes  
- Data da ocorrência mais recente por fabricante  
- Correlação entre eventos e fatores contribuintes  

---

### 🖼️ Prints da aplicação

## Modelagem Conceitual
<img width="1249" height="569" alt="Image" src="https://github.com/user-attachments/assets/7131c4a5-feca-4e44-8e33-50686d0f3ff2" />

### Modelagem lógica
<img width="1195" height="797" alt="Image" src="https://github.com/user-attachments/assets/092af966-e1d1-4418-ad61-d542ba105eda" />

### Prints da Aplicação
<img width="1382" height="686" alt="Image" src="https://github.com/user-attachments/assets/30691d67-1e29-4958-91a9-b4a78b5ec833" />
### Ao selecionar um ponto destacado qualquer no mapa aparecerá detalhes sobre a ocorrência para o usuário, haverá um botão para exibir mais detalhes da ocorrência selecionada (conforme as imagens abaixo).
<img width="840" height="323" alt="Image" src="https://github.com/user-attachments/assets/14075ae9-780d-49d0-bbfa-2358c90e5725" />
### Uma outra funcionalidade do site é a obtenção de detalhes no sentido de saber qual fabricante detém o maior número de acidentes de acordo com o dado, saber mais detalhes do ocorrido, como foi e etc. Segue abaixo a imagem um exemplo:
<img width="1580" height="486" alt="Image" src="https://github.com/user-attachments/assets/f3c6bce3-76ed-4119-a8bf-9f5acdc19bbb" />

---

## 👥 Equipe
- **Renan Guedes**
- **Bruno Rodrigues** 
- **Lucas Rodrigues**
- **Lucas Vargas**

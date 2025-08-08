# Cellular-Automata
Modelagem de Sistemas Biológicos com Autômatos Celulares Baseados em Agentes
Este repositório apresenta uma abordagem inovadora para modelagem computacional utilizando autômatos celulares com agentes autônomos. Os modelos simulam ecossistemas microbianos, dinâmicas predador-presa e geração de padrões complexos a partir de regras locais.

# Objetivos
Os modelos desenvolvidos permitem:

Simular interações complexas em ecossistemas microbianos

Estudar dinâmicas populacionais entre espécies com adaptação evolutiva

Explorar a emergência de padrões complexos a partir de regras simples

Analisar comportamentos emergentes em sistemas biológicos

# Fundamentação Teórica
A abordagem combina:

Autômatos celulares clássicos

Modelagem baseada em agentes

Algoritmos genéticos simples

Estocasticidade controlada

# Modelos Implementados
1. Ecossistema Microbiano (EcoMicrobiano.py)
Simula a competição entre três tipos de microrganismos:

Produtores (verde): Geram energia

Consumidores (vermelho): Alimentam-se dos produtores

Decompositores (amarelo): Reciclam matéria orgânica

2. Dinâmica de Espécies (DinamicaEspecies.py)
Modela relações predador-presa com:

Adaptação evolutiva

Aprendizado individual

Memória de eventos passados

3. Gerador de Padrões (GeradorPadroes.py)
Gera padrões complexos através de:

Regras locais estocásticas

Inibição lateral

Propagação de sinais

# Como Executar
Pré-requisitos
Instale as dependências necessárias:

bash
pip install pygame numpy

Executando as Simulações

## **Ecossistema Microbiano:**

bash
python EcoMicrobiano.py

Controles:

Espaço: Pausar/continuar

R: Reiniciar simulação

Clique do mouse: Adicionar organismos

## **Dinâmica de Espécies:**

bash
python DinamicaEspecies.py

Controles:

Espaço: Pausar/continuar

R: Reiniciar

## **Gerador de Padrões:**

bash
python GeradorPadroes.py

Controles:

Espaço: Pausar/continuar

R: Reiniciar

S: Adicionar nova semente

# Considerações Científicas
## Estes modelos oferecem uma estrutura flexível para:

Estudos em ecologia teórica

Pesquisa em microbiologia computacional

Análise de sistemas complexos

Desenvolvimento de algoritmos bioinspirados

Os códigos podem ser estendidos para incluir:

Mais espécies interagentes

Variações ambientais

Mecanismos evolutivos mais complexos
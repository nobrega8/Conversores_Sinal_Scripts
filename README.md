# Calculadora para Conversores de Sinal - FCT Nova

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Educational%20Open-green)
![Version](https://img.shields.io/badge/Version-v3.0.0-orange)
![Contributors](https://img.shields.io/badge/Contributors-3-purple)

![TI Nspire CX II-T](https://img.shields.io/badge/TI%20Nspire%20CX%20II--T-%20Complete-success)
![TI Nspire CX](https://img.shields.io/badge/TI%20Nspire%20CX-%20Limited-yellow)
![Casio FX-CG50](https://img.shields.io/badge/Casio%20FX--CG50-%20Complete-success)

</div>

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Calculadoras Testadas](#calculadoras-testadas)
- [Funcionalidades](#funcionalidades)
- [Exemplos de Uso](#exemplos-de-uso)
- [Uso Académico](#uso-académico)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)
- [Desenvolvedores](#desenvolvedores)

---

## Sobre o Projeto

Conjunto de calculadoras especializadas para análise de conversores de sinal, desenvolvido para estudantes da área de eletrónica. Inclui implementações para diferentes modelos de calculadoras, permitindo cálculos precisos de parâmetros críticos em ADCs e DACs.

**Características principais:**

- Suporte para Texas Instruments Nspire CX Series e Casio FX-CG50
- Ferramentas para SNR, INL/DNL, jitter e moduladores Sigma-Delta
- Alinhado com o currículo da FCT Nova

---

## Instalação e Configuração

### Requisitos

- **Computador**: Python 3.7 ou superior
- **Calculadoras**: Modelos listados na secção de compatibilidade

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/nobrega8/Conversores_Sinal_Scripts.git
   cd Conversores_Sinal_Scripts
   ```

2. Execute o script principal:
   ```bash
   python source.py
   ```

3. Para calculadoras específicas, navegue até `calculadoras/<marca>/<modelo>.py`, transfira o ficheiro para a calculadora e execute conforme as instruções do modelo.

---

## Calculadoras Testadas

| Modelo | Compatibilidade | Problemas Conhecidos | Último Update |
|--------|-----------------|----------------------|---------------|
| **Source (Python)** | Completa | Nenhum | v3.0.0 |
| **Texas Nspire CX Series** ||||
| [CX II-T](https://github.com/nobrega8/Conversores_Sinal_Scripts/blob/main/calculadoras/texas/tinspirecxiit.py) | Completa | Nenhum | v3.0.0 |
| [CX](https://github.com/nobrega8/Conversores_Sinal_Scripts/tree/main/calculadoras/texas/tinspirecx) | Limitada | Utiliza TI-Basic | v3.0.0 |
| **Casio FX Series** ||||
| [FX-CG50](https://github.com/nobrega8/Conversores_Sinal_Scripts/blob/main/calculadoras/casio/casiofxcg50.py) | Completa | Espaço de ecrã limitado | v3.0.0 |

---

## Funcionalidades

<details>
<summary><strong>v1.0.0 - Funcionalidades Base</strong></summary>

1. **Calculadora de Tabelas INL/DNL** — Análise de linearidade diferencial e integral em ADCs/DACs.

2. **Calculadora SNR max** — Relação entre SNR teórico máximo e número de bits (SNR = 6.02n + 1.76 dB).

3. **Calculadora SNR** — Análise completa de ruído, incluindo jitter, ruído térmico e quantização.

</details>

<details>
<summary><strong>v2.2.0 - Análise Temporal</strong></summary>

4. **Clock Frequency** — Cálculo da frequência de clock a partir do número de bits; relação entre resolução e velocidade de conversão.

</details>

<details>
<summary><strong>v2.6.0 - Análise Avançada</strong></summary>

5. **Real and Ideal VLSB** — Cálculo do VLSB (Voltage of Least Significant Bit) real e ideal; análise de precisão em conversores.

6. **Pipeline Tools** — Ferramentas para simulação de ADCs em pipeline: análise de estágios e propagação de erro.

</details>

<details>
<summary><strong>v3.0.0 - Moduladores Sigma-Delta</strong></summary>

7. **Sigma-Delta SNR** — Calculadora de SNR para moduladores Sigma-Delta de 1ª, 2ª e 3ª ordem, considerando OSR e Vin.

8. **Sigma-Delta OSR** — Determinação do OSR necessário para atingir um SNR alvo, com base no número de bits, Vin e ordem do modulador.

</details>

---

## Exemplos de Uso

### Cálculo de SNR Básico
```python
# ADC de 12 bits
bits = 12
snr_max = 6.02 * bits + 1.76  # Resultado: 74 dB
```

### Análise Sigma-Delta
```python
# Modulador de 2ª ordem, OSR = 64
ordem = 2
osr = 64
# SNR ≈ 6.02*ENOB + 1.76 + 30*log10(OSR) + 20*log10(ordem)
```

### Conversão Binário para Tensão
```python
codigo_binario = "101010"
vref = 3.3
bits = 6
tensao = bin_to_val(codigo_binario, vref, bits)
```

---

## Uso Académico

Software desenvolvido para apoiar estudantes na unidade curricular **[Conversores de Sinal](https://guia.unl.pt/pt/2024/fct/program/1068/course/12708)** da [FCT Nova](https://www.fct.unl.pt/).

**Aplicações:**

- Verificação de cálculos em laboratórios práticos
- Análise e dimensionamento de conversores em projetos de curso
- Avaliação comparativa de diferentes arquiteturas

Os cálculos implementados estão alinhados com o conteúdo teórico, bibliografia recomendada e exercícios da unidade curricular.

---

## Como Contribuir

Contribuições são bem-vindas. Consulte o ficheiro [CONTRIBUTING.md](CONTRIBUTING.md) para instruções detalhadas.

**Resumo:**

1. Faça fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push da branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

**Diretrizes:**

- Código compatível com Python 3.7+
- Teste em pelo menos uma calculadora suportada
- Nomenclatura em português
- Documente novas funcionalidades no README

---

## Licença

Este projeto está licenciado sob a **Educational Open License** (baseada na MIT License).

- Uso: permitido apenas para fins educativos e não-comerciais, sujeito às condições da licença
- Modificação: permitida apenas para fins educativos e não-comerciais, mantendo os avisos e termos aplicáveis
- Distribuição: permitida apenas para fins educativos e não-comerciais, com inclusão do aviso de licença e atribuição ao autor original
- Uso comercial: requer autorização explícita
- Atribuição e aviso: é obrigatório dar crédito ao autor original e preservar/incluir o aviso de licença aplicável

Consulte o ficheiro [LICENSE](LICENSE) para mais detalhes.

---

## Desenvolvedores

<table>
<tr>
<td align="center">
<strong>Afonso Nóbrega</strong><br>
<sub>Source Code & Nspire CX II-T</sub>
</td>
<td align="center">
<strong>João Pedro Antunes</strong><br>
<sub>Nspire CX</sub>
</td>
<td align="center">
<strong>Diogo Ventura</strong><br>
<sub>Casio FX-CG50</sub>
</td>
</tr>
</table>

---

<div align="center">

**Copyright © 2025 | Afonso Nóbrega**

</div>

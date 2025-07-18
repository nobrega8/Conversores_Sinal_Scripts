# 🧮 Calculadora para Conversores de Sinal - FCT Nova 📊

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Educational%20Open-green)
![Version](https://img.shields.io/badge/Version-v3.0.0-orange)
![Last Update](https://img.shields.io/badge/Last%20Update-2025--07--18-brightgreen)
![Contributors](https://img.shields.io/badge/Contributors-3-purple)

![TI Nspire CX II-T](https://img.shields.io/badge/TI%20Nspire%20CX%20II--T-✅%20Complete-success)
![TI Nspire CX](https://img.shields.io/badge/TI%20Nspire%20CX-⚠️%20Limited-yellow)
![Casio FX-CG50](https://img.shields.io/badge/Casio%20FX--CG50-✅%20Complete-success)
![Python Source](https://img.shields.io/badge/Python%20Source-✅%20Complete-success)

</div>

---

## 📑 Índice

- [📋 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Características Principais](#-características-principais)
- [🚀 Instalação e Configuração](#-instalação-e-configuração)
- [📱 Funcionalidades](#-funcionalidades)
- [🔄 Calculadoras Testadas](#-calculadoras-testadas)
- [💡 Exemplos de Uso](#-exemplos-de-uso)
- [🎓 Uso Académico](#-uso-académico)
- [🤝 Como Contribuir](#-como-contribuir)
- [📄 Licença](#-licença)
- [👨‍💻 Desenvolvedores](#-desenvolvedores)

---

## 📋 Sobre o Projeto

Este projeto oferece um conjunto completo de **calculadoras especializadas para análise de conversores de sinal**, desenvolvido especificamente para estudantes e profissionais da área de eletrónica. O software inclui implementações para diferentes modelos de calculadoras, permitindo cálculos precisos de parâmetros críticos em ADCs e DACs.

### ✨ Características Principais

- 🔧 **Múltiplas Plataformas**: Suporte para Texas Instruments Nspire CX Series e Casio FX-CG50
- 📊 **Análise Completa**: Ferramentas para SNR, INL/DNL, jitter, e moduladores Sigma-Delta
- 🎯 **Precisão Académica**: Alinhado com o currículo da FCT Nova
- 📱 **Interface Otimizada**: Adaptado para as limitações de cada calculadora
- 🔄 **Atualizações Regulares**: Versão atual v3.0.0 com novas funcionalidades

---

## 🚀 Instalação e Configuração

### Requisitos

- **Para uso em computador**: Python 3.7 ou superior
- **Para calculadoras**: Modelos compatíveis listados na secção de compatibilidade

### Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/nobrega8/Conversores_Sinal_Scripts.git
   cd Conversores_Sinal_Scripts
   ```

2. **Execute o script principal**:
   ```bash
   python source.py
   ```

3. **Para calculadoras específicas**:
   - Navegue até `calculadoras/<marca>/<modelo>.py`
   - Transfira o ficheiro para a sua calculadora
   - Execute conforme as instruções específicas do modelo

---

## 📱 Funcionalidades

## 🔄 Calculadoras Testadas

| Modelo de Calculadora | Compatibilidade | Problemas Conhecidos       | Último Update |
|------------------------|-----------------|-----------------------------|----------------|
| **Source (Python)** | ✅ Completa | Nenhum | v3.0.0 |
| **Texas Nspire CX Series** ||||
| [CX II-T](https://github.com/nobrega8/Conversores_Sinal_Scripts/blob/main/calculadoras/texas/tinspirecxiit.py)     | ✅ Completa | Nenhum                  | v3.0.0     |
| [CX](https://github.com/nobrega8/Conversores_Sinal_Scripts/tree/main/calculadoras/texas/tinspirecx)      | ⚠️ Limitada | Utiliza TI-Basic        | v3.0.0     |
| **Casio FX Series** ||||
| [FX-CG50](https://github.com/nobrega8/Conversores_Sinal_Scripts/blob/main/calculadoras/casio/casiofxcg50.py)       | ✅ Completa | Espaço de ecrã limitado | v3.0.0    |

### 🧰 Ferramentas Disponíveis

<details>
<summary><strong>📈 v1.0.0 - Funcionalidades Base</strong></summary>

1. **📈 Calculadora de Tabelas INL/DNL**
   - Análise de linearidade diferencial e integral
   - Cálculo de desvios de linearidade em ADCs/DACs

2. **🔊 Calculadora SNR max**
   - Relação entre SNR teórico máximo e número de bits
   - Fórmula: SNR = 6.02n + 1.76 dB

3. **📲 Calculadora SNR**
   - Análise completa de ruído
   - Incluindo efeitos de jitter
   - Consideração de ruído térmico e quantização

</details>

<details>
<summary><strong>🕒 v2.2.0 - Análise Temporal</strong></summary>

4. **🕒 Clock Frequency**
   - Cálculo do Clock Frequency a partir do número de bits
   - Relação entre resolução e velocidade de conversão

</details>

<details>
<summary><strong>🔧 v2.6.0 - Análise Avançada</strong></summary>

5. **🔧 Real and Ideal VLSB**
   - Cálculo do VLSB (Voltage of Least Significant Bit) real e ideal
   - Análise de precisão em conversores

6. **🧪 Pipeline Tools**
   - Ferramentas especializadas para simulação de ADCs em pipeline
   - Análise de estágios e propagação de erro

</details>

<details>
<summary><strong>🔉 v3.0.0 - Moduladores Sigma-Delta</strong></summary>

7. **🔉 Sigma-Delta SNR**
   - Calculadora de SNR para moduladores Sigma-Delta
   - Suporte para 1ª, 2ª e 3ª ordem
   - Consideração de OSR (Over-Sampling Ratio), ordem e Vin

8. **🧮 Sigma-Delta OSR**
   - Determinação do OSR necessário para atingir um SNR alvo
   - Otimização baseada no número de bits, Vin e ordem do modulador

</details>

---

## 💡 Exemplos de Uso

### Exemplo 1: Cálculo de SNR Básico
```python
# Para um ADC de 12 bits
bits = 12
snr_max = 6.02 * bits + 1.76  # Resultado: 74 dB
```

### Exemplo 2: Análise Sigma-Delta
```python
# Modulador de 2ª ordem, OSR = 64
ordem = 2
osr = 64
# SNR ≈ 6.02*ENOB + 1.76 + 30*log10(OSR) + 20*log10(ordem)
```

### Exemplo 3: Conversão Binário-Decimal
```python
# Converter código binário para tensão
codigo_binario = "101010"
vref = 3.3
bits = 6
tensao = bin_to_val(codigo_binario, vref, bits)
```

---

## 🎓 Uso Académico

Este software foi desenvolvido especificamente para apoiar os estudantes na unidade curricular **[Conversores de Sinal](https://guia.unl.pt/pt/2024/fct/program/1068/course/12708)** da [FCT Nova](https://www.fct.unl.pt/). 

### 📚 Aplicações Académicas

- **Laboratórios práticos**: Verificação de cálculos teóricos
- **Projetos de curso**: Análise e dimensionamento de conversores
- **Estudos comparativos**: Avaliação de diferentes arquiteturas
- **Investigação**: Suporte a trabalhos de investigação em conversores de sinal

### 🎯 Alinhamento Curricular

Os cálculos e métodos implementados estão rigorosamente alinhados com:
- Conteúdo teórico da unidade curricular
- Bibliografia recomendada
- Exercícios práticos e laboratoriais
- Projetos de avaliação

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. **Crie** uma branch para a sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** as suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### 📝 Diretrizes de Contribuição

- Mantenha o código compatível com Python 3.7+
- Adicione comentários explicativos
- Teste em pelo menos uma calculadora suportada
- Mantenha a nomenclatura em português (contexto académico português)
- Documente novas funcionalidades no README

Veja o ficheiro [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

---

## 📄 Licença

Este projeto está licenciado sob a **Educational Open License** (baseada na MIT License).

### 📋 Resumo da Licença

- ✅ **Uso educativo**: Permitido sem restrições
- ✅ **Modificação**: Permitida para fins educativos
- ✅ **Distribuição**: Permitida para fins não-comerciais
- ❌ **Uso comercial**: Requer autorização explícita
- ⚖️ **Atribuição**: Obrigatória ao autor original

Para mais detalhes, consulte o ficheiro [LICENSE](LICENSE).

---

## 👨‍💻 Desenvolvedores

<table>
<tr>
<td align="center">
<strong>Afonso Nóbrega</strong><br>
<sub>Source Code & Nspire CX II-T</sub><br>
🔧 Arquitetura principal<br>
📱 Implementação Nspire CX II-T
</td>
<td align="center">
<strong>João Pedro Antunes</strong><br>
<sub>Nspire CX</sub><br>
📱 Implementação Nspire CX<br>
🔧 Adaptação TI-Basic
</td>
<td align="center">
<strong>Diogo Ventura</strong><br>
<sub>Casio FX-CG50</sub><br>
📱 Implementação Casio FX-CG50<br>
🎨 Otimização de interface
</td>
</tr>
</table>

### 📊 Estatísticas do Projeto

- **Linhas de código**: ~2000 linhas
- **Linguagens**: Python, TI-Basic
- **Plataformas**: 3 calculadoras suportadas
- **Funcionalidades**: 8 calculadoras especializadas

---

<div align="center">

### 🙏 Agradecimentos

*"Obrigado pela ajuda Nóbrega!"*

---

**Copyright © 2025 | Afonso Nóbrega**

</div>

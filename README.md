# 🧮 Calculadora para Conversores de Sinal - FCT Nova 📊

## 📝 Visão Geral

Este software fornece um conjunto de ferramentas de cálculo essenciais para análise e projeto de conversores de sinal na unidade curricular "Conversores de Sinal" da FCT Nova. Desenvolvido por **Afonso Nóbrega** para a Texas Nspire CX II-T CAS, o script inclui três calculadoras principais:

1. **📈 Calculadora de Tabelas INL/DNL** - Para análise de linearidade diferencial e integral
2. **🔊 Calculadora SNR max** - Para relações entre SNR e número de bits
3. **📲 Calculadora SNR** - Para análise completa de ruído incluindo efeitos de jitter

## 🛠️ Funcionalidades

### 1. 📈 Calculadora de Tabelas INL/DNL

Permite calcular e visualizar valores de não-linearidade integral (INL) e não-linearidade diferencial (DNL) para um conversor ADC ou DAC.

**Recursos:**
- Entrada flexível para número de bits
- Cálculo automático de VlsbReal
- Entrada de dados binários e valores Vout correspondentes
- Cálculo completo de INL e DNL para cada código
- Cálculo de linearidade efetiva em bits

**Fórmulas utilizadas:**
- VlsbReal = (VoutMax - VoutMin)/(2^n - 1)
- INL = (Vout - n*VlsbR - Vout_min)/VlsbR
- DNL = (Vout(n) - Vout(n-1))/VlsbR - 1
- Linearidade = nbits-log₂(INLmax-INLmin)

### 2. 🔊 Calculadora SNR max

Ferramenta simples para cálculos rápidos entre SNR máximo e número de bits.

**Recursos:**
- Cálculo de SNR max a partir do número de bits
- Cálculo do número de bits necessário a partir do SNR desejado

**Fórmulas utilizadas:**
- SNR max = 6.02 * n + 1.76 dB
- n = (SNR max - 1.76) / 6.02

### 3. 📲 Calculadora SNR

Ferramenta avançada para análise completa de SNR com efeitos de jitter.

**Recursos:**
- Cálculo de SNR considerando ruído de quantização
- Cálculo de SNR considerando efeitos de jitter
- Determinação do número de bits necessário para um SNR específico
- Verificação de limitações impostas pelo jitter

**Fórmulas utilizadas:**
- VinRMS = Vin / √2
- Vlsb = Vref / 2^n
- VNQRMS = Vlsb / √12
- VJitterRMS = VinRMS * 2π * Fin * Djitter
- SNR = 10 * log₁₀(VinRMS² / (VNQRMS² + VJitterRMS²))

## 🔄 Compatibilidade e Problemas Conhecidos

| Modelo de Calculadora | Compatibilidade | Problemas Conhecidos |
|----------------------|-----------------|---------------------|
| Texas Nspire CX II-T CAS | ✅ Completa | Nenhum |
| Texas Nspire CX II-T | ✅ Completa | Nenhum |
| Casio FX-CG50 | ✅ Completa | Espaço de ecrã limitado |

## 🎓 Uso Académico

Este software foi desenvolvido especificamente para apoiar os estudantes na unidade curricular "Conversores de Sinal" da FCT Nova. Os cálculos e métodos implementados estão alinhados com o conteúdo do curso.

## 👨‍💻 Desenvolvedor

Desenvolvido por **Afonso Nóbrega** (2025)
Copyright © 2025 Barraca Familia Software

## 📄 Licença

Este software é fornecido apenas para uso educacional no contexto da unidade curricular "Conversores de Sinal" da FCT Nova.

---

*"Obrigado pela ajuda Nobrega!"* 🙏

# Calculadora para Conversores de Sinal - FCT Nova
# Copyright © 2025 Afonso Nóbrega
# **source code**
# - versões especificas de cada calculadora estão em ./calculadoras/<marca>/<modelo>.py

import matplotlib.pyplot as plt
from math import log, log10, log2, pi, ceil, floor

# Constants
SNR_FORMULA_SLOPE = 6.02  # dB per bit
SNR_FORMULA_OFFSET = 1.76  # dB offset
SQRT_2 = 2**0.5
SQRT_12 = 12**0.5

def bin2dec(binary_bits):
    """Convert binary string to decimal"""
    return int(binary_bits, 2)

def bin_to_val(bin_str, vref, bits):
        """Converte binário para valor de tensão DAC"""
        nivel = int(bin_str, 2)
        max_nivel = 2**bits - 1
        passo = vref / (2**bits)
        return -vref/2 + nivel * passo
    
def val_to_bin(val, vref, bits):
    """Converte um valor analógico para binário"""
    steps = 2**bits
    delta = vref / steps
    code = int((val + vref/2) / delta)
    # Limita o código entre 0 e 2^bits-1
    code = max(0, min(code, steps - 1))
    # Converte para binário e remove o '0b' do início
    return format(code, f'0{bits}b')

def calculate_vlsbr(vout_min, vout_max, num_bits):
    """Calcula VlsbReal usando fórmula: (VoutMax - VoutMin)/(2^n - 1)
    
    Args:
        vout_min (float): valor mínimo de Vout
        vout_max (float): valor máximo de Vout
        num_bits (int): número de bits
        
    Returns:
        float: valor de VlsbReal
    """
    try:
        return (vout_max - vout_min)/(2**num_bits - 1)
    except:
        return 0
    
def calculate_vlsbi(vref, num_bits):
    """Calcula VlsbIdeal usando fórmula: Vref/(2^n)
    
    Args:
        vref (float): valor de Vref
        num_bits (int): número de bits
        
    Returns:
        float: valor de VlsbIdeal
    """
    try:
        return vref/(2**num_bits)
    except:
        return 0

def calculate_inl(vout, decimal_value, vlsbr, vout_min):
    """Calcula INL usando fórmula: INL = (Vout - n*VlsbR - Vout_min)/VlsbR
    
    Args:
        vout (float): valor de Vout
        
        decimal_value (float): valor decimal correspondente aos bits
        
        vlsbr (float): valor de VlsbReal
        
        vout_min (float): valor mínimo de Vout
        
    Returns:
        float: valor de INL
        
        bool: True se o cálculo foi bem-sucedido, False caso contrário
    """
    try:
        # Aplica fórmula INL: INL = (Vout - n*VlsbR - Vout_min)/VlsbR 
        inl = (vout - decimal_value*vlsbr - vout_min)/vlsbr 
        return inl, True
    except:
        return 0, False

def calculate_dnl(vout, prev_vout, vlsbr):
    """Calcula DNL usando fórmula: DNL = (Vout(n) - Vout(n-1))/VlsbR - 1

    Args:
        vout (float): valor de Vout atual
        
        prev_vout (float): valor de Vout anterior
        
        vlsbr (float): valor de VlsbReal

    Returns:
        float: valor de DNL
    """
    
    try:
        # DNL = (Vout(n) - Vout(n-1))/VlsbR - 1
        dnl = (vout - prev_vout)/vlsbr - 1
        return dnl, True
    except:
        return 0, False

def calculate_linearity(num_bits, inl_values):
    """Calcula linearidade usando fórmula: nbits-log_2(INLmax-INLmin)
    
    Args:
        num_bits (int): número de bits
        
        inl_values (list): lista de valores INL
        
    Returns:
        float: valor de linearidade
    """
    try:
        # Filtra valores INL não numéricos
        numeric_inl = []
        for inl in inl_values:
            try:
                if inl != "ERROR" and inl != "N/A":
                    numeric_inl.append(float(inl))
            except:
                continue
        
        if len(numeric_inl) == 0:
            return "N/A"
            
        inl_max = max(numeric_inl)
        inl_min = min(numeric_inl)
        inl_range = inl_max - inl_min
        
        if inl_range <= 0:
            return "N/A"
            
        # Usando log10 e convertendo para log base 2
        linearity = num_bits - (log10(inl_range) / log10(2))
        return round(linearity, 3)
    except:
        return "N/A"

def inl_dnl_calculator():
    """Executa a Calculadora de Tabela INL/DNL
    
    Args:
        None
        
    Returns:
        None    
    """
    print("INL/DNL Table Calculator")
    print("-----------------------------")
    
    # Obtém número de bits
    try:
        num_bits = int(input("Enter number of bits (n): "))
        if num_bits <= 0:
            print("Invalid input. Using default of 5 bits.")
            num_bits = 5
    except:
        print("Invalid input. Using default of 5 bits.")
        num_bits = 5
    
    # Entrada valores mín e máx para cálculo do VlsbReal
    try:
        vout_min = float(input("Enter Vout_min value: "))
        vout_max = float(input("Enter Vout_max value: "))
        
        # Calcula VlsbReal
        vlsbr = calculate_vlsbr(vout_min, vout_max, num_bits)
        print(f"\nCalculated VlsbReal = {round(vlsbr, 6)}")
    except:
        print("Error in calculation. Please check your inputs.")
        return
    
    # Inicializa dados da tabela
    bits_list = []
    vout_list = []
    
    # Obtém número de entradas
    try:
        max_entries = 2**num_bits
        print(f"\nMaximum possible entries: {max_entries}")
        num_entries = int(input("How many entries in the table? "))
        if num_entries <= 0 or num_entries > max_entries:
            print(f"Invalid input. Using default of {max_entries}")
            num_entries = max_entries
    except:
        num_entries = 2**num_bits
        print(f"Invalid input. Using default of {num_entries}")
    
    # Coleta dados da tabela
    print("\nEnter data for each table row:")
    for i in range(num_entries):
        print(f"\nEntry {i+1}/{num_entries}:")
        
        # Obtém bits binários
        valid = False
        while not valid:
            binary_bits = input(f"Enter {num_bits} bits (binary): ")
            valid = True
            if len(binary_bits) != num_bits:
                valid = False
            else:
                for bit in binary_bits:
                    if bit != '0' and bit != '1':
                        valid = False
                        break
            
            if not valid:
                print(f"Invalid input! Enter {num_bits} bits (0s and 1s).")
        
        # Obtém valor Vout
        try:
            vout = float(input("Enter Vout value: "))
        except:
            print("Invalid input. Using 0.0")
            vout = 0.0
        
        # Armazena valores em listas
        bits_list.append(binary_bits)
        vout_list.append(vout)
    
    # Calcula INL e DNL e exibe tabela
    print("\n--- RESULTS TABLE ---")
    print("No. Bits  Dec  Vout   INL      DNL")
    print("-------------------------------")
    
    inl_list = []
    dnl_list = ["N/A"]  # First DNL is always N/A
    
    # Calcula todos os valores INL
    for i in range(num_entries):
        decimal_value = bin2dec(bits_list[i])
        inl, success = calculate_inl(vout_list[i], decimal_value, vlsbr, vout_min)
        if success:
            inl_list.append(str(round(inl, 6)))
        else:
            inl_list.append("ERROR")
    
    # Calcula todos os valores DNL (começando da segunda entrada)
    for i in range(1, num_entries):
        decimal_prev = bin2dec(bits_list[i-1])
        decimal_curr = bin2dec(bits_list[i])
        
        # Verifica se os códigos são consecutivos
        if decimal_curr == decimal_prev + 1:
            dnl, success = calculate_dnl(vout_list[i], vout_list[i-1], vlsbr)
            if success:
                dnl_list.append(str(round(dnl, 6)))
            else:
                dnl_list.append("ERROR")
        else:
            dnl_list.append("N/A")
    
    # Imprime a tabela completa
    for i in range(num_entries):
        decimal_value = bin2dec(bits_list[i])
        row = f"{i+1} {bits_list[i]} {decimal_value} {round(vout_list[i], 3)} {inl_list[i]} {dnl_list[i]}"
        print(row)
    
    # Calcula e exibe linearidade
    linearity = calculate_linearity(num_bits, inl_list)
    print(f"\nLinearity = {linearity} bits")
    print("Formula: nbits-log_2(INLmax-INLmin)")
    
    print("\nTable calculation complete.\nObrigado pela ajuda Nobrega!")

def snr_max_calculator():
    """Calculadora SNR max
    Args:
        None
    Returns:
        None
    """
    print("\nSNR max calculator")
    print("==================")
    
    # Obtém o número de bits
    num_bits = int(input("Number of bits: "))
    snr_max = SNR_FORMULA_SLOPE * num_bits + SNR_FORMULA_OFFSET
    print(f"\nSNR max = {snr_max} dB")
    print("Obrigado pela ajuda Nobrega!")
    
def snr_calculator():
    """Calculadora SNR que pode resolver para diferentes variáveis
    Args:
        None
    Returns:
        None
    """
    print("\nSNR Calculator")
    print("===============")
    
    # Pergunta ao usuário qual variável resolver
    print("Which variable would you like to solve for?")
    print("1. SNR")
    print("2. Number of bits (n)")
    choice = int(input("Enter your choice (1 or 2): "))
    
    # Entradas comuns independentemente do tipo de cálculo
    vin = float(input("Enter Vin value (V): "))
    vref = float(input("Enter Vref value (V): "))
    fin = float(input("Enter Fin value (MHz): "))
    djit = float(input("Enter jitter value (ps): "))
    
    # Converte unidades para cálculos
    # Converte MHz para Hz
    fin_hz = fin * 1e6
    # Converte ps para segundos
    djit_sec = djit * 1e-12
    
    # Calcula valor RMS do sinal de entrada
    vinrms = vin / SQRT_2
    print(f"\nVin RMS = {round(vinrms, 4)} V")
    
    # Verifica se jitter deve ser considerado
    consider_jitter = (djit_sec != 0) and (fin_hz != 0)
    
    if choice == 1:
        # Cálculo original - resolver para SNR
        n = int(input("Enter number of bits (n): "))
        vlsb = vref / (2**n)
        print(f"\nVlsb = {round(vlsb, 4)} V")
        vnqrms = vlsb / SQRT_12
        print(f"VNQ RMS = {round(vnqrms, 4)} V")
        
        if consider_jitter:
            vjitterns = vinrms * 2 * pi * fin_hz * djit_sec
            print(f"VJitter RMS = {round(vjitterns, 4)} V")
            snr = 10 * log10(vinrms**2 / (vnqrms**2 + vjitterns**2))
            print(f"\nSNR = {round(snr, 2)} dB (considering both quantization and jitter noise)")
        else:
            # Considera apenas ruído de quantização se jitter ou frequência for zero
            snr = 10 * log10(vinrms**2 / vnqrms**2)
            print(f"\nSNR = {round(snr, 2)} dB (considering only quantization noise)")
        
    elif choice == 2:
        # Novo cálculo - resolver para n (número de bits)
        snr = float(input("Enter SNR value (dB): "))
        
        # Converte SNR para escala linear
        snr_linear = 10**(snr/10)
        
        if consider_jitter:
            # Calcula ruído de jitter
            vjitterns = vinrms * 2 * pi * fin_hz * djit_sec
            print(f"VJitter RMS = {round(vjitterns, 4)} V")
            
            # Se o ruído de jitter for muito alto, SNR pode ser impossível de atingir
            jitter_limited_snr = 10 * log10(vinrms**2 / vjitterns**2)
            print(f"Jitter limited SNR = {round(jitter_limited_snr, 2)} dB")
            if jitter_limited_snr < snr:
                print(f"\nWarning: The requested SNR of {round(snr, 2)} dB cannot be achieved due to jitter limitations.")
                print(f"Maximum possible SNR with given jitter is {round(jitter_limited_snr, 2)} dB")
                return
            
            # Calcula máximo ruído de quantização permitido para alcançar SNR desejado
            vnqrms_max = (vinrms**2 / snr_linear - vjitterns**2)**0.5
            print(f"Maximum VNQ RMS = {round(vnqrms_max, 4)} V")
        else:
            # Se não houver jitter a considerar, o cálculo é mais simples
            vnqrms_max = vinrms / (snr_linear**0.5)
            print(f"Maximum VNQ RMS = {round(vnqrms_max, 4)} V")
        
        # Calcula valor LSB necessário
        vlsb_required = vnqrms_max * SQRT_12
        
        # Calcula número de bits necessário
        n_calculated = log(vref / vlsb_required) / log(2)
        
        # Arredonda para cima para o próximo inteiro, pois precisamos de pelo menos esse número de bits
        n_required = ceil(n_calculated)
        
        print(f"\nRequired number of bits (n) = {n_required}")
        print(f"(Exact calculated value: {round(n_calculated, 4)})")
        
        # Calcula o SNR real que será alcançado com esse número de bits
        vlsb_actual = vref / (2**n_required)
        vnqrms_actual = vlsb_actual / SQRT_12
        
        if consider_jitter:
            snr_actual = 10 * log10(vinrms**2 / (vnqrms_actual**2 + vjitterns**2))
            print(f"With {n_required} bits, the actual SNR will be {round(snr_actual, 2)} dB (considering both quantization and jitter noise)")
        else:
            snr_actual = 10 * log10(vinrms**2 / vnqrms_actual**2)
            print(f"With {n_required} bits, the actual SNR will be {round(snr_actual, 2)} dB (considering only quantization noise)")
    
    else:
        print("Invalid choice. Please run the program again.")
        
def dount_step_graph():
    """Calculadora de gráfico de passos Dout
    
    Args:
        None
        
    Returns:
        None
    """
    print("\nDout Step Graph")
    print("================")

    n = int(input("Número de bits (n): "))
    Vref = float(input("Vref (V): "))

    print("\nEscolhe o modo:")
    print("1 - Simétrico (Vin ∈ [-Vref/2, +Vref/2], Dout ∈ [0, 2^n - 1])")
    print("2 - Clássico  (Vin ∈ [0, Vref], Dout ∈ [0, 2^n - 1])")
    modo = input("Modo [1/2]: ").strip()
    Vlsb = Vref / (2**n)
    
    if modo == "1":
        Vin_min = -Vref / 2
        Vin_max = +Vref / 2
    else:
        Vin_min = 0
        Vin_max = Vref

    num_points = 1000
    Vin_values = []
    Dout_values = []

    for i in range(num_points + 1):
        Vin = Vin_min + (Vin_max - Vin_min) * i / num_points

        if modo == "1":
            Dout = int((Vin + Vref / 2) / Vlsb)
        else:
            Dout = int(Vin / Vlsb)

        Dout = max(0, min(Dout, 2**n - 1))  # saturação
        Vin_values.append(Vin)
        Dout_values.append(Dout)

    # Gráfico
    plt.figure(figsize=(8, 4))
    titulo = "Simétrico (centrado em 0)" if modo == "1" else "Clássico (0 a Vref)"
    plt.step(Vin_values, Dout_values, where='post')
    plt.title(f'Dout vs Vin ({n} bits) - {titulo}')
    plt.xlabel('Vin (V)')
    plt.ylabel('Dout')
    plt.grid(True)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.show()
    
def clock_freq_calculator():
    """Calculator for clock frequency"""
    print("\nClock Frequency Calculator")
    print("===========================")
    print("1 - Solve for n bits")
    print("2 - Solve for f")
    choice = int(input("Enter your choice (1 or 2): "))
    
    if choice == 1:
        # Resolve para n bits
        f = float(input("Enter f (MHz): "))
        try:
            pf = float(input("Enter power frequency (Default: 50 Hz): "))
        except:
            print("Invalid input. Using default of 50 Hz.")
            pf = 50
        n = ceil(log2(f * 1e6 / pf))
        print(f"Calculated n = {n} bits")
    elif choice == 2:
        # Resolve para freq 
        n = float(input("Enter n bits: "))
        try:
            pf = float(input("Enter power frequency (Default: 50 Hz): "))
        except:
            print("Invalid input. Using default of 50 Hz.")
            pf = 50
        q = 2**n
        t = 1 / pf
        f = (q / t)/1e6
        print(f"Calculated f = {f} MHz")
    else:
        print("Invalid choice. Please run the program again.")
        
def calculate_vlsb():
    """ Calcula Vlsb
    
    Args:
        None
        
    Returns:
        None
    """
    print("\nVlsb Calculator")
    print("======================")
    print("1 - Ideal")
    print("2 - Real")
    choice = int(input("Enter your choice (1 or 2): "))
    if choice == 1:
        num_bits = int(input("Enter number of bits (n): "))
        vref = float(input("Enter Vref value (V): "))
        vlsb_ideal = calculate_vlsbi(vref, num_bits)
        print(f"\nCalculated Ideal Vlsb = {round(vlsb_ideal, 3)}")
    elif choice == 2:
        vout_min = float(input("Enter Vout_min value: "))
        vout_max = float(input("Enter Vout_max value: "))
        num_bits = int(input("Enter number of bits (n): "))
        vlsb_real = calculate_vlsbr(vout_min, vout_max, num_bits)
        print(f"\nCalculated Real Vlsb = {round(vlsb_real, 3)}")
    else:
        print("Invalid choice. Please run the program again.")
        
def pipeline_dout():
    print("\nPipeline Simulator")
    print("======================")
    num_estagios = int(input("Número de stages do pipeline: "))
    bits_por_estagio = int(input("n bits por estágio: "))
    vref = float(input("Vref: "))
    vin = float(input("Vin: "))
    residuos = [vin]
    douts = []
    valores_dac = []
    print("\n--- Cálculos por stage ---")
    for i in range(num_estagios):
        vin_stage = residuos[-1]
        dout_bin = val_to_bin(vin_stage, vref, bits_por_estagio)
        douts.append(dout_bin)
        # calcular DAC correspondente
        nivel = int(dout_bin, 2)
        passo = vref / (2 ** bits_por_estagio)
        # Correção: O valor do DAC deve corresponder ao ponto médio do intervalo representado pelo código
        dac_val = -vref / 2 + (nivel + 0.5) * passo
        valores_dac.append(dac_val)
        if i < num_estagios - 1:
            # Correção: Resíduo é 2x(Vin-Vdac) em vez de 4x
            res = 2 * (vin_stage - dac_val)
            residuos.append(res)
        print(f"Stage {i + 1}:")
        print(f"  Vin: {vin_stage:.4f} V")
        print(f"  Dout: {dout_bin} (decimal: {nivel})")
        print(f"  DAC: {dac_val:.4f} V")
        if i < num_estagios - 1:
            print(f"  VRes: {res:.4f} V")
    # Correção digital
    bits_finais = douts[0]
    for i in range(1, num_estagios):
        bits_finais += douts[i][0]  # só MSB dos seguintes
    decimal_final = int(bits_finais, 2)
    nbits_total = len(bits_finais)
    delta = vref / (2 ** nbits_total)
    tensao_estim = -vref / 2 + decimal_final * delta
    print("\n=== Resultado Final ===")
    print("Bits concatenados:", bits_finais)
    print("Código decimal:   ", decimal_final)
    print(f"Tensão estimada:   {tensao_estim:.4f} V")

def pipeline_snr():
    snr_target = float(input("SNR desejado (dB): "))
    amplitude_sinal = float(input("Amplitude do sinal (V): "))
    vref = float(input("Valor de Vref (V): "))
    v_low_bound = float(input("Valor mínimo de Vin (assumir vref/2): "))
    v_high_bound = float(input("Valor máximo de Vin (assumir vref/2): "))
    bits_por_estagio = int(input("Bits por estágio (ex: 2): "))
    bits_redundantes = int(input("Bits redundantes por estágio (ex: 1): "))

    if amplitude_sinal > v_high_bound or amplitude_sinal < v_low_bound:
        print("\nA amplitude do sinal excede o limite. Verifica o intervalo do ADC.")
        return 

    # SNR real inclui penalização por amplitude
    penalizacao = 20 * log10(amplitude_sinal / (vref / 2))
    snr_ideal_necessaria = snr_target - penalizacao

    # Cálculo da resolução mínima N
    N = ceil((snr_ideal_necessaria - SNR_FORMULA_OFFSET) / SNR_FORMULA_SLOPE)

    # Estágios necessários:
    # - O primeiro estágio fornece todos os bits (sem redundância)
    # - Os seguintes fornecem apenas (bits_por_estagio - bits_redundantes)
    bits_primeiro = bits_por_estagio
    bits_restantes = N - bits_primeiro
    if bits_restantes <= 0:
        num_estagios = 1
    else:
        bits_por_estagio_util = bits_por_estagio - bits_redundantes
        if bits_por_estagio_util <= 0:
            print("\nErro: bits úteis por estágio após redundância é ≤ 0.")
            return
        num_estagios = 1 + ceil(bits_restantes / bits_por_estagio_util)

    # Resultados
    print("\n======== RESULTADOS ========")
    print(f"Resolução mínima necessária: {N} bits")
    print(f"Número mínimo de estágios do pipeline: {num_estagios}")
    print(f"Penalização de SNR por amplitude limitada: {penalizacao:.2f} dB")



def sd_snr():
    print("\nSigma-Delta SNR Calculator")
    print("================================")
    n = int(input("n bits: "))
    Vin = float(input("Introduz Vin (em volts): "))
    osr = float(input("Introduz o OSR: "))
    order = int(input("Introduz a ordem (1, 2 ou 3): "))

    if order not in [1, 2, 3]:
        print("Erro: ordem inválida.")
        return

    gains = {1: 30, 2: 50, 3: 70}
    corrections = {1: -5.17, 2: -12.9, 3: -20.9}

    snr = SNR_FORMULA_SLOPE * n + SNR_FORMULA_OFFSET + gains[order] * log10(osr) + corrections[order] + 20 * log10(Vin)
    print(f"\nSNR calculado: {snr:.2f} dB")

def sd_osr():
    print("\nSigma-Delta OSR Calculator (com V_REF e V_lsb)")
    print("===============================================")
    order = int(input("Introduz a ordem do modulador Sigma-Delta (1, 2 ou 3): "))
    snr = float(input("Introduz o SNR alvo (em dB): "))
    n = int(input("Introduz o número de bits do quantizador (e.g. 1 ou 3): "))
    Vin = float(input("Introduz Vin (em volts): "))

    if order not in [1, 2, 3]:
        print("Erro: ordem inválida.")
        return

    gains = {1: 30, 2: 50, 3: 70}
    corrections = {1: -5.17, 2: -12.9, 3: -20.9}

    osr = 10**((snr - SNR_FORMULA_OFFSET - SNR_FORMULA_SLOPE * n - corrections[order] - 20 * log10(Vin)) / gains[order])
    print(f"\nOSR necessário para atingir SNR de {snr} dB: {osr:.3f}")
    
    
def main():
    """Função de menu principal
    
    Args:
        None
        
    Returns:
        None
    """
    while True:
        print("\n===================================")
        print("      CONVERSORES DE SINAL")
        print("         NOBREGA 2025")
        print("==================================")
        print("1. Vlsb Calculator")
        print("2. INL/DNL Table Calculator")
        print("3. SNR Tools")
        print("4. Pipeline Tools")
        print("5. Clock Frequency Calculator")
        print("6. Sigma-Delta Tools")
        
        print("0. Exit")
        print("----------------------------------")
        
        try:
            choice = int(input("Enter your choice (0-5): "))
            
            if choice == 0:
                print("Exiting program. Obrigado e volte sempre!")
                break
            elif choice == 1:
                calculate_vlsb()
                
            elif choice == 2:
                inl_dnl_calculator()
                
            elif choice == 3:
                print("SNR Tools")
                print("1. SNRMax Calculator") 
                print("2. SNR Calculator")
                snr_choice = int(input("Enter your choice (1 or 2): "))
                if snr_choice == 1:
                    snr_max_calculator()
                elif snr_choice == 2:
                    snr_calculator()
                else:
                    print("Invalid choice. Please try again.")
                    
            elif choice == 4:
                print("Pipeline Tools")
                print("1. Dout Step Graph")
                print("2. Pipeline SNR")
                print("3. Pipeline Dout")
                pipeline_choice = int(input("Enter your choice (1-3): "))
                if pipeline_choice == 1:
                    dount_step_graph()
                elif pipeline_choice == 2:
                    pipeline_snr()
                elif pipeline_choice == 3:
                    pipeline_dout()
                else:
                    print("Invalid choice. Please try again.")
                    
            elif choice == 5:
                clock_freq_calculator()
                
            elif choice == 6:
                print("Sigma-Delta Tools")
                print("1. SD SNR")
                print("2. OSR")
                sigma_delta_choice = int(input("Enter your choice (1-3): "))
                if sigma_delta_choice == 1:
                    sd_snr()
                if sigma_delta_choice == 2:
                    sd_osr()
                else:
                    print("Invalid choice. Please try again.")
                
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid option (0-5).")
        
        input("\nPress Enter to return to main menu...")

# Execute program only if run directly
if __name__ == "__main__":
    main()
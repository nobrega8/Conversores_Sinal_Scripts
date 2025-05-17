# INL e DNL Calculator
# Copyright © 2025 Barraca Familia Software
# Para Texas Nspire CX II-T CAS

from math import *

def binary_to_decimal(binary_bits):
    """Converte string binária para valor decimal"""
    return int(binary_bits, 2)

def calculate_vlsbr(vout_min, vout_max, num_bits):
    """Calcula VlsbReal usando fórmula: (VoutMax - VoutMin)/(2^n - 1)"""
    try:
        return (vout_max - vout_min)/(2**num_bits - 1)
    except:
        return 0

def calculate_inl(vout, decimal_value, vlsbr, vout_min):
    try:
        # Aplica fórmula INL: INL = (Vout - n*VlsbR - Vout_min)/VlsbR 
        inl = (vout - decimal_value*vlsbr - vout_min)/vlsbr 
        return inl, True
    except:
        return 0, False

def calculate_dnl(vout, prev_vout, vlsbr):
    try:
        # DNL = (Vout(n) - Vout(n-1))/VlsbR - 1
        dnl = (vout - prev_vout)/vlsbr - 1
        return dnl, True
    except:
        return 0, False

def calculate_linearity(num_bits, inl_values):
    """Calcula linearidade usando fórmula: nbits-log_2(INLmax-INLmin)"""
    try:
        # Filtra valores INL não numéricos
        numeric_inl = []
        for inl in inl_values:
            try:
                if inl != "Drena n Bazofa" and inl != "nepia":
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
    """Executa a Calculadora de Tabela INL/DNL"""
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
        print("\nCalculated VlsbReal = " + str(round(vlsbr, 6)))
    except:
        print("Error in calculation. Please check your inputs.")
        return
    
    # Inicializa dados da tabela
    bits_list = []
    vout_list = []
    
    # Obtém número de entradas
    try:
        max_entries = 2**num_bits
        print("\nMaximum possible entries: " + str(max_entries))
        num_entries = int(input("How many entries in the table? "))
        if num_entries <= 0 or num_entries > max_entries:
            print("Invalid input. Using default of " + str(max_entries))
            num_entries = max_entries
    except:
        num_entries = 2**num_bits
        print("Invalid input. Using default of " + str(num_entries))
    
    # Coleta dados da tabela
    print("\nEnter data for each table row:")
    for i in range(num_entries):
        print("\nEntry " + str(i+1) + "/" + str(num_entries) + ":")
        
        # Obtém bits binários
        valid = False
        while not valid:
            binary_bits = input("Enter " + str(num_bits) + " bits (binary): ")
            valid = True
            if len(binary_bits) != num_bits:
                valid = False
            else:
                for bit in binary_bits:
                    if bit != '0' and bit != '1':
                        valid = False
                        break
            
            if not valid:
                print("Invalid input! Enter " + str(num_bits) + " bits (0s and 1s).")
        
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
    dnl_list = ["nepia"]  # Primeiro DNL é sempre N/A
    
    # Calcula todos os valores INL
    for i in range(num_entries):
        decimal_value = binary_to_decimal(bits_list[i])
        inl, success = calculate_inl(vout_list[i], decimal_value, vlsbr, vout_min)
        if success:
            inl_list.append(str(round(inl, 6)))
        else:
            inl_list.append("Drena n Bazofa")
    
    # Calcula todos os valores DNL (começando da segunda entrada)
    for i in range(1, num_entries):
        decimal_prev = binary_to_decimal(bits_list[i-1])
        decimal_curr = binary_to_decimal(bits_list[i])
        
        # Verifica se os códigos são consecutivos
        if decimal_curr == decimal_prev + 1:
            dnl, success = calculate_dnl(vout_list[i], vout_list[i-1], vlsbr)
            if success:
                dnl_list.append(str(round(dnl, 6)))
            else:
                dnl_list.append("Drena n Bazofa")
        else:
            dnl_list.append("nepia")
    
    # Imprime a tabela completa
    for i in range(num_entries):
        decimal_value = binary_to_decimal(bits_list[i])
        row = str(i+1) + " " + bits_list[i] + " " + str(decimal_value)
        row += " " + str(round(vout_list[i], 3))
        row += " " + inl_list[i] + " " + dnl_list[i]
        print(row)
    
    # Calcula e exibe linearidade
    linearity = calculate_linearity(num_bits, inl_list)
    print("\nLinearity = " + str(linearity) + " bits")
    print("Formula: nbits-log_2(INLmax-INLmin)")
    
    print("\nTable calculation complete.\nObrigado pela ajuda Nobrega!")

def snr_max_calculator():
    """Calculadora SNR max"""
    print("\nSNR max calculator")
    print("\nBipolar->Vref*2")
    print("==================")
    print("Resolver para: ")
    print("1. SNR max")
    print("2. Numero de bits (n)")
    choice = int(input("Escolha (1-2): "))
    
    if choice == 2:
        # Cálculo SNR max
        snr_max = float(input("SNR max (dB): "))
        num_bits = (snr_max - 1.76) / 6.02
        print("\nNumber of bits = " + str(ceil(num_bits)))
        print("Obrigado pela ajuda Nobrega!")
    elif choice == 1:
        # Cálculo número de bits
        num_bits = int(input("Number of bits: "))
        snr_max = 6.02 * num_bits + 1.76
        print("\nSNR max = " + str(snr_max) + " dB")
        print("Obrigado pela ajuda Nobrega!")
    else:
        print("Opção inválida!")
        print("Obrigado pela ajuda Nobrega!")
    
def snr_calculator():
    """Calculadora SNR que pode resolver para diferentes variáveis"""
    print("\nSNR Calculator")
    print("\nBipolar->Vref*2")
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
    vinrms = vin / (2**0.5)
    print("\nVin RMS = " + str(round(vinrms, 4)) + " V")
    
    # Verifica se jitter deve ser considerado
    consider_jitter = (djit_sec != 0) and (fin_hz != 0)
    
    if choice == 1:
        # Cálculo original - resolver para SNR
        n = int(input("Enter number of bits (n): "))
        vlsb = vref / (2**n)
        print("\nVlsb = " + str(round(vlsb, 4)) + " V")
        vnqrms = vlsb / (12**0.5)
        print("VNQ RMS = " + str(round(vnqrms, 4)) + " V")
        
        if consider_jitter:
            vjitterns = vinrms * 2 * pi * fin_hz * djit_sec
            print("VJitter RMS = " + str(round(vjitterns, 4)) + " V")
            snr = 10 * log10(vinrms**2 / (vnqrms**2 + vjitterns**2))
            print("\nSNR = " + str(round(snr, 2)) + " dB (considering both quantization and jitter noise)")
        else:
            # Considera apenas ruído de quantização se jitter ou frequência for zero
            snr = 10 * log10(vinrms**2 / vnqrms**2)
            print("\nSNR = " + str(round(snr, 2)) + " dB (considering only quantization noise)")
        
    elif choice == 2:
        # Novo cálculo - resolver para n (número de bits)
        snr = float(input("Enter SNR value (dB): "))
        
        # Converte SNR para escala linear
        snr_linear = 10**(snr/10)
        
        if consider_jitter:
            # Calcula ruído de jitter
            vjitterns = vinrms * 2 * pi * fin_hz * djit_sec
            print("VJitter RMS = " + str(round(vjitterns, 4)) + " V")
            
            # Se o ruído de jitter for muito alto, SNR pode ser impossível de atingir
            jitter_limited_snr = 10 * log10(vinrms**2 / vjitterns**2)
            print("Jitter limited SNR = " + str(round(jitter_limited_snr, 2)) + " dB")
            if jitter_limited_snr < snr:
                print("\nWarning: The requested SNR of " + str(round(snr, 2)) + " dB cannot be achieved due to jitter limitations.")
                print("Maximum possible SNR with given jitter is " + str(round(jitter_limited_snr, 2)) + " dB")
                return
            
            # Calcula máximo ruído de quantização permitido para alcançar SNR desejado
            vnqrms_max = (vinrms**2 / snr_linear - vjitterns**2)**0.5
            print("Maximum VNQ RMS = " + str(round(vnqrms_max, 4)) + " V")
        else:
            # Se não houver jitter a considerar, o cálculo é mais simples
            vnqrms_max = vinrms / (snr_linear**0.5)
            print("Maximum VNQ RMS = " + str(round(vnqrms_max, 4)) + " V")
        
        # Calcula valor LSB necessário
        vlsb_required = vnqrms_max * (12**0.5)
        
        # Calcula número de bits necessário
        n_calculated = log(vref / vlsb_required) / log(2)
        
        # Arredonda para cima para o próximo inteiro, pois precisamos de pelo menos esse número de bits
        n_required = ceil(n_calculated)
        
        print("\nRequired number of bits (n) = " + str(n_required))
        print("(Exact calculated value: " + str(round(n_calculated, 4)) + ")")
        
        # Calcula o SNR real que será alcançado com esse número de bits
        vlsb_actual = vref / (2**n_required)
        vnqrms_actual = vlsb_actual / (12**0.5)
        
        if consider_jitter:
            snr_actual = 10 * log10(vinrms**2 / (vnqrms_actual**2 + vjitterns**2))
            print("With " + str(n_required) + " bits, the actual SNR will be " + str(round(snr_actual, 2)) + " dB (considering both quantization and jitter noise)")
        else:
            snr_actual = 10 * log10(vinrms**2 / vnqrms_actual**2)
            print("With " + str(n_required) + " bits, the actual SNR will be " + str(round(snr_actual, 2)) + " dB (considering only quantization noise)")
    
    else:
        print("Invalid choice. Please run the program again.")

def main():
    """Função de menu principal"""
    while True:
        print("\n===================================")
        print("      CONVERSORES DE SINAL")
        print("         NOBREGA 2025")
        print("==================================")
        print("1. INL/DNL Table Calculator")
        print("2. SNRMax Calculator")
        print("3. SNR Calculator")
        print("0. Exit")
        print("----------------------------------")
        
        try:
            choice = int(input("Enter your choice (0-3): "))
            
            if choice == 0:
                print("Exiting program. Obrigado e volte sempre!")
                break
            elif choice == 1:
                inl_dnl_calculator()
            elif choice == 2:
                snr_max_calculator()
            elif choice == 3:
                snr_calculator()
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid option (0-3).")
        
        input("\nPress Enter to return to main menu...")

# Executa programa
main()
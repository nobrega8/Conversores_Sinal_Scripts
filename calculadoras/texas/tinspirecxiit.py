## Texas Instruments
## Nspire CX II T
## 2025 (c) Afonso Nóbrega
## v2.6.1

from math import *

def binary_to_decimal(binary_bits):
    return int(binary_bits, 2)

def bin_to_val(bin_str, vref, bits):
    n = int(bin_str, 2)
    max_n = 2**bits - 1
    p = vref/(2**bits)
    return -vref/2 + n * p

def val_to_bin(val, vref, bits):
    steps = 2**bits
    delta = vref/steps
    code = int((val+vref/2)/delta)
    code = max(0, min(code, steps-1))
    result = ""
    temp = code
    for i in range(bits):
        result = str(temp % 2) + result
        temp = temp // 2
        
    return result

def calculate_vlsbr(vout_min, vout_max, num_bits):
    try:
        return (vout_max - vout_min)/(2**num_bits - 1)
    except:
        return 0
    
def calculate_vlsbi(vref, num_bits):
    try:
        return vref/(2**num_bits)
    except:
        return 0

def calculate_inl(vout, decimal_value, vlsbr, vout_min):
    try:
        inl = (vout - decimal_value*vlsbr - vout_min)/vlsbr 
        return inl, True
    except:
        return 0, False

def calculate_dnl(vout, prev_vout, vlsbr):
    try:
        dnl = (vout - prev_vout)/vlsbr - 1
        return dnl, True
    except:
        return 0, False

def calculate_linearity(num_bits, inl_values):
    try:
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
            
        linearity = num_bits - (log10(inl_range) / log10(2))
        return round(linearity, 3)
    except:
        return "N/A"

def inl_dnl_calculator():
    print("INL/DNL Table Calculator")
    print("-----------------------------")
    
    try:
        num_bits = int(input("Enter number of bits (n): "))
        if num_bits <= 0:
            print("Invalid input. Using default of 5 bits.")
            num_bits = 5
    except:
        print("Invalid input. Using default of 5 bits.")
        num_bits = 5
    
    try:
        vout_min = float(input("Enter Vout_min value: "))
        vout_max = float(input("Enter Vout_max value: "))
        
        vlsbr = calculate_vlsbr(vout_min, vout_max, num_bits)
        print("\nCalculated VlsbReal = " + str(round(vlsbr, 6)))
    except:
        print("Error in calculation. Please check your inputs.")
        return
    
    bits_list = []
    vout_list = []
    
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
    
    print("\nEnter data for each table row:")
    for i in range(num_entries):
        print("\nEntry " + str(i+1) + "/" + str(num_entries) + ":")
        
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
        
        try:
            vout = float(input("Enter Vout value: "))
        except:
            print("Invalid input. Using 0.0")
            vout = 0.0

        bits_list.append(binary_bits)
        vout_list.append(vout)
    
    print("\n--- RESULTS TABLE ---")
    print("No. Bits  Dec  Vout   INL      DNL")
    print("-------------------------------")
    
    inl_list = []
    dnl_list = ["nepia"]  

    for i in range(num_entries):
        decimal_value = binary_to_decimal(bits_list[i])
        inl, success = calculate_inl(vout_list[i], decimal_value, vlsbr, vout_min)
        if success:
            inl_list.append(str(round(inl, 6)))
        else:
            inl_list.append("Drena n Bazofa")

    for i in range(1, num_entries):
        decimal_prev = binary_to_decimal(bits_list[i-1])
        decimal_curr = binary_to_decimal(bits_list[i])
        
        if decimal_curr == decimal_prev + 1:
            dnl, success = calculate_dnl(vout_list[i], vout_list[i-1], vlsbr)
            if success:
                dnl_list.append(str(round(dnl, 6)))
            else:
                dnl_list.append("Drena n Bazofa")
        else:
            dnl_list.append("nepia")
    
    for i in range(num_entries):
        decimal_value = binary_to_decimal(bits_list[i])
        row = str(i+1) + " " + bits_list[i] + " " + str(decimal_value)
        row += " " + str(round(vout_list[i], 3))
        row += " " + inl_list[i] + " " + dnl_list[i]
        print(row)
    
    linearity = calculate_linearity(num_bits, inl_list)
    print("\nLinearity = " + str(linearity) + " bits")
    print("Formula: nbits-log_2(INLmax-INLmin)")
    
    print("\nTable calculation complete.\nObrigado pela ajuda Nobrega!")

def snr_max_calculator():
    print("\nSNR max calculator")
    print("\nBipolar->Vref*2")
    print("==================")
    print("Resolver para: ")
    print("1. SNR max")
    print("2. Numero de bits (n)")
    choice = int(input("Escolha (1-2): "))
    
    if choice == 2:
        snr_max = float(input("SNR max (dB): "))
        num_bits = (snr_max - 1.76) / 6.02
        print("\nNumber of bits = " + str(ceil(num_bits)))
        print("Obrigado pela ajuda Nobrega!")
    elif choice == 1:
        num_bits = int(input("Number of bits: "))
        snr_max = 6.02 * num_bits + 1.76
        print("\nSNR max = " + str(snr_max) + " dB")
        print("Obrigado pela ajuda Nobrega!")
    else:
        print("Opção inválida!")
        print("Obrigado pela ajuda Nobrega!")
    
def snr_calculator():
    print("\nSNR Calculator")
    print("\nBipolar->Vref*2")
    print("===============")

    print("Which variable would you like to solve for?")
    print("1. SNR")
    print("2. Number of bits (n)")
    choice = int(input("Enter your choice (1 or 2): "))

    vin = float(input("Enter Vin value (V): "))
    vref = float(input("Enter Vref value (V): "))
    fin = float(input("Enter Fin value (MHz): "))
    djit = float(input("Enter jitter value (ps): "))
    
    fin_hz = fin * 1e6

    djit_sec = djit * 1e-12
    
    vinrms = vin / (2**0.5)
    print("\nVin RMS = " + str(round(vinrms, 4)) + " V")
    
    consider_jitter = (djit_sec != 0) and (fin_hz != 0)
    
    if choice == 1:
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
            snr = 10 * log10(vinrms**2 / vnqrms**2)
            print("\nSNR = " + str(round(snr, 2)) + " dB (considering only quantization noise)")
        
    elif choice == 2:
        snr = float(input("Enter SNR value (dB): "))
        
        snr_linear = 10**(snr/10)
        
        if consider_jitter:
            vjitterns = vinrms * 2 * pi * fin_hz * djit_sec
            print("VJitter RMS = " + str(round(vjitterns, 4)) + " V")
            jitter_limited_snr = 10 * log10(vinrms**2 / vjitterns**2)
            print("Jitter limited SNR = " + str(round(jitter_limited_snr, 2)) + " dB")
            if jitter_limited_snr < snr:
                print("\nWarning: The requested SNR of " + str(round(snr, 2)) + " dB cannot be achieved due to jitter limitations.")
                print("Maximum possible SNR with given jitter is " + str(round(jitter_limited_snr, 2)) + " dB")
                return
            
            vnqrms_max = (vinrms**2 / snr_linear - vjitterns**2)**0.5
            print("Maximum VNQ RMS = " + str(round(vnqrms_max, 4)) + " V")
        else:
            vnqrms_max = vinrms / (snr_linear**0.5)
            print("Maximum VNQ RMS = " + str(round(vnqrms_max, 4)) + " V")
        
        vlsb_required = vnqrms_max * (12**0.5)
        
        n_calculated = log(vref / vlsb_required) / log(2)
        
        n_required = ceil(n_calculated)
        
        print("\nRequired number of bits (n) = " + str(n_required))
        print("(Exact calculated value: " + str(round(n_calculated, 4)) + ")")
        
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
        
def dout_step_graph():
    print("\nDout Step Table")
    print("================")

    n = int(input("Número de bits (n): "))
    Vref = float(input("Vref (V): "))

    print("\nEscolhe o modo:")
    print("1 - Simétrico (Vin ∈ [-Vref/2, +Vref/2], Dout ∈ [0, 2^n])")
    print("2 - Clássico  (Vin ∈ [0, Vref], Dout ∈ [0, 2^n - 1])")
    modo = input("Modo [1/2]: ")

    Vlsb = Vref / (2 ** n)

    if modo == "1":
        Vin_min = -Vref / 2
        Vin_max = +Vref / 2
    else:
        Vin_min = 0
        Vin_max = Vref

    total_pontos = 2 * (2 ** n)
    step_size = (Vin_max - Vin_min) / (total_pontos - 1)

    print("\n{:>6} | {:>6}".format("Vin", "Dout"))
    print("-" * 15)

    for i in range(total_pontos):
        Vin = Vin_min + i * step_size

        if modo == "1":
            Dout = round(Vin / Vlsb) + 2**(n - 1)
            Dout = max(0, min(Dout, 2**n))  
        else:
            Dout = floor(Vin / Vlsb)
            Dout = max(0, min(Dout, 2**n - 1))  

        print("{:6.3f} | {:6}".format(Vin, Dout))
        
def clock_freq_calculator():
    print("\nClock Frequency Calculator")
    print("==============================")
    print("1 - Solve for n bits")
    print("2 - Solve for f")
    
    choice = int(input("Choose (1-2): "))
    
    if choice == 1:
        f = float(input("Enter f (MHz): "))
        pf = float(input("Enter power f (Hz (default=50)): ") or "50")
        n = ceil(log2(f*1e6 / pf))
        print("n bits =", n, "bits")
    
    elif choice == 2:
        n = int(input("Enter n bits: "))
        pf = float(input("Enter power f (Hz (default=50)): ") or "50")
        q = 2**n
        t = 1 / pf
        f = (q/t) / 1e6
        print("f =", f, "MHz")
    
    else:
        print("Invalid option. Please try again.")

def calculate_vlsb():
    print("\nVlsb Calculator")
    print("======================")
    print("1 - Ideal")
    print("2 - Real")
    choice = int(input("(1 or 2): "))
    if choice == 1:
        num_bits = int(input("n bits (n): "))
        vref = float(input("Vref (V): "))
        vlsb_ideal = calculate_vlsbi(vref, num_bits)
        print("\nIdeal Vlsb = " + str(round(vlsb_ideal, 3)))
    elif choice == 2:
        vout_min = float(input("Vout_min: "))
        vout_max = float(input("Vout_max: "))
        num_bits = int(input("n bits (n): "))
        vlsb_real = calculate_vlsbr(vout_min, vout_max, num_bits)
        print("\nCalculated Real Vlsb = " + str(round(vlsb_real, 3)))
    else:
        print("Invalid choice.")

def pipeline_dout():
    print("\nPipeline Simulator")
    print("======================")
    num_estagios = int(input("stages do pipeline: "))
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
        nivel = int(dout_bin, 2)
        passo = vref / (2 ** bits_por_estagio)
        dac_val = -vref / 2 + (nivel + 0.5) * passo
        valores_dac.append(dac_val)
        
        if i < num_estagios - 1:
            res = 2 * (vin_stage - dac_val)
            residuos.append(res)
            
        print("Stage " + str(i + 1) + ":")
        print("  Vin: {:.4f} V".format(vin_stage))
        print("  Dout: " + dout_bin + " (decimal: " + str(nivel) + ")")
        print("  DAC: {:.4f} V".format(dac_val))
        if i < num_estagios - 1:
            print("  VRes: {:.4f} V".format(res))
    
    # Construindo resultado final
    bits_finais = douts[0]
    for i in range(1, num_estagios):
        bits_finais += douts[i][0]
    
    decimal_final = int(bits_finais, 2)
    nbits_total = len(bits_finais)
    delta = vref / (2 ** nbits_total)
    tensao_estim = -vref / 2 + decimal_final * delta
    
    print("\n=== Resultado Final ===")
    print("Bits concatenados: " + bits_finais)
    print("Código decimal:    " + str(decimal_final))
    print("Tensão estimada:   {:.4f} V".format(tensao_estim))
    
def pipeline_snr():
    print("\nPipeline SNR Calculator")
    print("=======================")
    
    snr_target = float(input("SNR desejado (dB): "))
    amplitude_sinal = float(input("Amplitude do sinal (V): "))
    vref = float(input("Valor de Vref (V): "))
    v_low_bound = float(input("Valor mínimo de Vin (assumir -vref/2): ") or str(-vref/2))
    v_high_bound = float(input("Valor máximo de Vin (assumir vref/2): ") or str(vref/2))
    bits_por_estagio = int(input("Bits por estágio (ex: 2): "))
    bits_redundantes = int(input("Bits redundantes por estágio (ex: 1): "))
    
    if amplitude_sinal > v_high_bound or amplitude_sinal < v_low_bound:
        print("\nA amplitude do sinal excede o limite. Verifica o intervalo do ADC.")
        return
    
    penalizacao = 20 * log10(amplitude_sinal / (vref / 2))
    snr_ideal_necessaria = snr_target - penalizacao
    N = ceil((snr_ideal_necessaria - 1.76) / 6.02)
    
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
    
    print("\n======== RESULTADOS ========")
    print("Resolução mínima necessária: {} bits".format(N))
    print("Número mínimo de estágios do pipeline: {}".format(num_estagios))
    print("Penalização de SNR por amplitude limitada: {:.2f} dB".format(penalizacao))


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
                    dout_step_graph()
                elif pipeline_choice == 2:
                    pipeline_snr()
                elif pipeline_choice == 3:
                    pipeline_dout()
                else:
                    print("Invalid choice. Please try again.")
                    
            elif choice == 5:
                clock_freq_calculator()
                
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid option (0-5).")
        
        input("\nPress Enter to return to main menu...")

main()
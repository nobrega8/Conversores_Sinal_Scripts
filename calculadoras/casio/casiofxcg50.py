## Casio
## Fx-CG50
## 2025 (c) Afonso Nóbrega
## v3.0.0

from math import *

def bin2dec(b):
    """Convert binary string to decimal"""
    return int(b, 2)

def calc_vlsbr(vmin, vmax, n):
    """Calculate VlsbReal"""
    try:
        return (vmax - vmin)/(2**n - 1)
    except:
        return 0
    
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

def calc_inl(vout, dec, vlsbr, vmin):
    """Calculate INL"""
    try:
        inl = (vout - dec*vlsbr - vmin)/vlsbr
        return inl, True
    except:
        return 0, False

def calc_dnl(vout, prev, vlsbr):
    """Calculate DNL"""
    try:
        dnl = (vout - prev)/vlsbr - 1
        return dnl, True
    except:
        return 0, False

def calc_linear(n, inl_vals):
    """Calculate linearity"""
    try:
        nums = []
        for inl in inl_vals:
            try:
                if inl != "Error" and inl != "N/A":
                    nums.append(float(inl))
            except:
                continue
        
        if len(nums) == 0:
            return "N/A"
            
        inl_max = max(nums)
        inl_min = min(nums)
        inl_range = inl_max - inl_min
        
        if inl_range <= 0:
            return "N/A"
            
        lin = n - (log10(inl_range) / log10(2))
        return round(lin, 3)
    except:
        return "N/A"

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

def inl_dnl_calc():
    """INL/DNL Table Calculator"""
    print("INL/DNL Calculator")
    print("-----------------")
    
    # Get number of bits
    try:
        n = int(input("Bits (n): "))
        if n <= 0:
            print("Invalid. Using n=5")
            n = 5
    except:
        print("Invalid. Using n=5")
        n = 5
    
    # Min and max values
    try:
        vmin = float(input("Vout_min: "))
        vmax = float(input("Vout_max: "))
        
        # Calculate VlsbReal
        vlsbr = calc_vlsbr(vmin, vmax, n)
        print("VlsbReal = "+str(round(vlsbr,6)))
    except:
        print("Error in calculation.")
        return
    
    # Initialize table data
    bits = []
    vouts = []
    
    # Get number of entries
    try:
        max_ent = 2**n
        print("Max entries: " + str(max_ent))
        num_ent = int(input("# entries: "))
        if num_ent <= 0 or num_ent > max_ent:
            print("Invalid. Using " + str(max_ent))
            num_ent = max_ent
    except:
        num_ent = 2**n
        print("Invalid. Using " + str(num_ent))
    
    # Collect table data
    print("Enter data for each row:")
    for i in range(num_ent):
        print("Entry " + str(i+1) + "/" + 
              str(num_ent) + ":")
        
        # Get binary bits
        valid = False
        while not valid:
            b = input(str(n) + " bits: ")
            valid = True
            if len(b) != n:
                valid = False
            else:
                for bit in b:
                    if bit != '0' and bit != '1':
                        valid = False
                        break
            
            if not valid:
                print("Invalid! Enter "+str(n)+" bits")
        
        # Get Vout value
        try:
            v = float(input("Vout: "))
        except:
            print("Invalid. Using 0.0")
            v = 0.0
        
        # Store values
        bits.append(b)
        vouts.append(v)
    
    # Calculate INL and DNL
    print("--- RESULTS ---")
    print("No. Bits Dec Vout INL DNL")
    
    inl_list = []
    dnl_list = ["N/A"]  # First DNL is N/A
    
    # Calculate all INL values
    for i in range(num_ent):
        dec = bin2dec(bits[i])
        inl, ok = calc_inl(vouts[i], dec, vlsbr, vmin)
        if ok:
            inl_list.append(str(round(inl, 6)))
        else:
            inl_list.append("Error")
    
    # Calculate all DNL values
    for i in range(1, num_ent):
        d_prev = bin2dec(bits[i-1])
        d_curr = bin2dec(bits[i])
        
        # Check consecutive codes
        if d_curr == d_prev + 1:
            dnl, ok = calc_dnl(vouts[i], vouts[i-1], vlsbr)
            if ok:
                dnl_list.append(str(round(dnl, 6)))
            else:
                dnl_list.append("Error")
        else:
            dnl_list.append("N/A")
    
    # Print complete table
    for i in range(num_ent):
        dec = bin2dec(bits[i])
        row = str(i+1) + " " + bits[i] + " " + str(dec)
        row += " " + str(round(vouts[i], 3))
        row += " " + inl_list[i] + " " + dnl_list[i]
        print(row)
    
    # Calculate linearity
    lin = calc_linear(n, inl_list)
    print("Linearity = " + str(lin) + " bits")
    print("Formula: n-log2(INLmax-INLmin)")

def snr_max_calc():
    """SNR max calculator"""
    print("SNR max calculator")
    print("=================")
    print("Solve for: ")
    print("1. SNR max")
    print("2. Number of bits (n)")
    ch = int(input("Choice (1-2): "))
    
    if ch == 2:
        # Calculate SNR max
        snr = float(input("SNR max (dB): "))
        n = (snr - 1.76) / 6.02
        print("Number of bits = " + str(ceil(n)))
    elif ch == 1:
        # Calculate bits
        n = int(input("Number of bits: "))
        snr = 6.02 * n + 1.76
        print("SNR max = " + str(snr) + " dB")
    else:
        print("Invalid option!")
    
def snr_calc():
    """SNR Calculator"""
    print("SNR Calculator")
    print("=============")
    
    print("Solve for:")
    print("1. SNR")
    print("2. Number of bits (n)")
    ch = int(input("Choice (1-2): "))
    
    vin = float(input("Vin (V): "))
    vref = float(input("Vref (V): "))
    fin = float(input("Fin (MHz): "))
    djit = float(input("Jitter (ps): "))
    
    # Convert units
    fin_hz = fin * 1e6
    djit_sec = djit * 1e-12
    
    # Calculate RMS input
    vinrms = vin / (2**0.5)
    print("Vin RMS = " + str(round(vinrms, 4)) + " V")
    
    # Check if jitter should be considered
    use_jit = (djit_sec != 0) and (fin_hz != 0)
    
    if ch == 1:
        # Solve for SNR
        n = int(input("Bits (n): "))
        vlsb = vref / (2**n)
        print("Vlsb = " + str(round(vlsb, 4)) + " V")
        vnqrms = vlsb / (12**0.5)
        print("VNQ RMS = " + str(round(vnqrms, 4)) + " V")
        
        if use_jit:
            vjit = vinrms * 2 * pi * fin_hz * djit_sec
            print("VJit RMS = " + str(round(vjit, 4)) + " V")
            snr = 10 * log10(vinrms**2 / (vnqrms**2 + vjit**2))
            print("SNR = " + str(round(snr, 2)) + " dB")
            print("(with quant+jitter noise)")
        else:
            snr = 10 * log10(vinrms**2 / vnqrms**2)
            print("SNR = " + str(round(snr, 2)) + " dB")
            print("(quant noise only)")
        
    elif ch == 2:
        # Solve for n
        snr = float(input("SNR (dB): "))
        
        # Convert SNR to linear scale
        snr_lin = 10**(snr/10)
        
        if use_jit:
            # Calculate jitter noise
            vjit = vinrms * 2 * pi * fin_hz * djit_sec
            print("VJit RMS = " + str(round(vjit, 4)) + " V")
            
            # Check if jitter is too high
            jit_snr = 10 * log10(vinrms**2 / vjit**2)
            print("Jitter SNR limit = " + str(round(jit_snr, 2)) + " dB")
            if jit_snr < snr:
                print("WARNING: Requested SNR can't be achieved")
                print("Max possible SNR with jitter: " + str(round(jit_snr, 2)) + " dB")
                return
            
            # Calculate max quant noise allowed
            vnq_max = (vinrms**2 / snr_lin - vjit**2)**0.5
            print("Max VNQ = " + str(round(vnq_max, 4)) + " V")
        else:
            # Simpler calc without jitter
            vnq_max = vinrms / (snr_lin**0.5)
            print("Max VNQ = " + str(round(vnq_max, 4)) + " V")
        
        # Calculate required LSB
        vlsb_req = vnq_max * (12**0.5)
        
        # Calculate required bits
        n_calc = log(vref / vlsb_req) / log(2)
        
        # Round up
        n_req = ceil(n_calc)
        
        print("Required bits (n) = " + str(n_req))
        print("(Exact: " + str(round(n_calc, 4)) + ")")
        
        # Calculate actual SNR with n bits
        vlsb_act = vref / (2**n_req)
        vnq_act = vlsb_act / (12**0.5)
        
        if use_jit:
            snr_act = 10 * log10(vinrms**2 / (vnq_act**2 + vjit**2))
            print("With " + str(n_req) + " bits:")
            print("SNR = " + str(round(snr_act, 2)) + " dB")
        else:
            snr_act = 10 * log10(vinrms**2 / vnq_act**2)
            print("With " + str(n_req) + " bits:")
            print("SNR = " + str(round(snr_act, 2)) + " dB")
    
    else:
        print("Invalid choice.")
        
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

def sd_snr():
    print("Sigma-Delta SNR")
    print("=======================")
    n = int(input("n bits: "))
    Vin = float(input("Vin (V): "))
    osr = float(input("OSR: "))
    order = int(input("Ordem (1-3): "))

    if order not in [1, 2, 3]:
        print("Erro: Ordem inválida")
        return

    if order == 1:
        ganho = 30
        correcao = -5.17
    elif order == 2:
        ganho = 50
        correcao = -12.9
    else:
        ganho = 70
        correcao = -20.9

    snr = 6.02 * n + 1.76 + ganho * log10(osr) + correcao + 20 * log10(Vin)
    print("SNR calculado: {:.2f} dB".format(snr))
    
def sd_osr():
    print("Sigma-Delta OSR")
    print("=========================")
    order = int(input("Ordem (1-3): "))
    snr = float(input("SNR alvo (dB): "))
    n = int(input("Bits do quantizador: "))
    Vin = float(input("Vin (V): "))

    if order not in [1, 2, 3]:
        print("Erro: Ordem inválida")
        return

    if order == 1:
        ganho = 30
        correcao = -5.17
    elif order == 2:
        ganho = 50
        correcao = -12.9
    else:
        ganho = 70
        correcao = -20.9

    osr = 10 ** ((snr - 1.76 - 6.02 * n - correcao - 20 * log10(Vin)) / ganho)
    print("OSR necessário: {:.3f}".format(osr))

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
                inl_dnl_calc()
                
            elif choice == 3:
                print("SNR Tools")
                print("1. SNRMax Calculator") 
                print("2. SNR Calculator")
                snr_choice = int(input("Enter your choice (1 or 2): "))
                if snr_choice == 1:
                    snr_max_calc()
                elif snr_choice == 2:
                    snr_calc()
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
                
            elif choice == 6:
                print("Sigma-Delta Tools")
                print("1. Sigma-Delta SNR")
                print("2. Sigma-Delta OSR")
                sd_choice = int(input("Enter your choice (1-2): "))
                if sd_choice == 1:
                    sd_snr()
                elif sd_choice == 2:
                    sd_osr()
                else:
                    print("Invalid choice. Please try again.")
                
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid option (0-6).")
        
        input("\nPress Enter to return to main menu...")
        
main()
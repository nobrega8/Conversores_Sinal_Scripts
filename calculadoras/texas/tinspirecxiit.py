from math import *

def binary_to_decimal(binary_bits):
    return int(binary_bits, 2)

def calculate_vlsbr(vout_min, vout_max, num_bits):
    try:
        return (vout_max - vout_min)/(2**num_bits - 1)
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
        Dout_max = 2 ** n
    else:
        Vin_min = 0
        Vin_max = Vref
        Dout_max = 2 ** n - 1

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
            
def main():
    while True:
        print("\n===================================")
        print("      CONVERSORES DE SINAL")
        print("         NOBREGA 2025")
        print("==================================")
        print("1. INL/DNL Table Calculator")
        print("2. SNRMax Calculator")
        print("3. SNR Calculator")
        print("4. Dout Step Graph")
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
            elif choice == 4:
                dout_step_graph()
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid option (0-3).")
        
        input("\nPress Enter to return to main menu...")

main()
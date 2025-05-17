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

def main():
    """Main menu function"""
    while True:
        print("=======================")
        print("  SIGNAL CONVERTERS")
        print("       2025")
        print("=======================")
        print("1. INL/DNL Calculator")
        print("2. SNRMax Calculator")
        print("3. SNR Calculator")
        print("0. Exit")
        print("-----------------------")
        
        try:
            ch = int(input("Choice (0-3): "))
            
            if ch == 0:
                print("Exiting. Thanks!")
                break
            elif ch == 1:
                inl_dnl_calc()
            elif ch == 2:
                snr_max_calc()
            elif ch == 3:
                snr_calc()
            else:
                print("Invalid option.")
        except ValueError:
            print("Enter valid option (0-3).")
        
        input("Press Enter to continue...")

# Run program
main()

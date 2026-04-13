## Casio fx-CG50
## 2025 (c) Afonso Nobrega
## v3.0.0 - MicroPython 1.9.4

from math import log, log10, pi, ceil, floor

# --- log2 not guaranteed in uPy 1.9.4 ---
def log2(x):
    return log(x) / log(2)

# Constants
SNR_SLOPE  = 6.02   # dB per bit
SNR_OFFSET = 1.76   # dB
SQRT_2  = 2 ** 0.5
SQRT_12 = 12 ** 0.5

# -------------------------------------------
# Helpers
# -------------------------------------------

def bin2dec(b):
    return int(b, 2)

def bin_to_val(bin_str, vref, bits):
    n   = int(bin_str, 2)
    p   = vref / (2 ** bits)
    return -vref / 2 + n * p

def val_to_bin(val, vref, bits):
    steps = 2 ** bits
    delta = vref / steps
    code  = int((val + vref / 2) / delta)
    code  = max(0, min(code, steps - 1))
    result = ""
    temp   = code
    for _ in range(bits):
        result = str(temp % 2) + result
        temp   = temp // 2
    return result

def _input_float(prompt, default=None):
    """input() wrapper that returns a float; uses default on empty/error."""
    try:
        raw = input(prompt)
        if raw == "" and default is not None:
            return float(default)
        return float(raw)
    except (ValueError, TypeError):
        if default is not None:
            return float(default)
        raise

def _input_int(prompt, default=None):
    """input() wrapper that returns an int; uses default on empty/error."""
    try:
        raw = input(prompt)
        if raw == "" and default is not None:
            return int(default)
        return int(raw)
    except:
        if default is not None:
            return int(default)
        raise

# -------------------------------------------
# Core calculations
# -------------------------------------------

def calculate_vlsbr(vout_min, vout_max, num_bits):
    try:
        return (vout_max - vout_min) / (2 ** num_bits - 1)
    except:
        return 0

def calculate_vlsbi(vref, num_bits):
    try:
        return vref / (2 ** num_bits)
    except:
        return 0

def calculate_inl(vout, decimal_value, vlsbr, vout_min):
    try:
        inl = (vout - decimal_value * vlsbr - vout_min) / vlsbr
        return inl, True
    except:
        return 0, False

def calculate_dnl(vout, prev_vout, vlsbr):
    try:
        dnl = (vout - prev_vout) / vlsbr - 1
        return dnl, True
    except:
        return 0, False

def calculate_linearity(num_bits, inl_values):
    try:
        numeric_inl = []
        for inl in inl_values:
            try:
                if inl != "ERROR" and inl != "N/A":
                    numeric_inl.append(float(inl))
            except:
                continue
        if len(numeric_inl) == 0:
            return "N/A"
        inl_range = max(numeric_inl) - min(numeric_inl)
        if inl_range <= 0:
            return "N/A"
        linearity = num_bits - log2(inl_range)
        return round(linearity, 3)
    except:
        return "N/A"

# -------------------------------------------
# Menu functions
# -------------------------------------------

def inl_dnl_calc():
    print("INL/DNL Calculator")
    print("-----------------")
    try:
        n = _input_int("Bits (n): ")
        if n <= 0:
            print("Bad n, using 5")
            n = 5
    except:
        print("Bad n, using 5")
        n = 5

    try:
        vmin  = _input_float("Vout_min: ")
        vmax  = _input_float("Vout_max: ")
        vlsbr = calculate_vlsbr(vmin, vmax, n)
        print("VlsbR=" + str(round(vlsbr, 6)))
    except:
        print("Error.")
        return

    max_ent = 2 ** n
    print("Max entries: " + str(max_ent))
    try:
        num_ent = _input_int("# entries: ")
        if num_ent <= 0 or num_ent > max_ent:
            num_ent = max_ent
    except:
        num_ent = max_ent

    bits  = []
    vouts = []

    print("Enter row data:")
    for i in range(num_ent):
        print("Entry {}/{}:".format(i + 1, num_ent))
        valid = False
        while not valid:
            b = input(str(n) + " bits: ")
            if len(b) == n and all(c in "01" for c in b):
                valid = True
            else:
                print("Need " + str(n) + " bits (0/1)")
        try:
            v = _input_float("Vout: ")
        except:
            print("Bad, using 0.0")
            v = 0.0
        bits.append(b)
        vouts.append(v)

    print("--- RESULTS ---")
    print("No Bits Dec Vout INL DNL")

    inl_list = []
    dnl_list = ["N/A"]

    for i in range(num_ent):
        dec = bin2dec(bits[i])
        inl, ok = calculate_inl(vouts[i], dec, vlsbr, vmin)
        inl_list.append(str(round(inl, 4)) if ok else "Err")

    for i in range(1, num_ent):
        d_prev = bin2dec(bits[i - 1])
        d_curr = bin2dec(bits[i])
        if d_curr == d_prev + 1:
            dnl, ok = calculate_dnl(vouts[i], vouts[i - 1], vlsbr)
            dnl_list.append(str(round(dnl, 4)) if ok else "Err")
        else:
            dnl_list.append("N/A")

    for i in range(num_ent):
        dec = bin2dec(bits[i])
        print("{} {} {} {} {} {}".format(
            i + 1, bits[i], dec,
            round(vouts[i], 3),
            inl_list[i], dnl_list[i]))

    lin = calculate_linearity(n, inl_list)
    print("Linearity=" + str(lin) + " bits")
    print("n-log2(INLmax-INLmin)")


def snr_max_calc():
    print("SNR max calculator")
    print("==================")
    print("1. SNR max")
    print("2. n bits")
    ch = _input_int("Choice (1-2): ")

    if ch == 2:
        snr = _input_float("SNR max (dB): ")
        n   = (snr - SNR_OFFSET) / SNR_SLOPE
        print("n bits = " + str(int(ceil(n))))
    elif ch == 1:
        n   = _input_int("n bits: ")
        snr = SNR_SLOPE * n + SNR_OFFSET
        print("SNR max = " + str(snr) + " dB")
    else:
        print("Invalid option!")


def snr_calc():
    print("SNR Calculator")
    print("==============")
    print("1. SNR")
    print("2. n bits")
    ch = _input_int("Choice (1-2): ")

    vin  = _input_float("Vin (V): ")
    vref = _input_float("Vref (V): ")
    fin  = _input_float("Fin (MHz): ")
    djit = _input_float("Jitter (ps): ")

    fin_hz   = fin  * 1e6
    djit_sec = djit * 1e-12
    vinrms   = vin  / SQRT_2
    print("Vin RMS=" + str(round(vinrms, 4)) + " V")

    use_jit = (djit_sec != 0) and (fin_hz != 0)

    if ch == 1:
        n    = _input_int("Bits (n): ")
        vlsb = vref / (2 ** n)
        print("Vlsb=" + str(round(vlsb, 4)) + " V")
        vnqrms = vlsb / SQRT_12
        print("VNQ RMS=" + str(round(vnqrms, 4)) + " V")

        if use_jit:
            vjit = vinrms * 2 * pi * fin_hz * djit_sec
            print("VJit RMS=" + str(round(vjit, 4)) + " V")
            snr  = 10 * log10(vinrms ** 2 / (vnqrms ** 2 + vjit ** 2))
            print("SNR=" + str(round(snr, 2)) + " dB (q+jit)")
        else:
            snr = 10 * log10(vinrms ** 2 / vnqrms ** 2)
            print("SNR=" + str(round(snr, 2)) + " dB (quant)")

    elif ch == 2:
        snr     = _input_float("SNR (dB): ")
        snr_lin = 10 ** (snr / 10)

        if use_jit:
            vjit    = vinrms * 2 * pi * fin_hz * djit_sec
            print("VJit RMS=" + str(round(vjit, 4)) + " V")
            jit_snr = 10 * log10(vinrms ** 2 / vjit ** 2)
            print("Jit SNR lim=" + str(round(jit_snr, 2)) + " dB")
            if jit_snr < snr:
                print("WARN: SNR unachievable")
                print("Max=" + str(round(jit_snr, 2)) + " dB")
                return
            vnq_max = (vinrms ** 2 / snr_lin - vjit ** 2) ** 0.5
        else:
            vnq_max = vinrms / (snr_lin ** 0.5)

        print("Max VNQ=" + str(round(vnq_max, 4)) + " V")
        vlsb_req = vnq_max * SQRT_12
        n_calc   = log(vref / vlsb_req) / log(2)
        n_req    = int(ceil(n_calc))
        print("n bits=" + str(n_req))
        print("(Exact: " + str(round(n_calc, 4)) + ")")

        vlsb_act = vref / (2 ** n_req)
        vnq_act  = vlsb_act / SQRT_12
        if use_jit:
            snr_act = 10 * log10(vinrms ** 2 / (vnq_act ** 2 + vjit ** 2))
        else:
            snr_act = 10 * log10(vinrms ** 2 / vnq_act ** 2)
        print("With {} bits:".format(n_req))
        print("SNR=" + str(round(snr_act, 2)) + " dB")
    else:
        print("Invalid choice.")


def dout_step_graph():
    print("Dout Step Table")
    print("===============")
    n    = _input_int("n bits: ")
    Vref = _input_float("Vref (V): ")
    print("1-Symmetric [-Vref/2,+Vref/2]")
    print("2-Classic   [0, Vref]")
    modo = input("Mode [1/2]: ")

    Vlsb = Vref / (2 ** n)

    if modo == "1":
        Vin_min = -Vref / 2
        Vin_max =  Vref / 2
    else:
        Vin_min = 0
        Vin_max = Vref

    total  = 2 * (2 ** n)
    step   = (Vin_max - Vin_min) / (total - 1)

    print("{:>6} | {:>6}".format("Vin", "Dout"))
    print("-" * 15)

    for i in range(total):
        Vin = Vin_min + i * step
        if modo == "1":
            Dout = round(Vin / Vlsb) + 2 ** (n - 1)
            Dout = max(0, min(Dout, 2 ** n))
        else:
            Dout = int(floor(Vin / Vlsb))
            Dout = max(0, min(Dout, 2 ** n - 1))
        print("{:6.3f} | {:6}".format(Vin, Dout))


def clock_freq_calculator():
    print("Clock Freq Calc")
    print("===============")
    print("1. Solve for n bits")
    print("2. Solve for f")
    choice = _input_int("Choose (1-2): ")

    if choice == 1:
        f  = _input_float("f (MHz): ")
        pf = _input_float("Power f Hz [50]: ", 50)
        n  = int(ceil(log2(f * 1e6 / pf)))
        print("n bits = " + str(n))
    elif choice == 2:
        n  = _input_int("n bits: ")
        pf = _input_float("Power f Hz [50]: ", 50)
        f  = (2 ** n / (1 / pf)) / 1e6
        print("f = " + str(f) + " MHz")
    else:
        print("Invalid option.")


def calculate_vlsb():
    print("Vlsb Calculator")
    print("===============")
    print("1. Ideal")
    print("2. Real")
    choice = _input_int("(1 or 2): ")
    if choice == 1:
        n    = _input_int("n bits: ")
        vref = _input_float("Vref (V): ")
        print("Vlsb ideal=" + str(round(calculate_vlsbi(vref, n), 4)))
    elif choice == 2:
        vmin = _input_float("Vout_min: ")
        vmax = _input_float("Vout_max: ")
        n    = _input_int("n bits: ")
        print("Vlsb real=" + str(round(calculate_vlsbr(vmin, vmax, n), 4)))
    else:
        print("Invalid choice.")


def pipeline_dout():
    print("Pipeline Simulator")
    print("==================")
    stages = _input_int("Stages: ")
    bps    = _input_int("Bits/stage: ")
    vref   = _input_float("Vref: ")
    vin    = _input_float("Vin: ")

    residuos   = [vin]
    douts      = []
    valores_dac = []

    print("--- Per stage ---")
    for i in range(stages):
        vin_s   = residuos[-1]
        dout_b  = val_to_bin(vin_s, vref, bps)
        douts.append(dout_b)
        nivel   = int(dout_b, 2)
        passo   = vref / (2 ** bps)
        dac_val = -vref / 2 + (nivel + 0.5) * passo
        valores_dac.append(dac_val)

        if i < stages - 1:
            res = 2 * (vin_s - dac_val)
            residuos.append(res)

        print("Stage {}:".format(i + 1))
        print(" Vin={:.4f}V".format(vin_s))
        print(" Dout={} ({})".format(dout_b, nivel))
        print(" DAC={:.4f}V".format(dac_val))
        if i < stages - 1:
            print(" VRes={:.4f}V".format(res))

    bits_fin = douts[0]
    for i in range(1, stages):
        bits_fin += douts[i][0]

    dec_fin   = int(bits_fin, 2)
    nb_tot    = len(bits_fin)
    delta     = vref / (2 ** nb_tot)
    v_est     = -vref / 2 + dec_fin * delta

    print("=== Result ===")
    print("Bits: " + bits_fin)
    print("Dec:  " + str(dec_fin))
    print("V:    {:.4f}V".format(v_est))


def pipeline_snr():
    print("Pipeline SNR Calc")
    print("=================")
    snr_t  = _input_float("Target SNR (dB): ")
    amp    = _input_float("Signal amplitude (V): ")
    vref   = _input_float("Vref (V): ")
    v_lo   = _input_float("Vin min [-Vref/2]: ", -vref / 2)
    v_hi   = _input_float("Vin max [+Vref/2]: ",  vref / 2)
    bps    = _input_int("Bits/stage [2]: ", 2)
    breds  = _input_int("Redundant bits/stage [1]: ", 1)

    if amp > v_hi or amp < v_lo:
        print("Amplitude out of range!")
        return

    penalty       = 20 * log10(amp / (vref / 2))
    snr_ideal_req = snr_t - penalty
    N             = int(ceil((snr_ideal_req - SNR_OFFSET) / SNR_SLOPE))

    bits_remaining = N - bps
    if bits_remaining <= 0:
        num_stages = 1
    else:
        bps_useful = bps - breds
        if bps_useful <= 0:
            print("Err: useful bits/stage<=0")
            return
        num_stages = 1 + int(ceil(bits_remaining / bps_useful))

    print("=== Results ===")
    print("Min resolution: {} bits".format(N))
    print("Min stages: {}".format(num_stages))
    print("SNR penalty: {:.2f} dB".format(penalty))


def sd_snr():
    print("Sigma-Delta SNR")
    print("===============")
    n     = _input_int("n bits: ")
    Vin   = _input_float("Vin (V): ")
    osr   = _input_float("OSR: ")
    order = _input_int("Order (1-3): ")

    if order == 1:
        gain, corr = 30, -5.17
    elif order == 2:
        gain, corr = 50, -12.9
    elif order == 3:
        gain, corr = 70, -20.9
    else:
        print("Invalid order")
        return

    snr = (SNR_SLOPE * n + SNR_OFFSET
           + gain * log10(osr)
           + corr
           + 20 * log10(Vin))
    print("SNR={:.2f} dB".format(snr))


def sd_osr():
    print("Sigma-Delta OSR")
    print("===============")
    order = _input_int("Order (1-3): ")
    snr   = _input_float("Target SNR (dB): ")
    n     = _input_int("Quantizer bits: ")
    Vin   = _input_float("Vin (V): ")

    if order == 1:
        gain, corr = 30, -5.17
    elif order == 2:
        gain, corr = 50, -12.9
    elif order == 3:
        gain, corr = 70, -20.9
    else:
        print("Invalid order")
        return

    osr = 10 ** ((snr - SNR_OFFSET - SNR_SLOPE * n
                  - corr - 20 * log10(Vin)) / gain)
    print("OSR={:.3f}".format(osr))


# -------------------------------------------
# Main menu
# -------------------------------------------

def main():
    while True:
        print()
        print("=======================")
        print("   SIGNAL CONVERTERS")
        print("     NOBREGA 2025")
        print("=======================")
        print("1. Vlsb Calc")
        print("2. INL/DNL Table")
        print("3. SNR Tools")
        print("4. Pipeline Tools")
        print("5. Clock Freq Calc")
        print("6. Sigma-Delta Tools")
        print("0. Exit")
        print("-----------------------")

        try:
            choice = _input_int("Choice (0-6): ")
        except:
            print("Enter a number 0-6.")
            continue

        if choice == 0:
            print("Exiting. Obrigado!")
            break

        elif choice == 1:
            calculate_vlsb()

        elif choice == 2:
            inl_dnl_calc()

        elif choice == 3:
            print("SNR Tools")
            print("1. SNR Max")
            print("2. SNR Calc")
            try:
                sc = _input_int("Choice (1-2): ")
                if sc == 1:
                    snr_max_calc()
                elif sc == 2:
                    snr_calc()
                else:
                    print("Invalid.")
            except:
                print("Invalid.")

        elif choice == 4:
            print("Pipeline Tools")
            print("1. Dout Step Table")
            print("2. Pipeline SNR")
            print("3. Pipeline Dout")
            try:
                pc = _input_int("Choice (1-3): ")
                if pc == 1:
                    dout_step_graph()
                elif pc == 2:
                    pipeline_snr()
                elif pc == 3:
                    pipeline_dout()
                else:
                    print("Invalid.")
            except:
                print("Invalid.")

        elif choice == 5:
            clock_freq_calculator()

        elif choice == 6:
            print("Sigma-Delta Tools")
            print("1. SD SNR")
            print("2. SD OSR")
            try:
                sd = _input_int("Choice (1-2): ")
                if sd == 1:
                    sd_snr()
                elif sd == 2:
                    sd_osr()
                else:
                    print("Invalid.")
            except:
                print("Invalid.")

        else:
            print("Invalid option.")

        input("\nEnter to continue...")


main()

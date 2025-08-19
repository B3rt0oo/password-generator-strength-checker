# Password Generator and Strength Checker with Plots and Heatmap
# Generates random passwords
# Calculates entropy
# Estimates expected crack times
# Shows strength category
# Displays strength gauge, crack times plot, and heatmap of entropy vs length & charset

import random
import math
import matplotlib.pyplot as plt
import numpy as np

# Character sets
LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

# --------------------------
# Core Functions
# --------------------------
def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    charset = LOWERCASE
    if use_upper: charset += UPPERCASE
    if use_digits: charset += DIGITS
    if use_symbols: charset += SYMBOLS
    if not charset:
        raise ValueError("No characters selected for password generation.")
    return ''.join(random.choice(charset) for _ in range(length))

def password_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(c in SYMBOLS for c in password): charset_size += len(SYMBOLS)
    return len(password) * math.log2(charset_size)

def strength_category(entropy):
    if entropy < 28: return "Very Weak"
    elif entropy < 36: return "Weak"
    elif entropy < 60: return "Reasonable"
    elif entropy < 128: return "Strong"
    else: return "Very Strong"

def crack_time(entropy, guesses_per_second):
    seconds = (2 ** entropy) / (2 * guesses_per_second)
    return seconds

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    elif seconds < 3.154e+12:
        return f"{seconds/31536000:.2f} years"
    else:
        return f"{seconds/3.154e+12:.2f} millennia"

# --------------------------
# Plot Functions
# --------------------------
def plot_strength_gauge(entropy):
    thresholds = [28, 36, 60, 128]
    colors = ['red', 'orange', 'yellow', 'green', 'blue']
    
    fig, ax = plt.subplots(figsize=(6,1.5))
    ax.barh(0, thresholds[0], color=colors[0])
    ax.barh(0, thresholds[1]-thresholds[0], left=thresholds[0], color=colors[1])
    ax.barh(0, thresholds[2]-thresholds[1], left=thresholds[1], color=colors[2])
    ax.barh(0, thresholds[3]-thresholds[2], left=thresholds[2], color=colors[3])
    ax.barh(0, entropy-thresholds[3], left=thresholds[3], color=colors[4] if entropy>thresholds[3] else 'gray')
    
    ax.plot(entropy, 0, 'ko', markersize=12)
    ax.set_yticks([])
    ax.set_xlabel('Entropy (bits)')
    ax.set_title('Password Strength Gauge')
    plt.show()

def plot_crack_times(entropy):
    attacks = {"Online (1e3/s)": 1e3, "Offline (1e9/s)": 1e9, "GPU Rig (1e12/s)": 1e12}
    times = [crack_time(entropy, speed) for speed in attacks.values()]
    
    plt.figure(figsize=(6,4))
    plt.bar(attacks.keys(), times, color=['red','orange','green'])
    plt.yscale('log')
    plt.ylabel('Time to Crack (seconds, log scale)')
    plt.title('Estimated Crack Times')
    plt.show()

def plot_entropy_heatmap():
    # Vary length and charset options
    lengths = np.arange(4, 21, 1)  # 4 to 20 characters
    charsets = [LOWERCASE, LOWERCASE+UPPERCASE, LOWERCASE+UPPERCASE+DIGITS, LOWERCASE+UPPERCASE+DIGITS+SYMBOLS]
    labels = ['Lowercase', 'Lower+Upper', 'Letters+Digits', 'Letters+Digits+Symbols']

    heatmap = np.zeros((len(charsets), len(lengths)))
    
    for i, charset in enumerate(charsets):
        charset_size = len(charset)
        for j, length in enumerate(lengths):
            heatmap[i,j] = length * math.log2(charset_size)
    
    plt.figure(figsize=(8,4))
    plt.imshow(heatmap, aspect='auto', cmap='viridis', origin='lower')
    plt.colorbar(label='Entropy (bits)')
    plt.xticks(np.arange(len(lengths)), lengths)
    plt.yticks(np.arange(len(charsets)), labels)
    plt.xlabel('Password Length')
    plt.ylabel('Charset Complexity')
    plt.title('Password Entropy Heatmap')
    plt.show()

# --------------------------
# Main Program
# --------------------------
if __name__ == "__main__":
    print("=== Password Generator & Strength Checker ===")
    
    pw = generate_password(length=16, use_upper=True, use_digits=True, use_symbols=True)
    print(f"\nGenerated Password: {pw}")
    
    entropy = password_entropy(pw)
    print(f"Entropy: {entropy:.2f} bits")
    
    strength = strength_category(entropy)
    print(f"Strength: {strength}")
    
    print("\nEstimated Crack Times:")
    attacks = {"Online (1e3/s)": 1e3, "Offline (1e9/s)": 1e9, "GPU Rig (1e12/s)": 1e12}
    for attack, speed in attacks.items():
        print(f" - {attack}: {format_time(crack_time(entropy, speed))}")
    
    # Plots
    plot_strength_gauge(entropy)
    plot_crack_times(entropy)
    plot_entropy_heatmap()

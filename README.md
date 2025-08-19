# Password Generator & Strength Checker

A Python tool that generates strong passwords, calculates entropy, estimates expected crack times, and visualizes password strength with interactive plots and a heatmap.

---

## Features

- **Random Password Generator**  
  - Customizable length  
  - Options to include uppercase letters, digits, and symbols  

- **Entropy Calculation**  
  - Measures the randomness of a password in bits  

- **Password Strength Classification**  
  - Very Weak → Very Strong based on entropy  

- **Estimated Crack Times**  
  - Online attack (~1,000 guesses/sec)  
  - Offline attack (~1 billion guesses/sec)  
  - GPU/cluster attack (~1 trillion guesses/sec)  

- **Visualizations**  
  - Strength Gauge (color-coded)  
  - Crack Times Bar Chart (log scale)  
  - Entropy Heatmap showing effect of password length and charset diversity  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/B3rt0oo/password-strength-visualizer.git
cd password-strength-visualizer

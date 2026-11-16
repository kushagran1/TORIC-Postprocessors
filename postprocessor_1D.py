import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

file_path = "toricncdf_ncdump"

def extract_array(text, var_name):
    pattern = r"\b" + re.escape(var_name) + r"\b\s*=\s*(.*?);"
    match = re.search(pattern, text, re.S)

    if not match:
        print(f"{var_name} not found")
        return None

    data_str = match.group(1)
    numbers = re.findall(r"[-+]?\d*\.?\d+(?:[Ee][+-]?\d+)?", data_str)

    return np.array(numbers, dtype=float)

def extract_scalar(text, var_name):
    pattern = var_name + r"\s*=\s*([-+]?\d*\.?\d+(?:[Ee][+-]?\d+)?)"
    match = re.search(pattern, text)

    if not match:
        print(f"{var_name} not found")
        return None

    return float(match.group(1))

with open(file_path, "r") as f:
    text = f.read()


Npw = int(extract_scalar(text, "PsiPwdDim"))  
Nspec = int(extract_scalar(text, "SpecDim"))  
NpsiDim = int(extract_scalar(text, "NpsiDim")) 
NpsiCurDim = int(extract_scalar(text, "NpsiCurDim")) 

x_pw = extract_array(text, "Pw_abscissa")
x_poy = extract_array(text, "PoyFlx_abscissa")
x_curr = extract_array(text, "CurrDens_abscissa")

Spec_volume = extract_array(text, "Spec_volume")
PwE = extract_array(text, "PwE")
PwEIBW = extract_array(text, "PwEIBW")  

PwIF = extract_array(text,"PwIF") 
PwIH= extract_array(text,"PwIH")

PwIF = PwIF.reshape(Npw, Nspec)
PwIH = PwIH.reshape(Npw, Nspec)

PwETot = PwE + PwEIBW  
PwITot = PwIF + PwIH   

PwNet  = PwETot + PwITot[:,0] + PwITot[:,1] + PwITot[:,2] 

PoyFlx = extract_array(text,"PoyFlx")

CurDensFW = extract_array(text,"CurDensFW")
CurDensFW0 = extract_array(text,"CurDensFW0")
CurDensIBW = extract_array(text,"CurDensIBW")
CurDensIBW0 = extract_array(text,"CurDensIBW0")

plt.figure()
plt.plot(x_pw,PwE,'r--',linewidth = 1,label = "$P_e^{FW}$")
plt.plot(x_pw,PwEIBW,'y-.',linewidth = 1, label = "$P_e^{IBW}$")
plt.plot(x_pw,PwETot,'b--',linewidth = 1, label = "$P_e^{Tot.}$")
plt.title("Power Absorbed by Electrons",color='k',fontweight='bold',fontsize='14')
plt.xlabel("$\psi\ (normalized)$")
plt.ylabel("$P_e\ (W/cm³/MW_{abs})$")
plt.legend()
plt.grid(visible = 'True', which = 'both')
plt.savefig("PwEle.pdf")
plt.close()

plt.figure()
plt.plot(x_pw,PwIF[:,0],'r--',linewidth = 1,label = "$P_i^{Funda.}$")
plt.plot(x_pw,PwIH[:,0],'y-.',linewidth = 1, label = "$P_i^{Harm.}$")
plt.plot(x_pw,PwITot[:,0],'b--',linewidth = 1, label = "$P_i^{Tot.}$")
plt.title("Power Absorbed by Ion-1",color='k',fontweight='bold',fontsize='14')
plt.xlabel("$\psi\ (normalized)$")
plt.ylabel("$P_i\ (W/cm³/MW_{abs})$")
plt.legend()
plt.grid(visible = 'True', which = 'both')
plt.savefig("PwIon1.pdf")
plt.close()

plt.figure()
plt.plot(x_pw,PwIF[:,1],'r--',linewidth = 1,label = "$P_i^{Funda.}$")
plt.plot(x_pw,PwIH[:,1],'y-.',linewidth = 1, label = "$P_i^{Harm.}$")
plt.plot(x_pw,PwITot[:,1],'b--',linewidth = 1, label = "$P_i^{Tot.}$")
plt.title("Power Absorbed by Ion-2",color='k',fontweight='bold',fontsize='14')
plt.xlabel("$\psi\ (normalized)$")
plt.ylabel("$P_i\ (W/cm³/MW_{abs})$")
plt.legend()
plt.grid(visible = 'True', which = 'both')
plt.savefig("PwIon2.pdf")
plt.close()

plt.figure()
plt.plot(x_pw,PwIF[:,2],'r--',linewidth = 1,label = "$P_i^{Funda.}$")
plt.plot(x_pw,PwIH[:,2],'y-.',linewidth = 1, label = "$P_i^{Harm.}$")
plt.plot(x_pw,PwITot[:,2],'b--',linewidth = 1, label = "$P_i^{Tot.}$")
plt.title("Power Absorbed by Ion-3",color='k',fontweight='bold',fontsize='14')
plt.xlabel("$\psi\ (normalized)$")
plt.ylabel("$P_i\ (W/cm³/MW_{abs})$")
plt.legend()
plt.grid(visible = 'True', which = 'both')
plt.savefig("PwIon3.pdf")
plt.close()

plt.figure()
plt.plot(x_pw,PwETot,'r-.',linewidth = 1, label = "$P_e^{Tot.}$")
plt.plot(x_pw,PwITot[:,0],'y-.',linewidth = 1, label = "$P_{ion1}^{Tot.}$")
plt.plot(x_pw,PwITot[:,1],'b-.',linewidth = 1, label = "$P_{ion2}^{Tot.}$")
plt.plot(x_pw,PwITot[:,2],'g-.',linewidth = 1, label = "$P_{ion3}^{Tot.}$")
plt.plot(x_pw,PwNet,'k--',linewidth = 1,label = "$P_{Net}$")
plt.title("Net Power Absorbed",color='k',fontweight='bold',fontsize='14')
plt.xlabel("$\psi\ (normalized)$")
plt.ylabel("$P_{Net}\ (W/cm³/MW_{abs})$")
plt.legend()
plt.grid(visible = 'True', which = 'both')
plt.savefig("PwNet.pdf")
plt.close()
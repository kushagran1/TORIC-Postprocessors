import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

file_path = "toricncdf_ncdump"

def extract_array(text, var_name):
    pattern = var_name + r"\s*=\s*(.*?);"
    match = re.search(pattern, text, re.S)

    if not match:
        print(f"{var_name} not found")
        return None

    data_str = match.group(1)
    numbers = re.findall(r"[-+]?\d*\.?\d+(?:[Ee][+-]?\d+)?", data_str)

    return np.array(numbers, dtype=float)

with open(file_path, "r") as f:
    text = f.read()

Nth = extract_array(text, "ThetaDim")   
Npsi = extract_array(text, "PsiEfDim")   
NpsiDim = extract_array(text, "NpsiDim") 
Nspec = extract_array(text, "SpecDim")   
Nth = int(Nth[0]);
Npsi = int(Npsi[0]);
NpsiDim = int(NpsiDim[0]);
Nspec = int(Nspec[0]);
    

Xvessel = extract_array(text, "Xvessel")
Zvessel = extract_array(text, "Zvessel")
Xsurf = extract_array(text, "XSurfPlasma")
Zsurf = extract_array(text, "ZSurfPlasma")
X = extract_array(text, "Xplasma")
Z = extract_array(text, "Zplasma")
ReEplus = extract_array(text, "Re2Eplus")
ImEplus = extract_array(text, "Im2Eplus")
ReEminus = extract_array(text, "Re2Eminus")
ImEminus = extract_array(text, "Im2Eminus")
ReEzeta = extract_array(text, "Re2Ezeta")
ImEzeta = extract_array(text, "Im2Ezeta")
TDPwE = extract_array(text, "TDPwE")
TDPwEIBW = extract_array(text, "TDPwEIBW")
TDPwIF = extract_array(text, "TDPwIF")
TdPwIH = extract_array(text, "TdPwIH")

if Xvessel is None or Zvessel is None:
    raise ValueError("Vessel data not found in file")
if Xsurf is None or Zsurf is None:
    raise ValueError("Plasma Surface data not found in file")

X = X.reshape(Nth, Npsi)
X = np.append(X,[X[0,:]],axis=0)
Z = Z.reshape(Nth, Npsi)
Z = np.append(Z,[Z[0,:]],axis=0)

ReEplus = ReEplus.reshape(Nth, Npsi)
ReEplus = np.append(ReEplus,[ReEplus[0,:]],axis=0)
ImEplus = ImEplus.reshape(Nth, Npsi)
ImEplus = np.append(ImEplus,[ImEplus[0,:]],axis=0)
Eplus_mag = np.sqrt(ReEplus**2 + ImEplus**2)

ReEminus = ReEminus.reshape(Nth, Npsi)
ReEminus = np.append(ReEminus,[ReEminus[0,:]],axis=0)
ImEminus = ImEminus.reshape(Nth, Npsi)
ImEminus = np.append(ImEminus,[ImEminus[0,:]],axis=0)
Eminus_mag = np.sqrt(ReEminus**2 + ImEminus**2)

ReEzeta = ReEzeta.reshape(Nth, Npsi)
ReEzeta = np.append(ReEzeta,[ReEzeta[0,:]],axis =0)
ImEzeta = ImEzeta.reshape(Nth, Npsi)
ImEzeta = np.append(ImEzeta,[ImEzeta[0,:]],axis =0)
Ezeta_mag = np.sqrt(ReEzeta**2 + ImEzeta**2)

TDPwE = TDPwE.reshape(Nth, Npsi)
TDPwE = np.append(TDPwE,[TDPwE[0,:]],axis =0)
TDPwEIBW = TDPwEIBW.reshape(Nth, Npsi)
TDPwEIBW = np.append(TDPwEIBW,[TDPwEIBW[0,:]],axis =0)
TDPwIF = TDPwIF.reshape(Nth, Npsi, Nspec)
TDPwIF = np.append(TDPwIF,[TDPwIF[0,:]],axis =0)
TdPwIH = TdPwIH.reshape(Nth, Npsi, Nspec)
TdPwIH = np.append(TdPwIH,[TdPwIH[0,:]],axis =0)

Xvessel = np.append(Xvessel, Xvessel[0])
Zvessel = np.append(Zvessel, Zvessel[0])

Xsurf = np.append(Xsurf, Xsurf[0])
Zsurf = np.append(Zsurf, Zsurf[0])

clevels = 25

fig, ax = plt.subplots(3, 3, figsize=(15, 8), sharex=True, sharey=True)
ax = ax.flatten()

im0 = ax[0].contourf(X, Z, ReEplus, cmap='jet', levels = clevels, linewidths=0.2)
ax[0].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[0].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[0].set_title("Re E+(R,Z)")
fig.colorbar(im0, ax=ax[0], label="$V/m/MW_{abs}$")


im1 = ax[1].contourf(X, Z, ImEplus, cmap='jet', levels = clevels, linewidths=0.2)
ax[1].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[1].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[1].set_title("Im E+(R,Z)")
fig.colorbar(im1, ax=ax[1], label="$V/m/MW_{abs}$")


im2 = ax[2].contourf(X, Z, Eplus_mag, cmap='jet', levels = clevels, linewidths=0.2)
ax[2].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[2].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[2].set_title("|E+|(R,Z)")
fig.colorbar(im2, ax=ax[2], label="$V/m/MW_{abs}$")


im0 = ax[3].contourf(X, Z, ReEminus, cmap='jet', levels = clevels, linewidths=0.2)
ax[3].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[3].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[3].set_title("Re E-(R,Z)")
fig.colorbar(im0, ax=ax[3], label="$V/m/MW_{abs}$")


im1 = ax[4].contourf(X, Z, ImEminus, cmap='jet', levels = clevels, linewidths=0.2)
ax[4].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[4].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[4].set_title("Im E-(R,Z)")
fig.colorbar(im1, ax=ax[4], label="$V/m/MW_{abs}$")


im2 = ax[5].contourf(X, Z, Eminus_mag, cmap='jet', levels = clevels, linewidths=0.2)
ax[5].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[5].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[5].set_title("|E-|(R,Z)")
fig.colorbar(im2, ax=ax[5], label="$V/m/MW_{abs}$")


im0 = ax[6].contourf(X, Z, ReEzeta, cmap='jet', levels = clevels, linewidths=0.2)
ax[6].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[6].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[6].set_title("Re Eζ(R,Z)")
fig.colorbar(im0, ax=ax[6], label="$V/m/MW_{abs}$")


im1 = ax[7].contourf(X, Z, ImEzeta, cmap='jet', levels = clevels, linewidths=0.2)
ax[7].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[7].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[7].set_title("Im Eζ(R,Z)")
fig.colorbar(im1, ax=ax[7], label="$V/m/MW_{abs}$")


im2 = ax[8].contourf(X, Z, Ezeta_mag, cmap='jet', levels = clevels, linewidths=0.2)
ax[8].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[8].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[8].set_title("|Eζ|(R,Z)")
fig.colorbar(im2, ax=ax[8], label="$V/m/MW_{abs}$")

# ================= common formatting =================
for a in ax:
    a.set_xlabel("R (cm)")
    a.set_ylabel("Z (cm)")
    a.set_aspect('equal')
    a.grid()
    a.minorticks_on()

plt.tight_layout()
plt.savefig('2DE-Fields.pdf', dpi=300, bbox_inches='tight')
plt.close() 


fig, ax = plt.subplots(2, 4, figsize=(15, 8), sharex=True, sharey=True)
ax = ax.flatten()

im0 = ax[0].contourf(X, Z, TDPwE, cmap='jet', levels = clevels, linewidths=0.2)
ax[0].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[0].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[0].set_title("2D Power absorbed by electron via FW(R,Z)")
fig.colorbar(im0, ax=ax[0], label="$W/cm^3/MW_{abs}$")

im4 = ax[4].contourf(X, Z, TDPwEIBW, cmap='jet', levels = clevels, linewidths=0.2)
ax[4].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[4].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[4].set_title("2D Power abs by electron via IBW(R,Z)")
fig.colorbar(im4, ax=ax[4], label="$W/cm^3/MW_{abs}$")


im1 = ax[1].contourf(X, Z, TDPwIF[:,:,0], cmap='jet', levels = clevels, linewidths=0.2)
ax[1].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[1].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[1].set_title("2D Power absorbed by ion-1 at funda(R,Z)")
fig.colorbar(im1, ax=ax[1], label="$W/cm^3/MW_{abs}$")


im5 = ax[5].contourf(X, Z, TdPwIH[:,:,0], cmap = 'jet', levels = clevels, linewidths=0.2)
ax[5].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[5].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[5].set_title("2D Power absorbed by ion-1 at harmonic(R,Z)")
fig.colorbar(im5, ax=ax[5], label="$W/cm^3/MW_{abs}$")


im2 = ax[2].contourf(X, Z, TDPwIF[:,:,1], cmap='jet', levels = clevels, linewidths=0.2)
ax[2].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[2].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[2].set_title("2D Power absorbed by ion-2 funda(R,Z)")
fig.colorbar(im2, ax=ax[2], label="$W/cm^3/MW_{abs}$")


im6 = ax[6].contourf(X, Z, TdPwIH[:,:,1], cmap='jet', levels = clevels, linewidths=0.2)
ax[6].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[6].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[6].set_title("2D Power absorbed by iont-2 at harmonic(R,Z)")
fig.colorbar(im6, ax=ax[6], label="$W/cm^3/MW_{abs}$")


im3 = ax[3].contourf(X, Z, TDPwIF[:,:,2], cmap = 'jet', levels = clevels, linewidths=0.2)
ax[3].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[3].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[3].set_title("2D Power absorbed by ion-3 at harmonic(R,Z)")
fig.colorbar(im3, ax=ax[3], label="$W/cm^3/MW_{abs}$")


im7 = ax[7].contourf(X, Z, TdPwIH[:,:,2], cmap='jet', levels = clevels, linewidths=0.2)
ax[7].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[7].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[7].set_title("2D Power absorbed by ion-3 at harmonic(R,Z)")
fig.colorbar(im7, ax=ax[7], label="$W/cm^3/MW_{abs}$")


for a in ax:
    a.set_xlabel("R (cm)")
    a.set_ylabel("Z (cm)")
    a.set_aspect('equal')
    a.grid()
    a.minorticks_on()

plt.tight_layout()
plt.savefig('2DPowerProfiles.pdf', dpi=300, bbox_inches='tight')
plt.close() 
 


fig, ax = plt.subplots(1, 2, figsize=(15, 8), sharex=True, sharey=True)

im0 = ax[0].contourf(X, Z, TDPwIF[:,:,0], cmap='jet', levels = clevels, linewidths=0.2)
ax[0].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[0].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[0].set_title("2D Power absorbed by ion-1 at funda(R,Z)")
fig.colorbar(im0, ax=ax[0], label="$W/cm^3/MW_{abs}$")


im1 = ax[1].contourf(X, Z, TdPwIH[:,:,0], cmap = 'jet', levels = clevels, linewidths=0.2)
ax[1].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[1].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[1].set_title("2D Power absorbed by ion-1 at harmonic(R,Z)")
fig.colorbar(im1, ax=ax[1], label="$W/cm^3/MW_{abs}$")


for a in ax:
    a.set_xlabel("R (cm)")
    a.set_ylabel("Z (cm)")
    a.set_aspect('equal')
    a.grid()
    a.minorticks_on()

plt.tight_layout()
plt.savefig('2DPowProfile_ion1.pdf',dpi = 300,  bbox_inches='tight')
plt.close()

fig, ax = plt.subplots(1, 2, figsize=(15, 8), sharex=True, sharey=True)

im0 = ax[0].contourf(X, Z, TDPwIF[:,:,1], cmap='jet', levels = clevels, linewidths=0.2)
ax[0].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[0].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[0].set_title("2D Power absorbed by ion-2 at funda(R,Z)")
fig.colorbar(im0, ax=ax[0], label="$W/cm^3/MW_{abs}$")


im1 = ax[1].contourf(X, Z, TdPwIH[:,:,1], cmap = 'jet', levels = clevels, linewidths=0.2)
ax[1].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[1].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[1].set_title("2D Power absorbed by ion-2 at harmonic(R,Z)")
fig.colorbar(im1, ax=ax[1], label="$W/cm^3/MW_{abs}$")


for a in ax:
    a.set_xlabel("R (cm)")
    a.set_ylabel("Z (cm)")
    a.set_aspect('equal')
    a.grid()
    a.minorticks_on()

plt.tight_layout()
plt.savefig('2DPowProfile_ion2.pdf',dpi = 300,  bbox_inches='tight')
plt.close()

fig, ax = plt.subplots(1, 2, figsize=(15, 8), sharex=True, sharey=True)

im0 = ax[0].contourf(X, Z, TDPwIF[:,:,2], cmap='jet', levels = clevels, linewidths=0.2)
ax[0].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[0].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[0].set_title("2D Power absorbed by ion-3 at funda(R,Z)")
fig.colorbar(im0, ax=ax[0], label="$W/cm^3/MW_{abs}$")

im1 = ax[1].contourf(X, Z, TdPwIH[:,:,2], cmap = 'jet', levels = clevels, linewidths=0.2)
ax[1].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[1].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[1].set_title("2D Power absorbed by ion-3 at harmonic(R,Z)")
fig.colorbar(im1, ax=ax[1], label="$W/cm^3/MW_{abs}$")

for a in ax:
    a.set_xlabel("R (cm)")
    a.set_ylabel("Z (cm)")
    a.set_aspect('equal')
    a.grid()
    a.minorticks_on()

plt.tight_layout()
plt.savefig('2DPowProfile_ion3.pdf',dpi = 300,  bbox_inches='tight')
plt.close()

fig, ax = plt.subplots(1, 2, figsize=(15, 8), sharex=True, sharey=True)

im0 = ax[0].contourf(X, Z, TDPwE, cmap='jet', levels = clevels, linewidths=0.2)
ax[0].plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
ax[0].plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
ax[0].set_title("2D Power absorbed by electron via FW(R,Z)")
fig.colorbar(im0, ax=ax[0], label="$W/cm^3/MW_{abs}$")

im1 = ax[1].contourf(X, Z, TDPwEIBW, cmap='jet', levels = clevels, linewidths=0.2)
ax[1].plot(Xsurf, Zsurf, 'y', linewidth=2)
ax[1].plot(Xvessel, Zvessel, 'c', linewidth=2)
ax[1].set_title("2D Power abs by electron via IBW(R,Z)")
fig.colorbar(im1, ax=ax[1], label="$W/cm^3/MW_{abs}$")

for a in ax:
    a.set_xlabel("R (cm)")
    a.set_ylabel("Z (cm)")
    a.set_aspect('equal')
    a.grid()
    a.minorticks_on()

plt.tight_layout()
plt.savefig('2DPowProfile_ele.pdf',dpi = 300,  bbox_inches='tight')
plt.close()


plt.figure(figsize=(15, 8))

plt.subplot(1,3,1)
im1 = plt.contourf(X, Z, ReEplus, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("Re E+(R,Z)")
plt.colorbar(im1,label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.subplot(1,3,2)
im2 = plt.contourf(X, Z, ImEplus, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("Im E+(R,Z)")
plt.colorbar(im2, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.subplot(1,3,3)
im3 =plt.contourf(X, Z, Eplus_mag, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("|E+|(R,Z)")
plt.colorbar(im3, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.savefig('E+.pdf',dpi = 300,  bbox_inches='tight')
plt.close()

plt.figure(figsize=(15, 8))
plt.subplot(1,3,1)
im1 = plt.contourf(X, Z, ReEminus, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("Re E-(R,Z)")
plt.colorbar(im1, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.subplot(1,3,2)
im2 = plt.contourf(X, Z, ImEminus, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("Im E-(R,Z)")
plt.colorbar(im2, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.subplot(1,3,3)
im3 = plt.contourf(X, Z, Eminus_mag, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("|E-|(R,Z)")
plt.colorbar(im3, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.savefig('E-.pdf',dpi = 300,  bbox_inches='tight')
plt.close()

plt.figure(figsize=(15, 8))

plt.subplot(1,3,1)
im1 = plt.contourf(X, Z, ReEzeta, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("Re Eζ(R,Z)")
plt.colorbar(im1, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.subplot(1,3,2)
im2 = plt.contourf(X, Z, ImEzeta, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("Im Eζ(R,Z)")
plt.colorbar(im2, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.subplot(1,3,3)
im3 = plt.contourf(X, Z, Ezeta_mag, cmap='jet', levels = clevels, linewidths=0.2)
plt.plot(Xsurf, Zsurf, 'y', linewidth=2, label="viridis (LCFS)")
plt.plot(Xvessel, Zvessel, 'c', linewidth=2, label="Vessel")
plt.title("|Eζ|(R,Z)")
plt.colorbar(im3, label="$V/m/MW_{abs}$")
plt.xlabel("R (cm)")
plt.ylabel("Z (cm)")
plt.axis('equal')
plt.grid()
plt.minorticks_on()
plt.tight_layout()

plt.savefig('Ezeta.pdf',dpi = 300,  bbox_inches='tight')
plt.close()

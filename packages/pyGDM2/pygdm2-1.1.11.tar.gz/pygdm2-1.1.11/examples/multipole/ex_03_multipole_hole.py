# encoding: utf-8
"""
getting started
===============

demonstration of the basic functionality and usage of torchgdm

author: P. Wiecha, 10/2024
"""
# %%
# imports
# -------
from __future__ import print_function, division

## --- load the modules
import numpy as np
import matplotlib.pyplot as plt

import pyGDM2 as gdm

# %%
# simulation setup
# ----------------
# we set up the environemnt, illumination field(s) and the structure(s).
# This is then wrapped up in an instance of `Simulation`.
#
#  - structure: sphere of 160nm radius,
#  - constant dielectric function
#  - incident field: plane wave, 400nm, lin. pol. along X
#  - homogeneous environment with n=1
## --- simulation initialization ---

## --- geometry
mesh = "hex"
step = 25  # in nm
radius = 60  # in nm
height = 120  # in nm
hole_radius = 25  # in nm


## --- Full nanodisc
geometry_0 = gdm.structures.nanodisc(step, R=radius / step, H=height // step, mesh=mesh)
## --- Holed nanodisc
## We copy the full nanodisc meshpoints except where the hole is
X_h, _, Z_h = geometry_0.T
X_h = X_h - np.mean(X_h) + radius / 2.0  # hole center = radius/2
Z_h = Z_h - np.mean(Z_h)
geometry_1 = geometry_0.copy()[X_h**2 + Z_h**2 > hole_radius**2]

material = gdm.materials.silicon()
struct_0 = gdm.structures.struct(step, geometry_0, material)
struct_1 = gdm.structures.struct(step, geometry_1, material)


## --- incident field: lin. pol plane wave
field_generator = gdm.fields.plane_wave
wavelengths = np.arange(400, 700, 20)
kwargs = dict(theta=0.0, inc_angle=180)  ## normal incidence from top
efield = gdm.fields.efield(field_generator, wavelengths=wavelengths, kwargs=kwargs)


## --- environment
dyads = gdm.propagators.DyadsQuasistatic123(n1=1, n2=1)


## --- create simulation instance
sim_0 = gdm.core.simulation(struct_0, efield, dyads)
sim_1 = gdm.core.simulation(struct_1, efield, dyads)

gdm.visu.structure(sim_0, projection="XZ")
print("full:   N dp={}".format(len(geometry_0)))
gdm.visu.structure(sim_1, projection="XZ")
print("hole:   N dp={}".format(len(geometry_0)))

## --- run the main simulation ---
sim_0.scatter()
sim_1.scatter()

# %%
# extinction spectra
# ------------------

## -- spectra of extinction sections per multipole moment
wl, spec1 = gdm.tools.calculate_spectrum(sim_0, 0, gdm.linear.extinct)
ex_0, sc_0, ab_0 = spec1.T
wl, spec2 = gdm.tools.calculate_spectrum(sim_0, 0, gdm.multipole.extinct)
ex_p_0, ex_m_0, ex_qe_0, ex_qm_0 = spec2.T

plt.figure()
plt.title("full disc")
plt.plot(wl, ex_0, label="extinct")
plt.plot(wl, ex_p_0, label="p")
plt.plot(wl, ex_m_0, label="m")
plt.plot(wl, ex_p_0 + ex_m_0, label="dipole sum", dashes=[2, 2])

plt.legend()
plt.xlabel("wavelength (nm)")
plt.ylabel("extinction cross section (nm^2)")
plt.show()


## -- spectra of extinction sections per multipole moment
wl, spec1 = gdm.tools.calculate_spectrum(sim_1, 0, gdm.linear.extinct)
ex_1, sc_1, ab_1 = spec1.T
wl, spec2 = gdm.tools.calculate_spectrum(sim_1, 0, gdm.multipole.extinct)
ex_p_1, ex_m_1, ex_qe_1, ex_qm_1 = spec2.T

plt.figure()
plt.title("disc with hole")
plt.plot(wl, ex_1, label="extinct")
plt.plot(wl, ex_p_1, label="p")
plt.plot(wl, ex_m_1, label="m")
plt.plot(wl, ex_qe_1, label="Qe")
plt.plot(wl, ex_qm_1, label="Qm")
plt.plot(wl, ex_p_1 + ex_m_1 + ex_qe_1 + ex_qm_1, label="multipole sum", dashes=[2, 2])

plt.legend()
plt.xlabel("wavelength (nm)")
plt.ylabel("extinction cross section (nm^2)")
plt.show()

# %%
# near-fields
# ----------_
# We now plot the near-field intensity inside the sphere.
# We use the first field-config (=index 0), slice through sphere center

## -- nearfield intensity map: full disc
wl_0 = 540  # MD resonance
delta_wl = np.abs(wl - wl_0)
i_0 = np.argmin(delta_wl)
plt.figure()
MAP = gdm.tools.generate_NF_map_XZ(-150, 150, 51, -100, 200, 51, Y0=0)
Etot_0 = gdm.linear.nearfield(sim_0, field_index=i_0, r_probe=MAP, which_fields=["Et"])[0]
gdm.visu.vectorfield_color(
    Etot_0,
    cmap="jet",
    projection="XZ",
    fieldComp="I",
    clim=(0, 30),
    tit="full disc",
    interpolation="bicubic",
    show=True,
)

#%%
## -- nearfield intensity map: with hole
wl_1 = 476  # MD resonance
delta_wl = np.abs(wl - wl_1)
i_1 = np.argmin(delta_wl)
plt.figure()
MAP = gdm.tools.generate_NF_map_XZ(-150, 150, 51, -100, 200, 51, Y0=0)
Etot_1 = gdm.linear.nearfield(sim_1, field_index=i_1, r_probe=MAP, which_fields=["Et"])[0]
gdm.visu.vectorfield_color(
    Etot_1,
    cmap="jet",
    projection="XZ",
    fieldComp="I",
    clim=(0, 30),
    tit="with hole",
    interpolation="bicubic",
    show=True,
)


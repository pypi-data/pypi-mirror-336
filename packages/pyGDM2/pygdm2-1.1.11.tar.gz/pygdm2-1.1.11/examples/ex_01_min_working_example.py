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

import matplotlib.pyplot as plt
import numpy as np

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

# geometry
step = 20
geometry = gdm.structures.sphere(step, R=4.2, mesh="cube")
material = gdm.materials.dummy(3.0)
struct = gdm.structures.struct(step, geometry, material)

# illumination
field_generator = gdm.fields.plane_wave
wavelengths = np.linspace(500, 1000, 51)
kwargs = dict(inc_angle=0, inc_plane="xz", theta=0)
efield = gdm.fields.efield(field_generator, wavelengths=wavelengths, kwargs=kwargs)

# environment: vacuum
n1 = 1.0
dyads = gdm.propagators.DyadsQuasistatic123(n1)

# create simulation
sim = gdm.core.simulation(struct, efield, dyads)


plt.subplot()
gdm.visu.structure(sim)
plt.show()

# %%
# run the simulation
# ------------------
# we run the simulation by calling its `scatter` method.
# This evaulates the self-consistend fields at each dipole location.

# - run the simulation
sim.scatter()


# %%
# Visualize fields
# ----------------
# We now plot the near-field intensity inside the sphere.
# We use the first field-config (=index 0), slice through sphere center

plt.subplot(131)
gdm.visu.vectorfield_color_by_fieldindex(sim, 0, projection="XY", slice_level=160)
plt.subplot(132)
gdm.visu.vectorfield_color_by_fieldindex(sim, 0, projection="XZ", slice_level=0)
plt.subplot(133)
gdm.visu.vectorfield_color_by_fieldindex(sim, 0, projection="YZ", slice_level=0)
plt.tight_layout()
plt.show()

# %%
# Visualize fields
# ----------------
# We now re-propagate the fields to the surrounding to obtain the 
# near-fields in a plane below the particle.

Z0 = -3 * step
r_probe = gdm.tools.generate_NF_map_XY(-500, 500, 51, -500, 500, 51, Z0=Z0)
Es, Etot, Bs, Btot = gdm.linear.nearfield(sim, field_index=0, r_probe=r_probe)

# plot
gdm.visu.structure(sim, zorder=10, scale=0.1, show=0)
im = gdm.visu.vectorfield_color(Etot, show=0)
plt.colorbar(im)
plt.show()


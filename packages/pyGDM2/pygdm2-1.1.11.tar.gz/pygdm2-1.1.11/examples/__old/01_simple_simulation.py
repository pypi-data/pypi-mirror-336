# encoding: utf-8
import matplotlib.pyplot as plt

from pyGDM2 import structures
from pyGDM2 import materials
from pyGDM2 import propagators
from pyGDM2 import fields
from pyGDM2 import core
from pyGDM2 import visu

## --- simulation initialization ---
## structure: sphere of 160nm radius,
## constant dielectric function,
step = 20
geometry = structures.sphere(step, R=4.2, mesh='cube')
material = materials.dummy(2.0)
struct = structures.struct(step, geometry, material)

## incident field: plane wave, 400nm, lin. pol. along X
field_generator = fields.plane_wave
wavelengths = [400]
kwargs = dict(inc_angle=0, inc_plane='xz', theta=0)
efield = fields.efield(field_generator, 
               wavelengths=wavelengths, kwargs=kwargs)

## environment: vacuum
n1 = 1.0
dyads = propagators.DyadsQuasistatic123(n1)

## create simulation object
sim = core.simulation(struct, efield, dyads)


plt.subplot()
visu.structure(sim)
# visu.structure_contour(sim)
plt.show()


## --- run the simulation ---
core.scatter(sim)


## --- plot the near-field inside the sphere ---
## using first (of one) field-config (=index 0)
## slice through sphere center
plt.subplot(131)
visu.vectorfield_color_by_fieldindex(sim, 0, projection='XY', slice_level=160)
plt.subplot(132)
visu.vectorfield_color_by_fieldindex(sim, 0, projection='XZ', slice_level=0)
plt.subplot(133)
visu.vectorfield_color_by_fieldindex(sim, 0, projection='YZ', slice_level=0)
plt.tight_layout()
plt.show()

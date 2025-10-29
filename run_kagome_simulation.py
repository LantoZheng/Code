#!/usr/bin/env python3
"""
Run Kagome Lattice Gold Moth-Eye Simulation
This script extracts and runs the kagome lattice simulation from the notebook
"""

import meep as mp
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

# =============================================================================
# SIMULATION PARAMETERS - VISIBLE SPECTRUM (380-750 nm)
# =============================================================================

# Wavelength range (visible spectrum in micrometers)
wl_min = 0.38  # 380 nm (violet)
wl_max = 0.75  # 750 nm (red)
wl_center = (wl_min + wl_max) / 2  # 565 nm (center of visible)

# Convert wavelength to frequency (c=1 in Meep units)
fcen = 1/wl_center  # Center frequency
df = 1/wl_min - 1/wl_max  # Frequency width
nfreq = 200  # Number of frequency points

print(f"Visible Spectrum Simulation:")
print(f"  Wavelength range: {wl_min} - {wl_max} μm ({wl_min*1000:.0f} - {wl_max*1000:.0f} nm)")
print(f"  Center wavelength: {wl_center} μm ({wl_center*1000:.0f} nm)")
print(f"  Frequency range: {fcen-df/2:.3f} - {fcen+df/2:.3f} (1/μm)")
print()

# =============================================================================
# METALLIC GOLD MATERIAL (Drude Model)
# =============================================================================

# Gold Drude model parameters (SI units converted to eV)
wp = 9.0  # Plasma frequency in eV
gamma = 0.07  # Damping rate in eV

# Create gold material using Drude model
coating_material = mp.Medium(
    epsilon=1.0,
    E_susceptibilities=[
        mp.DrudeSusceptibility(
            frequency=wp,
            gamma=gamma,
            sigma=1.0
        )
    ]
)

# Substrate material (glass)
n_substrate = 1.5
substrate_medium = mp.Medium(index=n_substrate)

print(f"Material properties (METALLIC GOLD):")
print(f"  Coating (moth-eye): Gold (Drude model)")
print(f"    Plasma frequency: {wp} eV")
print(f"    Damping: {gamma} eV")
print(f"  Substrate: n = {n_substrate} (glass)")
print(f"  Surrounding: n = 1.0 (air)")
print(f"  → Plasmonic gold nanostructures on glass substrate")
print()

# =============================================================================
# KAGOME LATTICE GEOMETRY PARAMETERS
# =============================================================================

# Cone dimensions
period = 0.75  # Cone spacing (1.5x increased from 0.5 μm)
cone_base = 0.6  # Base diameter (increased from 0.4 for better coverage)
cone_height = 0.4  # Height (increased from 0.3)

# Kagome lattice unit cell (3 cones per cell)
sx = 2 * period  # 1.5 μm
sy = period * np.sqrt(3)  # 1.299 μm  
sz = 4.0  # Total simulation height

# Kagome positions (3 cones per unit cell)
kagome_positions = [
    (0, 0),                           # Cone 1
    (period, 0),                      # Cone 2
    (period/2, period * np.sqrt(3)/2) # Cone 3
]

# Substrate parameters
h_substrate = 0.5  # Substrate thickness
substrate_bottom = -sz/2  # Bottom of simulation
cone_base_z = 0.0  # Base of cone at z=0
structure_top = cone_base_z + cone_height

fill_factor = 3 * np.pi * (cone_base/2)**2 / (sx * sy)

print(f"Kagome Lattice Configuration:")
print(f"  Lattice type: Kagome (3 cones/cell)")
print(f"  Period: {period} μm (cone spacing)")
print(f"  Unit cell: {sx:.3f} × {sy:.3f} μm")
print(f"  Cone diameter: {cone_base} μm")
print(f"  Cone height: {cone_height} μm")
print(f"  Fill factor: {fill_factor*100:.1f}%")
print(f"  Height/Period ratio: {cone_height/period:.2f}")
print()

# =============================================================================
# BUILD SIMULATION GEOMETRY
# =============================================================================

print("="*70)
print("BUILDING 3D KAGOME LATTICE - GOLD")
print("="*70)

resolution = 50  # pixels per micrometer
dpml = 0.5  # PML thickness

# PML layers only in z-direction (propagation direction)
pml_layers = [mp.PML(dpml, direction=mp.Z)]

# Periodic boundary conditions in x and y
k_point = mp.Vector3(0, 0, 0)

# Build geometry - substrate + kagome array of cones
geometry = []

# 1. Glass substrate
substrate_thickness = h_substrate
substrate_center_z = cone_base_z - substrate_thickness/2
geometry.append(mp.Block(
    center=mp.Vector3(0, 0, substrate_center_z),
    size=mp.Vector3(sx, sy, substrate_thickness),
    material=substrate_medium
))

print(f"Substrate:")
print(f"  Position: z = {substrate_center_z - substrate_thickness/2:.2f} to {cone_base_z:.2f} μm")
print(f"  Size: {sx} × {sy} × {substrate_thickness} μm³")
print(f"  Material: Glass (n={n_substrate})")
print()

# 2. Kagome array of conical moth-eye structures (3 cones per unit cell)
num_layers = 8  # Number of layers to approximate cone
h_cone = cone_height
r_cone_base = cone_base / 2
w_cone_base = cone_base

print(f"Kagome Lattice - GOLD:")
print(f"  3 cones per unit cell at kagome positions")
print(f"  Each cone: {num_layers} cylindrical layers")

# Create 3 cones at kagome positions
for idx, (cone_x, cone_y) in enumerate(kagome_positions):
    # Offset to center in simulation cell
    cone_x_centered = cone_x - sx/2
    cone_y_centered = cone_y - sy/2
    
    for i in range(num_layers):
        layer_height = h_cone / num_layers
        z = cone_base_z + layer_height * (i + 0.5)
        
        # Tapered radius (linear cone profile)
        layer_radius = r_cone_base * (1 - i / num_layers)
        layer_width = 2 * layer_radius
        
        if layer_radius > 0.01:  # Skip layers that are too small
            geometry.append(mp.Cylinder(
                center=mp.Vector3(cone_x_centered, cone_y_centered, z),
                radius=layer_radius,
                height=layer_height,
                axis=mp.Vector3(0, 0, 1),
                material=coating_material
            ))
    
    print(f"  Cone {idx+1}: center at ({cone_x:.3f}, {cone_y:.3f}) μm")

print(f"  Base diameter: {w_cone_base} μm")
print(f"  Height: {h_cone} μm")
print(f"  Position: z = {cone_base_z:.2f} to {structure_top:.2f} μm")
print(f"  Material: Gold (plasmonic)")
print()

# =============================================================================
# SOURCE AND MONITORS
# =============================================================================

# Source position - above the structure
source_pos_z = structure_top + 0.5

# Monitor positions
refl_monitor_z = structure_top + 0.3  # Reflection monitor above structure
tran_monitor_z = substrate_center_z - substrate_thickness/2 - 0.1  # Below substrate

# Gaussian source (broadband, covers visible spectrum)
sources = [mp.Source(
    mp.GaussianSource(fcen, fwidth=df),
    component=mp.Ez,
    center=mp.Vector3(0, 0, source_pos_z),
    size=mp.Vector3(sx, sy, 0)
)]

print(f"Source & Monitors:")
print(f"  Source: z = {source_pos_z:.2f} μm (Gaussian pulse, visible)")
print(f"  Reflection monitor: z = {refl_monitor_z:.2f} μm")
print(f"  Transmission monitor: z = {tran_monitor_z:.2f} μm")
print(f"  Light direction: ↓ (-z, normal incidence)")
print()

print(f"Simulation will automatically utilize all available CPU cores for parallel computation")
print(f"Resolution: {resolution} pixels/μm")
print("="*70)
print()

# =============================================================================
# SIMULATION 1: NORMALIZATION (Empty, no structure)
# =============================================================================

print("STEP 1: Running normalization simulation (empty)...")
start_time = time.time()

cell = mp.Vector3(sx, sy, sz)

# Flux monitors
refl_fr = mp.FluxRegion(center=mp.Vector3(0, 0, refl_monitor_z), size=mp.Vector3(sx, sy, 0))
tran_fr = mp.FluxRegion(center=mp.Vector3(0, 0, tran_monitor_z), size=mp.Vector3(sx, sy, 0))

# Empty simulation (no structure)
sim_empty = mp.Simulation(
    cell_size=cell,
    sources=sources,
    k_point=k_point,
    boundary_layers=pml_layers,
    resolution=resolution,
    force_complex_fields=True  # Required for metallic materials
)

refl_empty = sim_empty.add_flux(fcen, df, nfreq, refl_fr)
tran_empty = sim_empty.add_flux(fcen, df, nfreq, tran_fr)

sim_empty.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, mp.Vector3(0, 0, tran_monitor_z), 1e-3))

freqs = mp.get_flux_freqs(refl_empty)
straight_refl_flux = mp.get_fluxes(refl_empty)
straight_tran_flux = mp.get_fluxes(tran_empty)

straight_refl_data = sim_empty.get_flux_data(refl_empty)

sim_time_1 = time.time() - start_time
print(f"✓ Normalization complete ({sim_time_1:.2f} sec)")
print()

# =============================================================================
# SIMULATION 2: WITH KAGOME STRUCTURE
# =============================================================================

print("STEP 2: Running simulation with kagome lattice structure...")
start_time_2 = time.time()

sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    sources=sources,
    k_point=k_point,
    boundary_layers=pml_layers,
    resolution=resolution,
    force_complex_fields=True  # Required for metallic materials
)

refl = sim.add_flux(fcen, df, nfreq, refl_fr)
tran = sim.add_flux(fcen, df, nfreq, tran_fr)

sim.load_minus_flux_data(refl, straight_refl_data)

sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, mp.Vector3(0, 0, tran_monitor_z), 1e-3))

refl_flux = mp.get_fluxes(refl)
tran_flux = mp.get_fluxes(tran)

sim_time_2 = time.time() - start_time_2
total_time = sim_time_1 + sim_time_2

print(f"✓ Structure simulation complete ({sim_time_2:.2f} sec)")
print(f"✓ Total simulation time: {total_time:.2f} sec")
print()

# =============================================================================
# ANALYSIS & RESULTS
# =============================================================================

print("="*70)
print("CALCULATING OPTICAL PROPERTIES")
print("="*70)

# Calculate normalized fluxes
Rs = -np.array(refl_flux) / np.array(straight_refl_flux)
Ts = np.array(tran_flux) / np.array(straight_tran_flux)
As = 1 - Rs - Ts  # Absorbance

# Convert frequencies to wavelengths
wls = 1 / np.array(freqs)
wls_nm = wls * 1000  # Convert to nanometers

# Extract visible spectrum data
visible_mask = (wls >= wl_min) & (wls <= wl_max)
visible_wls = wls_nm[visible_mask]
visible_Rs = Rs[visible_mask]
visible_Ts = Ts[visible_mask]
visible_As = As[visible_mask]

# Calculate average performance
avg_R = np.mean(visible_Rs) * 100
avg_T = np.mean(visible_Ts) * 100
avg_A = np.mean(visible_As) * 100

# Find result at center wavelength
center_idx = np.argmin(np.abs(wls - wl_center))
reflectance = Rs[center_idx] * 100
transmittance = Ts[center_idx] * 100
absorbance = As[center_idx] * 100

print(f"Visible Spectrum Average:")
print(f"  - Reflectance:   {avg_R:.2f}%")
print(f"  - Transmittance: {avg_T:.2f}%")
print(f"  - Absorbance:    {avg_A:.2f}%")
print()
print(f"At Center Wavelength ({wl_center*1000:.0f} nm):")
print(f"  - Reflectance:   {reflectance:.2f}%")
print(f"  - Transmittance: {transmittance:.2f}%")
print(f"  - Absorbance:    {absorbance:.2f}%")
print(f"{'='*70}")

# =============================================================================
# VISUALIZATION
# =============================================================================

print("\nCreating visualization...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('3D Kagome Lattice Moth-Eye Array (GOLD) - Visible Spectrum (380-750nm)', 
             fontsize=16, fontweight='bold')

# Plot 1: Spectral Response
ax = axes[0, 0]
ax.plot(visible_wls, visible_Rs, 'b-', linewidth=2.5, label='Reflectance')
ax.plot(visible_wls, visible_Ts, 'r-', linewidth=2.5, label='Transmittance')
ax.plot(visible_wls, visible_As, 'g-', linewidth=2.5, label='Absorbance')

ax.axvspan(380, 495, alpha=0.08, color='purple', label='Violet-Blue')
ax.axvspan(495, 590, alpha=0.08, color='yellow', label='Green-Yellow')
ax.axvspan(590, 750, alpha=0.08, color='red', label='Orange-Red')
ax.axvline(wl_center*1000, color='gray', linestyle='--', linewidth=1.5, 
          label=f'Center: {wl_center*1000:.0f}nm')

ax.set_xlabel('Wavelength (nm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Ratio', fontsize=12, fontweight='bold')
ax.set_title('Spectral Response', fontsize=13, fontweight='bold')
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
ax.set_xlim(wl_min*1000, wl_max*1000)
ax.set_ylim(0, 1.05)

# Plot 2: Cross-section (xz plane)
ax = axes[0, 1]
ax.set_aspect('equal')
view_width = 1.5
ax.set_xlim(-view_width, view_width)
ax.set_ylim(-0.5, sz/2 + 0.5)

# Draw kagome cones in cross-section (show first two cones)
for cone_x, cone_y in kagome_positions[:2]:
    x_offset = cone_x - sx/2
    
    # Substrate
    substrate = Rectangle((x_offset - period/2, 0), period, h_substrate, 
                          facecolor='lightgray', edgecolor='black', linewidth=0.5,
                          alpha=0.7)
    ax.add_patch(substrate)
    
    # Cone layers
    for i in range(num_layers):
        layer_height = h_cone / num_layers
        layer_center_z = cone_base_z + layer_height * (i + 0.5)
        layer_radius = r_cone_base * (1 - i / num_layers)
        
        if layer_radius > 0.01:
            layer = Rectangle((x_offset - layer_radius, layer_center_z - layer_height/2), 
                             2*layer_radius, layer_height,
                             facecolor='gold', edgecolor='black', alpha=0.6, linewidth=0.3)
            ax.add_patch(layer)

# Draw source
ax.axhline(source_pos_z, color='red', linestyle='-', linewidth=3, alpha=0.8, label='Source')
ax.arrow(0, source_pos_z, 0, -0.3, head_width=0.1, head_length=0.08, 
         fc='red', ec='red', alpha=0.7, linewidth=2)

# Draw monitors
ax.axhline(refl_monitor_z, color='blue', linestyle='--', linewidth=2, alpha=0.7, label='Refl')
ax.axhline(tran_monitor_z, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Trans')

ax.set_xlabel('X (μm)', fontsize=11, fontweight='bold')
ax.set_ylabel('Z (μm)', fontsize=11, fontweight='bold')
ax.set_title('Kagome Lattice Cross-section (xz)', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)

# Plot 3: Top view (xy plane) - showing kagome lattice
ax = axes[1, 0]
ax.set_aspect('equal')
view_range_x = 2.5 * period
view_range_y = 2.5 * period * np.sqrt(3) / 2
ax.set_xlim(-view_range_x, view_range_x)
ax.set_ylim(-view_range_y, view_range_y)

# Draw 3x2 array of kagome unit cells
for i in range(-1, 2):  # x-direction cells
    for j in range(-1, 2):  # y-direction cells
        cell_offset_x = i * sx
        cell_offset_y = j * sy
        
        # Draw all 3 cones in this unit cell
        for cone_x, cone_y in kagome_positions:
            x_pos = cone_x + cell_offset_x
            y_pos = cone_y + cell_offset_y
            
            # Draw cone base
            circle = Circle((x_pos, y_pos), r_cone_base, 
                           color='gold', alpha=0.6, edgecolor='black', linewidth=1.5)
            ax.add_patch(circle)
            
            # Draw layers to show conical structure
            for k in range(0, num_layers, 2):
                layer_radius = r_cone_base * (1 - k / num_layers)
                if layer_radius > 0.01:
                    circle = Circle((x_pos, y_pos), layer_radius, 
                                   fill=False, edgecolor='darkgoldenrod', linestyle=':', alpha=0.5)
                    ax.add_patch(circle)

# Draw kagome unit cell boundary
unit_cell_corners = np.array([
    [0, 0],
    [sx, 0],
    [sx, sy],
    [0, sy],
    [0, 0]
])
unit_cell = Polygon(unit_cell_corners, fill=False, edgecolor='red', linewidth=2.5, 
                     linestyle='--', label='Unit cell')
ax.add_patch(unit_cell)

ax.set_xlabel('X (μm)', fontsize=11, fontweight='bold')
ax.set_ylabel('Y (μm)', fontsize=11, fontweight='bold')
ax.set_title('Top View - Kagome Lattice (xy)', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)

# Plot 4: Performance Summary
ax = axes[1, 1]
ax.axis('off')

perf_text = f"""
{'='*54}
3D KAGOME LATTICE MOTH-EYE - GOLD
{'='*54}

Lattice Configuration:
  • Lattice type: Kagome (3 cones/cell)
  • Period: {period} μm (cone spacing)
  • Unit cell: {sx:.3f} × {sy:.3f} μm
  • Cone density: {3/(sx*sy):.2f} cones/μm²
  • Fill factor: {3*np.pi*r_cone_base**2/(sx*sy)*100:.1f}%
  • Boundary: Periodic in X,Y (infinite array)

Structure Layout:
  • Substrate: z = 0 to {h_substrate:.2f} μm (n={n_substrate})
  • Cone: z = {cone_base_z:.2f} to {structure_top:.2f} μm (GOLD - Drude model)
  • Source: z = {source_pos_z:.2f} μm (above structure)
  • Light direction: ↓ (-z, normal incidence)

Wavelength Range:
  • Full visible: {wl_min*1000:.0f}-{wl_max*1000:.0f} nm
  • Violet-Blue: {wl_min*1000:.0f}-495 nm
  • Green-Yellow: 495-590 nm
  • Orange-Red: 590-{wl_max*1000:.0f} nm

Simulation Settings:
  • Resolution: {resolution} pixels/μm
  • Freq. points: {nfreq}
  • CPU cores: {mp.count_processors()}
  • Grid: ~{int(sx*sy*sz*resolution**3/1e3):.0f}k points

Execution Time:
  • Normalization: {sim_time_1:.2f} sec
  • Structure sim: {sim_time_2:.2f} sec
  • Total: {total_time:.2f} sec

PERFORMANCE (Visible Range):
  • Reflectance:   {avg_R:.2f}%
  • Transmittance: {avg_T:.2f}%
  • Absorbance:    {avg_A:.2f}%

At Center ({wl_center*1000:.0f}nm):
  • Reflectance:   {reflectance:.2f}%
  • Transmittance: {transmittance:.2f}%
  • Absorbance:    {absorbance:.2f}%

Features:
  ✓ 3D cylindrical cones
  ✓ Kagome lattice arrangement  
  ✓ Periodic boundary (infinite array)
  ✓ Gold plasmonic nanostructures
  ✓ Visible spectrum coverage
  ✓ Multi-core parallel processing
"""

ax.text(0.05, 0.95, perf_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        family='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()
plt.savefig('kagome_gold_mothye_result.png', dpi=150, bbox_inches='tight')
print(f"✓ Visualization saved as 'kagome_gold_mothye_result.png'")
plt.show()

print("\n" + "="*70)
print("KAGOME LATTICE SIMULATION COMPLETE!")
print("="*70)

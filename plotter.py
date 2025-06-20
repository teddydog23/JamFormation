# traffic_ovm/plotter.py

import matplotlib.pyplot as plt
import numpy as np

def shade_slowdowns(ax, sections, color='lightgray'):
    for s in sections['slowdowns']:
        ax.axvspan(s['start'], s['end'], color=color, alpha=0.3, label='Slowdown' if 'Slowdown' not in ax.get_legend_handles_labels()[1] else None)

def plot_velocity(x, v, sections, title="Velocity Profile"):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(x, v, s=5, color='blue', label='Velocity')
    shade_slowdowns(ax, sections)
    ax.set_xlabel("Position")
    ax.set_ylabel("Velocity")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def plot_headway(x, sections, title="Headway Profile"):
    x_sorted = np.sort(x)
    headway = np.diff(np.concatenate((x_sorted, [x_sorted[0] + sections['L']])))
    pos = x_sorted

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(pos, headway, s=5, color='green', label='Headway')
    shade_slowdowns(ax, sections)
    ax.set_xlabel("Position")
    ax.set_ylabel("Headway")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def plot_current_vs_density(densities, currents, label="Simulated", theoretical_curve=None):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(densities, currents, 'o-', label=label)
    if theoretical_curve:
        dx_vals = np.linspace(1.0, 10.0, 200)
        J_vals = [theoretical_curve(dx) for dx in dx_vals]
        rho_vals = 1.0 / dx_vals
        ax.plot(rho_vals, J_vals, '--', label='Theoretical')
    ax.set_xlabel("Density")
    ax.set_ylabel("Current")
    ax.set_title("Fundamental Diagram (Current vs Density)")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.show()

def plot_jam_length_vs_density(densities, jam_ratios_dict, theoretical=None, title="Jam-Length Ratio vs Density"):
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, ratios in jam_ratios_dict.items():
        ax.plot(densities, ratios, 'o-', label=label)

    if theoretical:
        ax.plot(densities, theoretical, 'k--', label="Theoretical")

    ax.set_xlabel("Density")
    ax.set_ylabel("Jam Length Ratio (lJ / L)")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()
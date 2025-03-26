# KPU Quantum Computing Package
# Initialization file for KPU module

from KPU.Kalacell import KPUChip, KPUConfig,kala_time_travel_formula, quantum_multiverse_formula, quantum_fourier_transform, get_device, kpu_banner


__version__ = "1.1.2"

__all__ = [
    "KPUChip",
    "KPUConfig",
    "kala_time_travel_formula",
    "quantum_multiverse_formula",
    "quantum_fourier_transform",
    "get_device",
    "kpu_banner"
]

# Display KPU banner on import
kpu_banner()

import streamlit as st
import numpy as np

# Set up page styling for a dark tech/lab theme
st.set_page_config(page_title="Advanced Materials & Biochar Lab", layout="centered")

st.title("🔬 Advanced Structural Material Mechanics & Biochar Lab")
st.write("Adjust parameters below to simulate material performance.")

# --- SIDEBAR / CONTROLS (Perfect for Mobile dropdowns) ---
st.header("🎛️ Lab Control Panel")

# Material Selection
materials = ["Concrete", "Steel", "Timber"]
selected_mat = st.selectbox("Core Material Matrix:", materials)

# Dimensions
st.subheader("📐 Specimen Dimensions (Inches)")
col1, col2, col3 = st.columns(3)
with col1:
    L_in = st.number_input("Length (in):", min_value=0.1, value=6.0, step=0.5)
with col2:
    W_in = st.number_input("Width (in):", min_value=0.1, value=6.0, step=0.5)
with col3:
    H_in = st.number_input("Height (in):", min_value=0.1, value=6.0, step=0.5)

# Concrete Specific Settings
concrete_mixes = {
    "M15 (1:2:4)": {"c": 1, "s": 2, "ag": 4, "fcr": 2200},
    "M20 (1:1.5:3)": {"c": 1, "s": 1.5, "ag": 3, "fcr": 3000},
    "M25 (1:1:2)": {"c": 1, "s": 1, "ag": 2, "fcr": 4000}
}

biochar_pct = 0
struct_type = ""
mix_name = ""

if selected_mat == "Concrete":
    struct_type = st.selectbox("Structural Type:", ["PCC (Plain Cement Concrete)", "RCC (Reinforced Concrete)"])
    mix_name = st.selectbox("Mix Ratio Designation:", list(concrete_mixes.keys()))
    biochar_pct = st.slider("Biochar Dose (% by Cement Mass):", 0, 15, 0)

# --- COMPUTATION LOGIC ---
vol_cu_in = L_in * W_in * H_in
vol_cft = vol_cu_in / 1728.0

st.markdown("---")
st.header("📊 Laboratory Mechanical Report")

# Display Geometry
st.metric("Total Volume", f"{vol_cu_in:.2f} in³", f"{vol_cft:.4f} CFT")

if selected_mat == "Concrete":
    mix = concrete_mixes[mix_name]
    dry_vol_cft = vol_cft * 1.54
    sum_parts = mix["c"] + mix["s"] + mix["ag"]

    cement_cft = (mix["c"] / sum_parts) * dry_vol_cft
    sand_cft = (mix["s"] / sum_parts) * dry_vol_cft
    crush_cft = (mix["ag"] / sum_parts) * dry_vol_cft

    cement_bags = cement_cft / 1.25
    cement_kg = cement_bags * 50.0
    sand_kg = sand_cft * 45.35
    crush_kg = crush_cft * 45.35
    biochar_kg = cement_kg * (biochar_pct / 100.0)

    # Biochar curve logic
    base_psi = mix["fcr"]
    if biochar_pct == 0:
        calculated_strength = base_psi
        matrix_behavior = "Control formulation. No carbon modifications applied."
    elif biochar_pct <= 3:
        pct_increase = biochar_pct * 4.0
        calculated_strength = base_psi * (1.0 + (pct_increase / 100.0))
        matrix_behavior = f"🟢 Strength Increased (+{pct_increase:.1f}%). Biochar provides effective nucleation sites, filling capillary voids."
    else:
        pct_reduction = (biochar_pct - 3) * 3.5
        calculated_strength = base_psi * (1.0 - (pct_reduction / 100.0))
        matrix_behavior = f"🔴 Strength Reduced (-{pct_reduction:.1f}%). High aggregate replacement increases free water demand and structural micro-cracks."

    elastic_modulus = 57000 * np.sqrt(calculated_strength)
    tensile_strength = 7.5 * np.sqrt(calculated_strength)

    # UI Presentation
    st.subheader(f"Application Mode: {struct_type}")

    st.write("### Volumetrics")
    st.write(f"• **Cement:** {cement_kg:.2f} kg ({cement_bags:.2f} Bags)")
    st.write(f"• **Sand:** {sand_kg:.2f} kg")
    st.write(f"• **Crush:** {crush_kg:.2f} kg")
    st.write(f"• **Biochar:** {biochar_kg:.3f} kg ({biochar_pct}% cement replacement)")

    st.write("### Mechanical Performance")
    st.info(f"**Research Insight:** {matrix_behavior}")
    st.success(f"**Compressive Strength (f'c):** {calculated_strength:.0f} psi")
    st.warning(f"**Elastic Modulus (Ec):** {elastic_modulus:,.0f} psi")
    st.error(f"**Tensile Strength (fr):** {tensile_strength:.1f} psi")

elif selected_mat == "Steel":
    mass_kg = (vol_cft * 7850) / 35.3147
    st.write(f"• **Total Mass:** {mass_kg:,.2f} kg")
    st.write(f"• **Yield Strength (Fy):** 60,000 psi")
    st.write(f"• **Ultimate Tensile (Fu):** 90,000 psi")
    st.write(f"• **Modulus of Elasticity:** 29,000,000 psi")

elif selected_mat == "Timber":
    mass_kg = (vol_cft * 650) / 35.3147
    st.write(f"• **Total Mass:** {mass_kg:.2f} kg")
    st.write(f"• **Modulus of Rupture:** 8,500 psi")
    st.write(f"• **Elastic Modulus (E):** 1,600,000 psi")
    st.write(f"• **Compression Strength:** 5,200 psi")
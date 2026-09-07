import streamlit as st
import gsw

st.set_page_config(
    page_title="Seawater Density & Unit Converter",
    page_icon="🌊",
    layout="centered",
)

st.title("Seawater Density & Unit Converter")

st.write(
    "Calculate seawater density using TEOS-10 and convert "
    "between common oceanographic concentration units."
)

# ============================================================
# WATER PROPERTIES
# ============================================================

st.subheader("Water Properties")

salinity = st.number_input(
    "Practical Salinity (PSU)",
    min_value=0.0,
    max_value=50.0,
    value=35.0,
    step=0.1,
)

temperature = st.number_input(
    "Temperature (°C)",
    min_value=-5.0,
    max_value=50.0,
    value=20.0,
    step=0.1,
)

pressure = st.number_input(
    "Pressure (dbar)",
    min_value=0.0,
    value=0.0,
    step=1.0,
)

latitude = st.number_input(
    "Latitude (°)",
    min_value=-90.0,
    max_value=90.0,
    value=41.0,
    step=0.1,
)

longitude = st.number_input(
    "Longitude (°)",
    min_value=-180.0,
    max_value=180.0,
    value=-71.0,
    step=0.1,
)

# ============================================================
# DENSITY CALCULATION
# ============================================================

SA = gsw.SA_from_SP(
    salinity,
    pressure,
    longitude,
    latitude,
)

CT = gsw.CT_from_t(
    SA,
    temperature,
    pressure,
)

density = gsw.rho(
    SA,
    CT,
    pressure,
)

sigma0 = gsw.sigma0(
    SA,
    CT,
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Seawater Density",
        f"{density:.3f} kg/m³",
    )

with col2:
    st.metric(
        "Sigma-0",
        f"{sigma0:.3f} kg/m³",
    )

st.caption(
    f"Absolute Salinity: {SA:.4f} g/kg | "
    f"Conservative Temperature: {CT:.4f} °C"
)

# ============================================================
# CONVERSION FUNCTIONS
# ============================================================

def umolkg_to_uM(value, density):
    """Convert µmol/kg to µmol/L (µM)."""
    return value * density / 1000


def uM_to_umolkg(value, density):
    """Convert µmol/L (µM) to µmol/kg."""
    return value * 1000 / density


def umolkg_to_mmolm3(value, density):
    """Convert µmol/kg to mmol/m³."""
    return value * density / 1000


def mmolm3_to_umolkg(value, density):
    """Convert mmol/m³ to µmol/kg."""
    return value * 1000 / density


# ============================================================
# CONCENTRATION CONVERTER
# ============================================================

st.divider()

st.subheader("Concentration Converter")

conversion = st.selectbox(
    "Select conversion",
    [
        "µmol/kg → µM",
        "µM → µmol/kg",
        "µmol/kg → mmol/m³",
        "mmol/m³ → µmol/kg",
    ],
)

value = st.number_input(
    "Concentration",
    min_value=0.0,
    value=2000.0,
    step=1.0,
)

if conversion == "µmol/kg → µM":
    result = umolkg_to_uM(value, density)
    input_unit = "µmol/kg"
    output_unit = "µM"

elif conversion == "µM → µmol/kg":
    result = uM_to_umolkg(value, density)
    input_unit = "µM"
    output_unit = "µmol/kg"

elif conversion == "µmol/kg → mmol/m³":
    result = umolkg_to_mmolm3(value, density)
    input_unit = "µmol/kg"
    output_unit = "mmol/m³"

else:
    result = mmolm3_to_umolkg(value, density)
    input_unit = "mmol/m³"
    output_unit = "µmol/kg"

st.metric(
    "Converted Concentration",
    f"{result:.3f} {output_unit}",
)

st.caption(
    f"{value:.3f} {input_unit} = "
    f"{result:.3f} {output_unit} "
    f"at a density of {density:.3f} kg/m³."
)

# ============================================================
# NOTES
# ============================================================

with st.expander("About these calculations"):
    st.write(
        """
        Density is calculated using the TEOS-10 Gibbs SeaWater
        (GSW) toolbox.

        Practical Salinity is converted to Absolute Salinity using
        pressure, longitude, and latitude.

        In-situ temperature is converted to Conservative Temperature
        before density is calculated.

        Note that µM and mmol/m³ are numerically equivalent:
        1 µmol/L = 1 mmol/m³.
        """
    )
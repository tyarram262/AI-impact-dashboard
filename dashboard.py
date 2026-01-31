import streamlit as st
from google import genai
from ecologits import EcoLogits
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="AI Impact Dashboard", layout="wide")
st.title("🌍 AI Environmental Impact Dashboard")

# Initialize
EcoLogits.init(providers=["google_genai"])

#Constants for calculation
ENERGY_PER_REQUEST = {
    "Small": 0.0001,
    "Medium": 0.0005,
    "Large": 0.002,
    "Multimodal": 0.005
}

# Request type multipliers
REQUEST_TYPE_MULTIPLIER = {
    "Text": 1.0,
    "Image": 3.0,
    "Video": 10.0
}

# Scoring baselines (adjust as you see fit)
SCORE_BASELINES = {
    "energy_kwh": 10.0,   # 10 kWh -> 100 energy score
    "co2_kg": 5.0,        # 5 kg -> 100 CO₂ score
    "water_l": 50.0       # 50 L -> 100 water score
}

def _score(value, baseline):
    return min((value / baseline) * 100, 100)

def _rating(score):
    if score <= 20:
        return "A (Low Impact)"
    if score <= 40:
        return "B"
    if score <= 60:
        return "C"
    if score <= 80:
        return "D"
    return "E (Very High Impact)"

PUE = 1.2  # Power Usage Effectiveness (data center efficiency)
GRID_CARBON_INTENSITY = 0.5  # kg CO₂ per kWh (US average)
WUE = 1.8  # Water Usage Effectiveness (liters per kWh)


# Sidebar for input
with st.sidebar:
    st.header("⚙️ Input Parameters")
    
    num_requests = st.number_input(
        "Number of AI Requests",
        min_value=1,
        max_value=1000000,
        value=100,
        step=10
    )
    
    request_type = st.selectbox(
        "Request Type",
        options=["Text", "Image", "Video"]
    )
    
    model_class = st.selectbox(
        "Model Class",
        options=["Small", "Medium", "Large", "Multimodal"]
    )
    
    token_count = st.number_input(
        "Average Token Count per Request",
        min_value=10,
        max_value=100000,
        value=500,
        step=50,
        help="""
        **Token Guidelines for English:**
        - 1 token ≈ 4 characters or ¾ of a word
        - 100 tokens ≈ 75 words
        - 1-2 sentences ≈ 30 tokens
        - 1 paragraph ≈ 100 tokens
        - ~1,500 words ≈ 2,048 tokens
        """
    )
    
    inference_time = st.number_input(
        "Average Inference Time (ms)",
        min_value=1,
        max_value=10000,
        value=100,
        step=10
    )

    st.divider()
    
    

    if st.button("Calculate Impact", type="primary"):
        #Calculate base energy
        base_energy = ENERGY_PER_REQUEST[model_class]
        
        # Apply request type multiplier
        energy_per_request = base_energy * REQUEST_TYPE_MULTIPLIER[request_type]
        
        # Adjust for token count (scaling factor)
        token_factor = token_count / 500  # Normalize to 500 tokens
        energy_per_request *= token_factor
        
        # Adjust for inference time
        time_factor = inference_time / 100  # Normalize to 100ms
        energy_per_request *= time_factor
        
        # Total calculations
        total_energy = (num_requests * energy_per_request) * PUE
        total_co2 = total_energy * GRID_CARBON_INTENSITY
        total_water = total_energy * WUE
        Impact_Score = total_energy * 0.4 + total_co2 * 0.4 + total_water * 0.2

        
        # Store in session state
        st.session_state.energy = total_energy
        st.session_state.co2 = total_co2
        st.session_state.water = total_water
        st.session_state.energy_per_request = energy_per_request
        st.session_state.num_requests = num_requests
        st.session_state.impact_score = Impact_Score


# Main dashboard
if "energy" in st.session_state:
    energy = st.session_state.energy
    co2 = st.session_state.co2
    water = st.session_state.water
    
    st.success("✅ Impact calculated successfully!")
    
    st.divider()
    
    # Key Metrics
    st.subheader(f"📊 Total Environmental Impact")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Energy Consumed", f"{energy:.4f} kWh", 
                  help="Total energy including data center overhead (PUE)")
    with col2:
        st.metric("CO₂ Emissions", f"{co2:.4f} kg", 
                  help="Carbon emissions based on grid intensity")
    with col3:
        st.metric("Water Used", f"{water:.2f} L", 
                  help="Water consumed for cooling")
    
    st.divider()

        # Impact Score
    st.subheader("🏅 Impact Score")

    energy_score = _score(energy, SCORE_BASELINES["energy_kwh"])
    co2_score = _score(co2, SCORE_BASELINES["co2_kg"])
    water_score = _score(water, SCORE_BASELINES["water_l"])

    impact_score = ((energy_score * 0.4) + (co2_score * 0.4) + (water_score * 0.2))*100
    rating = _rating(impact_score)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Impact Score (0–100)", f"{impact_score:.1f}")
    with col2:
        st.metric("Rating", rating)

    st.caption(
        "A: Bottom 20% (Highly efficient) · B: 20–40% · C: 40–60% · D: 60–80% · E: Top 20% (Excessive)"
    )
    
    # Per-request breakdown
    st.subheader("🔍 Per-Request Breakdown")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Energy per Request", f"{st.session_state.energy_per_request:.6f} kWh")
    with col2:
        st.metric("Total Requests", f"{st.session_state.num_requests:,}")
    
    st.divider()
    
    # Projections
    st.subheader("📈 Daily & Yearly Projections")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Daily (Same Rate)**")
        daily_energy = energy
        daily_co2 = co2
        daily_water = water
        st.write(f"Energy: {daily_energy:.4f} kWh")
        st.write(f"CO₂: {daily_co2:.4f} kg")
        st.write(f"Water: {daily_water:.2f} L")
    
    with col2:
        st.write("**Monthly (30 days)**")
        monthly_energy = energy * 30
        monthly_co2 = co2 * 30
        monthly_water = water * 30
        st.write(f"Energy: {monthly_energy:.2f} kWh")
        st.write(f"CO₂: {monthly_co2:.2f} kg")
        st.write(f"Water: {monthly_water:.2f} L")
    
    with col3:
        st.write("**Yearly (365 days)**")
        yearly_energy = energy * 365
        yearly_co2 = co2 * 365
        yearly_water = water * 365
        st.write(f"Energy: {yearly_energy:.2f} kWh")
        st.write(f"CO₂: {yearly_co2:.2f} kg")
        st.write(f"Water: {yearly_water:.2f} L")
    
    st.divider()

    # Real-world comparisons
    st.subheader("🌳 Real-World Comparisons (Yearly)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Average home uses ~10,000 kWh/year
        home_equivalent = (yearly_energy / 10000) * 100
        st.metric("% of Home Energy Use", f"{home_equivalent:.2f}%")
    
    with col2:
        # 1 tree absorbs ~21 kg CO₂/year
        trees_needed = yearly_co2 / 21
        st.metric("Trees Needed to Offset", f"{trees_needed:.1f}")
    
    with col3:
        # Average person drinks ~730L water/year
        people_equivalent = yearly_water / 730
        st.metric("People's Annual Drinking Water", f"{people_equivalent:.2f}")
    
else:
    st.info("👈 Configure parameters in the sidebar and click 'Calculate Impact'")
    
    # Show example/instructions
    st.subheader("📋 How to Use")
    st.write("""
    1. **Number of Requests**: How many AI queries you expect
    2. **Request Type**: Text is cheapest, video is most expensive
    3. **Model Class**: Larger models consume more energy
    4. **Token Count**: More tokens = more computation
    5. **Inference Time**: Longer processing = more energy
    
    Click **Calculate Impact** to see your environmental footprint!
    """)
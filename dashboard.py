import streamlit as st
from google import genai
from ecologits import EcoLogits
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="AI Impact Dashboard", layout="wide")
st.title("🌍 AI Environmental Impact Dashboard")

# Initialize
EcoLogits.init(providers=["google_genai"])
client = genai.Client(api_key="AIzaSyAbV4-2Sw16NCepuJ-lMJmbbPfIQboCOhs")

# Sidebar for input
with st.sidebar:
    st.header("AI Prompt Input")
    user_prompt = st.text_area("Enter your prompt:")
    
    if st.button("Calculate Impact", type="primary"):
        if user_prompt:
            with st.spinner("Analyzing environmental impact..."):
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=user_prompt
                )
                
                impact = response.impacts
                energy_used = impact.energy.value
                water_used = energy_used * 1.8
                
                st.session_state.energy = energy_used
                st.session_state.water = water_used

# Main dashboard
if "energy" in st.session_state:
    energy = st.session_state.energy
    water = st.session_state.water

    st.divider()

    # Displaying AI Response
    st.subheader("AI Response")
    st.write(response.text)
    
    # Metrics row
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Energy Used (Single Prompt)", f"{energy:.6f} kWh")
    with col2:
        st.metric("Water Used (Single Prompt)", f"{water:.2f} L")
    
    # Projections
    st.subheader("📊 Daily & Yearly Projections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**10 Prompts/Day**")
        daily_10 = energy * 10
        yearly_10 = daily_10 * 365
        st.write(f"Daily: {daily_10:.4f} kWh | {daily_10 * 1.8:.2f} L")
        st.write(f"Yearly: {yearly_10:.2f} kWh | {yearly_10 * 1.8:.2f} L")
    
    with col2:
        st.write("**50 Prompts/Day**")
        daily_50 = energy * 50
        yearly_50 = daily_50 * 365
        st.write(f"Daily: {daily_50:.4f} kWh | {daily_50 * 1.8:.2f} L")
        st.write(f"Yearly: {yearly_50:.2f} kWh | {yearly_50 * 1.8:.2f} L")
    
#     # Chart
#     st.subheader("📈 Yearly Impact Comparison")
    
#     scenarios = ["10 Prompts/Day", "50 Prompts/Day"]
#     energy_yearly = [(yearly_10.value) if hasattr(yearly_10, 'value') else (yearly_10), 
#                      (yearly_50.value) if hasattr(yearly_50, 'value') else (yearly_50)]
#     water_yearly = [((yearly_10.value if hasattr(yearly_10, 'value') else yearly_10) * 1.8), 
#                     ((yearly_50.value if hasattr(yearly_50, 'value') else yearly_50) * 1.8)]
    
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
#     ax1.bar(scenarios, energy_yearly, color=["#2ecc71", "#e74c3c"])
#     ax1.set_ylabel("Energy (kWh)")
#     ax1.set_title("Yearly Energy Consumption")
#     ax1.grid(axis="y", alpha=0.3)
    
#     ax2.bar(scenarios, water_yearly, color=["#3498db", "#e67e22"])
#     ax2.set_ylabel("Water (Liters)")
#     ax2.set_title("Yearly Water Usage")
#     ax2.grid(axis="y", alpha=0.3)
    
#     st.pyplot(fig)
# else:
#     st.info("👈 Enter a prompt in the sidebar to calculate environmental impact")
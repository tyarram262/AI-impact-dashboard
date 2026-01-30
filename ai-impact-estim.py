from google import genai
from ecologits import EcoLogits
import os

# 1. Initialize the tracker
EcoLogits.init(providers=["google_genai"])

# 2. Initialize the Google Gemini client
client = genai.Client(api_key="AIzaSyAbV4-2Sw16NCepuJ-lMJmbbPfIQboCOhs")

user_prompt = input("Enter your prompt: ")

# 3. Run your AI prompt as usual
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=user_prompt
)

# 4. Access the hidden impact data
impact = response.impacts
energy_used = impact.energy.value # in kWh
water_used = energy_used * 1.8 # Estimate: 1.8L per kWh
print(f"Response: {response.texta}")
print(f"Energy: {energy_used} kWh")
print(f"Water: {water_used} Liters")


# 5. Environmental impact score
print("\n--- Environmental Impact Score ---")
daily_prompts_10 = energy_used * 10
daily_prompts_50 = energy_used * 50
water_10 = water_used * 10
water_50 = water_used * 50

print(f"10 prompts/day:  {daily_prompts_10:.4f} kWh | {water_10:.2f} Liters")
print(f"50 prompts/day:  {daily_prompts_50:.4f} kWh | {water_50:.2f} Liters")

# # Compare to typical household usage
# yearly_10 = daily_prompts_10 * 365
# yearly_50 = daily_prompts_50 * 365
# print(f"\nYearly (10/day): {yearly_10:.2f} kWh | {yearly_10 * 1.8:.2f} Liters")
# print(f"Yearly (50/day): {yearly_50:.2f} kWh | {yearly_50 * 1.8:.2f} Liters")
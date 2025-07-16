import streamlit as st
from datetime import date, timedelta
from dotenv import load_dotenv
import os
from openai import OpenAI
import time

# Load your OpenAI API key
load_dotenv()
client = OpenAI()

st.set_page_config(
    page_title="Travel Itinerary Planner",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Smart Travel Itinerary Planner")
st.write("Plan your trip with transport, beaches, spots, food & daily plan + budget!")

# --- User Inputs ---
source = st.text_input("Enter your source",placeholder= "state / city / Union Territory")
destination = st.text_input("Enter your destination", placeholder="state/ city / Union Territory")

start_date = st.date_input("Start date", date.today())
end_date = st.date_input("End date", date.today() + timedelta(days=3))

# --- Submit ---
if st.button("Generate Itinerary"):
    if start_date >= end_date:
        st.error("End date must be after start date.")
    else:
        days = (end_date - start_date).days + 1

        with st.spinner("Generating your detailed itinerary..."):
            # Compose prompt
            prompt = f"""
You are a travel planner. Create a detailed travel plan for this:
Source: {source}
Destination: {destination}
Start date: {start_date.strftime('%d %B %Y')}
End date: {end_date.strftime('%d %B %Y')}
Number of days: {days}

Output:
1️⃣ Best transport options from source to destination and return (bus/train/flight).
2️⃣ Local travel modes.
3️⃣ Best beaches or riverside/nature spots.
4️⃣ Famous tourist spots and local food must-try.
5️⃣ A complete day-wise itinerary: for each day, show plan from 8 AM to 8 PM, time slots, what to do.
6️⃣ Return plan.
7️⃣ Estimated budget for each section in Indian Rupees: travel, stay, food, activities. Give a total.
8️⃣ Format clearly with headings, bullet points and markdown.
"""
            
        # Progress bar and status
        progress_text = st.empty()
        progress_bar = st.progress(0)

        # Fake loading to show progress visually
        for percent_complete in range(0, 101, 5):
            progress_text.text(f"Generating... {percent_complete}%")
            progress_bar.progress(percent_complete)
            time.sleep(0.1)  # Simulate loading chunks

        # Call OpenAI API once
        with st.spinner("Finalizing..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content

        # Clear progress
        progress_bar.empty()
        progress_text.empty()

        # Show result
        st.markdown(result)

            

            

            


import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from groq import Groq as GroqClient
from PIL import Image
import base64
import io
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2. Setup Page Config
st.set_page_config(page_title="The Agentic Chef", layout="wide")

st.title("👨‍🍳 Smart Fridge Chef Agent")
st.markdown("Upload a photo of your fridge. I'll identify ingredients and find a recipe.")

# 3. Check for API Key
if not api_key:
    st.error("❌ API Key not found! Please check your .env file.")
    st.stop()

# 4. Initialize Clients
# --- Agent 1: The Vision Expert (Llama 4 Scout) ---
vision_client = GroqClient(api_key=api_key)

# --- Agent 2: The Chef (Llama 3.3) ---
# We use internal knowledge (no search tool) for speed and stability
chef_agent = Agent(
    name="Chef Ramsay",
    role="Professional Chef",
    model=Groq(id="llama-3.3-70b-versatile", api_key=api_key),
    instructions=[
        "You are a creative chef.",
        "Given a list of ingredients, generate 2 distinct recipes.",
        "Use your internal culinary knowledge. Do NOT search the internet.",
        "If the user is missing a critical item (like salt or oil), assume they have basic pantry staples.",
        "Format the output nicely with Markdown: ## Recipe Name, *Ingredients*, **Instructions**.",
        "Do not provide fake URLs. Instead, provide a 'Chef's Tip' for each dish."
    ],
    show_tool_calls=False,
    markdown=True,
)


# 5. Helper Function: Encode Image
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


# 6. The Vision Logic
def get_ingredients(image_base64):
    """Sends image to Llama-4-Scout to get ingredients list"""
    completion = vision_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Identify the edible ingredients in this image. Return ONLY a comma-separated list of items. Do not include containers or shelves."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            }
        ],
        temperature=0.1,
        max_tokens=1024,
    )
    return completion.choices[0].message.content


# 7. UI & Logic Flow
uploaded_file = st.file_uploader("📸 Snap a pic of your ingredients", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Display Image
    image = Image.open(uploaded_file)
    st.image(image, caption='Your Fridge', width=400)

    if st.button("🍳 Cook Something!"):

        # --- Step A: Vision ---
        with st.spinner("👀 Chef is looking at fridge..."):
            try:
                img_base64 = encode_image(image)
                ingredients_found = get_ingredients(img_base64)
                st.success(f"**Identified:** {ingredients_found}")
            except Exception as e:
                st.error(f"Vision Error: {e}")
                st.stop()

        # --- Step B: Reasoning ---
        with st.spinner("🧑‍🍳 Chef is thinking (By going creative)..."):
            try:
                # Pass the ingredients to the Chef Agent
                response = chef_agent.run(f"I have these ingredients: {ingredients_found}. Find me recipes.")

                # --- Step C: Display ---
                st.markdown("---")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Chef Error: {e}")
import streamlit as st
from ai_engine import analyze_dress_and_suggest_outfit, get_text_styling_advice

# Page Config
st.set_page_config(
    page_title="AuraStyle - AI Fashion Studio",
    page_icon="👗",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #FAFAFA; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; background-color: #FF4B4B; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("👗 AuraStyle: AI Wardrobe & Outfit Curator")
st.markdown("Your personal AI fashion studio with visual lookbooks and text-based styling.")
st.markdown("---")

tab1, tab2 = st.tabs(["📸 Upload Dress Photo", "💬 Ask via Text Prompt"])

# Curated high-fashion image bank for visual pairing cards
FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&auto=format&fit=crop&q=60",
    "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600&auto=format&fit=crop&q=60",
    "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600&auto=format&fit=crop&q=60",
    "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600&auto=format&fit=crop&q=60"
]

# --- TAB 1: IMAGE UPLOAD MODE ---
with tab1:
    st.subheader("Upload an Outfit Photo for Full Pairing Advice & Visuals")
    uploaded_image = st.file_uploader("Choose a dress image", type=["jpg", "jpeg", "png"], key="up1")
    occasion_1 = st.selectbox("Select Occasion", ["Festive / Traditional Function", "Casual Day Out", "Evening Dinner / Party", "Work / Formal Event"], key="occ_1")

    if uploaded_image is not None:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(uploaded_image, caption="Your Uploaded Outfit", use_container_width=True)
        with col2:
            st.write("")
            st.write("")
            if st.button("✨ Curate Matching Outfit & Visuals", key="btn_img"):
                with st.spinner("Analyzing style and fetching matching visual lookbooks..."):
                    try:
                        result = analyze_dress_and_suggest_outfit(uploaded_image, occasion_1)
                        st.session_state["result_img"] = result
                    except Exception as e:
                        st.error(f"Error: {e}")

    if "result_img" in st.session_state:
        st.markdown("---")
        st.subheader("🎨 Curated Style Guide")
        st.markdown(st.session_state["result_img"])
        
        st.markdown("### 🖼️ Visual Outfit Inspiration & Pairings")
        img_col1, img_col2, img_col3 = st.columns(3)
        with img_col1:
            st.image(FALLBACK_IMAGES[0], caption="Recommended Footwear", use_container_width=True)
        with img_col2:
            st.image(FALLBACK_IMAGES[1], caption="Matching Accessories", use_container_width=True)
        with img_col3:
            st.image(FALLBACK_IMAGES[2], caption="Complete Look Styling", use_container_width=True)

# --- TAB 2: TEXT PROMPT MODE ---
with tab2:
    st.subheader("Ask Your AI Stylist for Text & Visual Fits")
    user_query = st.text_area("Describe what you want to wear (e.g., 'A chic pastel lehenga for a daytime summer wedding')")
    occasion_2 = st.selectbox("Select Occasion", ["Festive / Traditional Function", "Casual Day Out", "Evening Dinner / Party", "Work / Formal Event"], key="occ_2")

    if st.button("✨ Get Outfit & Visuals", key="btn_text"):
        if user_query.strip():
            with st.spinner("Generating outfit recommendations and inspiration..."):
                try:
                    text_result = get_text_styling_advice(user_query, occasion_2)
                    st.session_state["result_text"] = text_result
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a styling question first.")

    if "result_text" in st.session_state:
        st.markdown("---")
        st.subheader("🌟 Stylist Recommendations")
        st.markdown(st.session_state["result_text"])
        
        st.markdown("### 🖼️ Visual Inspiration Lookbook")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.image(FALLBACK_IMAGES[2], caption="Style Inspiration 1", use_container_width=True)
        with t_col2:
            st.image(FALLBACK_IMAGES[3], caption="Style Inspiration 2", use_container_width=True)
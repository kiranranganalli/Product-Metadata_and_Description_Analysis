import streamlit as st
import requests

st.set_page_config(page_title="Product Metadata Extractor", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #f5f5f5;
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding-top: 6vh !important;
}
.main-title {
    text-align: center;
    font-size: 3.5rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.1em;
}
.sub-title {
    text-align: center;
    font-size: 1.1rem;
    color: #00adb5;
    margin-bottom: 2em;
}
.upload-box, .search-box {
    background-color: #0e1117;
    border-radius: 12px;
    padding: 1.5em;
}
.result-card {
    background: #11141a;
    border-radius: 12px;
    padding: 1.8em;
    width: 100%;
    color: #eaeaea;
    box-shadow: 0 0 8px rgba(0,0,0,0.2);
}
.result-key { color: #00adb5; font-weight: 600; }
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/ingest-image"
SEARCH_URL = "http://127.0.0.1:8000/products"

# --- Title ---
st.markdown('<div class="main-title">Product</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Metadata Extractor</div>', unsafe_allow_html=True)

if "image_mode" not in st.session_state:
    st.session_state.image_mode = False

# --- Upload Box ---
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a product image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    st.session_state.image_mode = True
else:
    st.session_state.image_mode = False

# --- Image Mode ---
if uploaded_file:
    col1, col2 = st.columns([1, 1.1])
    with col1:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=False, width=450)
    with col2:
        with st.spinner("🔍 Extracting metadata..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                data = response.json()
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown("<h4>📦 Extracted Product Metadata</h4>", unsafe_allow_html=True)
                for key, value in data.items():
                    st.markdown(f"<div><span class='result-key'>{key}</span>: {value}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error(f"❌ Error: {response.status_code}")

# --- Search Mode ---
elif not st.session_state.image_mode:
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    st.subheader("🔎 Search Existing Products")
    query = st.text_input("Enter product name, brand, or keyword", "")
    if st.button("Search"):
        if query.strip():
            try:
                res = requests.get(f"{SEARCH_URL}?q={query}")
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        for p in data:
                            st.markdown(f"**{p['name']}** — {p.get('brand', 'Unknown')}")
                    else:
                        st.info("No products found.")
                else:
                    st.error("Failed to fetch product list.")
            except Exception as e:
                st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

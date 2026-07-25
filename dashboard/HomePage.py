import streamlit as st
from pathlib import Path

#stetting preferred padding
st.markdown("""
<style>

/* Remove default Streamlit padding */
.block-container{
    padding-top:0rem;
    padding-left:0rem;
    padding-right:0rem;
    padding-bottom:0rem;
}

/* Remove the top blank space */
[data-testid="stHeader"]{
    background:transparent;
}

/* Make the app use the full width */
[data-testid="stAppViewContainer"]{
    padding:0;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="AI-Powered Customer Intelligence Platform",
    
    layout = "wide",
    initial_sidebar_state = "collapsed"
)



def load_css():
    css_file = Path(__file__).parent / "assets" / "style.css"

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

#navigation
st.markdown("""
<div class="navbar">

<div class="logo">
📊ProfitAI
</div>


</div>
""", unsafe_allow_html=True)

#hero section
st.markdown("""
<div class="hero">
<div class="hero-left">
<div class="h1_col">
<h1>
AI-Powered
<br class="brad">Global E-commerce Intelligence Platform<br></h1>
<div>
<div class="h_col_p">
<p class="h_col">
Make smarter business decisions with AI. Predict profitability, identify high-value markets, forecast future growth, and discover where your next expansion should be.
</p></div>
</div>
</div>
""", unsafe_allow_html=True)

#features
st.markdown("""
<h2 class="wy">
Why Choose ProfitAI?
</h2>
""", unsafe_allow_html=True)

st.markdown('<div class="features-section">', unsafe_allow_html=True)


#cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
    <div>fff</div>
        <h3>Monitor your business at a glance</h3>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="feature-card">
        <div>fff</div>
        <h3>Predict profitability before decisions are made</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div>fff</div>
        <h3>Plan for the future with confidence</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div>fff</div>
        <h3>Discover your next high-growth market</h3>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div>fff</div>
        <h3>Focus on products that drive growth</h3>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div>fff</div>
        <h3>Turn analytics into business strategy</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)



#footer
st.markdown("""
<hr>
<center style="color:#2A0B45; font-size:18px; font-weight:500;">
Designed by <strong>Segun A.</strong><br><br>
</center>
""", unsafe_allow_html=True)






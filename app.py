import streamlit as st
	import logic
	import auth
	
	st.set_page_config(page_title="The Meta-Forge", page_icon="⚒️", layout="wide")
	# REPLACE THIS WITH YOUR GUMROAD PERMALINK
	GUMROAD_PERMALINK = "meta-forge" 
	
	# --- SIDEBAR ---
	st.sidebar.title("🔐 The Gatehouse")
	api_key = st.sidebar.text_input("Gemini API Key", type="password")
	license_key = st.sidebar.text_input("License Key", type="password")
	
	st.sidebar.markdown("---")
	st.sidebar.markdown("### How to use")
	st.sidebar.info("1. Enter your keys.\n2. Describe your dream app.\n3. The Forge builds it.")
	
	# --- MAIN ---
	st.title("⚒️ The Meta-Forge")
	st.subheader("Turn Ideas into Deployable Software instantly.")
	
	# Auth Check
	is_auth, msg = auth.verify_license_key(GUMROAD_PERMALINK, license_key)
	if not is_auth:
	    st.warning("🔒 " + msg)
	    st.stop()
	
	if not api_key:
	    st.warning("⚠️ Please enter your Gemini API Key.")
	    st.stop()
	
	# Input
	col1, col2 = st.columns([1, 1])
	
	with col1:
	    st.markdown("### 1. The Blueprint")
	    user_idea = st.text_area("Describe the app you want to build:", height=300, placeholder="e.g., A Bitcoin ROI calculator that fetches live prices and lets me input my purchase date.")
	    
	    generate_btn = st.button("Ignite the Forge", type="primary")
	
	with col2:
	    st.markdown("### 2. The Artifact")
	    if generate_btn and user_idea:
	        with st.spinner("Forging your application..."):
	            # Generate Code
	            code = logic.generate_python_app(api_key, user_idea)
	            reqs = logic.generate_requirements(code)
	            
	            # Display Code
	            st.code(code, language="python")
	            
	            # Download Buttons
	            st.download_button(
	                label="📥 Download app.py",
	                data=code,
	                file_name="app.py",
	                mime="text/x-python"
	            )
	            
	            st.download_button(
	                label="📥 Download requirements.txt",
	                data=reqs,
	                file_name="requirements.txt",
	                mime="text/plain"
	            )
	            
	            st.success("Forge Complete. You can now deploy this code.")
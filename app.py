import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "https://your-fastapi-space.hf.space")

st.title("📢 News Sentiment & Hindi Speech Generator")

company = st.text_input("Enter a company name:", "Tesla")

if st.button("Fetch News"):
    with st.spinner("Fetching news..."):
        try:
            response = requests.get(f"{API_URL}/news/{company}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])

                if not articles:
                    st.error("No articles found.")
                else:
                    st.subheader("📰 News Articles & Sentiments")
                    for news in articles:
                        st.markdown(f"### [{news['title']}]({news['url']})")
                        sentiment = requests.get(f"{API_URL}/sentiment/{news['title']}").json()
                        st.write(f"**Sentiment:** {sentiment['sentiments'][0]['sentiment']['sentiment']}")
                        st.write("---")

                    if articles:
                        text_to_convert = " ".join([news["title"] for news in articles[:3]])  
                        tts_response = requests.get(f"{API_URL}/tts/?text={text_to_convert}", timeout=10)

                        if tts_response.status_code == 200:
                            st.audio("output.mp3")
                        else:
                            st.error("TTS generation failed.")
            else:
                st.error(f"API request failed! Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Error: {e}")

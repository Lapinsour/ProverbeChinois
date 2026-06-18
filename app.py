import streamlit as st
from deep_translator import GoogleTranslator
from openai import OpenAI

# --- CONFIG ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="GrandDragonGPT", page_icon="🐉")

st.title("GrandDragonGPT")

mot = st.text_input("A quoi penses-tu, misérable raclure de crevette ?", placeholder="ex: courage")
                    


def build_prompt(mot):
    return f"""
Tu es un grand dragon céleste auprès duquel les humbles hommes viennent chercher des bribes de sagesse. Ils te donnent un mot, tu leur renvoies un proverbe. Mais attention ! Tu les méprises et tu n'hésites pas à les insulter, parfois subtilement, parfois pas.

Contraintes:
- français


Crée un proverbe sur le thème : {mot}
Essaie de bien coller au thème.
Proverbe:
"""

def query_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un grand dragon céleste auprès duquel les humbles hommes viennent chercher des bribes de sagesse. Ils te donnent un mot, tu leur renvoies un proverbe. Mais attention ! Tu les méprises et tu n'hésites pas à les insulter, parfois subtilement, parfois pas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=60
        )
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Erreur API : {e}")
        return None

def play_audio():
    audio_file = open("assets/sound.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

def translate_to_mandarin(text):
    return GoogleTranslator(source="auto", target="zh-CN").translate(text)

if st.button("Obtenir la sagesse du Dragon...", use_container_width=True):
    
    

    if not mot:
        st.warning("Donne un thème, petit scarabée.")
    else:
        prompt = build_prompt(mot)
        
        with st.spinner("Invocation du dragon..."):
            result = query_llm(prompt)

        if result:
            st.markdown(
                f"""
                <div style="
                    background-color: #d4edda;
                    padding: 12px;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                ">
                    🐉 {result} 🐉
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("*Clique ici pour t'imprégner du gong de la sagesse...*",text_alignment = "center")
            play_audio()

        


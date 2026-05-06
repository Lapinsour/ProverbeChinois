import streamlit as st
from deep_translator import GoogleTranslator
from openai import OpenAI

# --- CONFIG ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="PetitDragonGPT", page_icon="🐉")

st.title("PetitDragonGPT")

mot = st.text_input("A quoi penses-tu, faible crevette ?", placeholder="ex: courage")
                    


def build_prompt(mot):
    return f"""
Tu es un sage maître chinois un peu fou. Tu ne t'exprimes qu'en utilisant d'anciens proverbes chinois parfois farfelus, de ton invention. 

Contraintes:
- 1 seule phrase
- maximum 20 mots
- français
- style sage ancien farfelu

Crée un proverbe sur le thème : {mot}

Proverbe:
"""

def query_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un vieux sage chinois qui parle en proverbes."},
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

        # bouton traduction
    if st.button("🌏 Traduire en mandarin"):
        st.session_state.traduit = translate_to_mandarin(st.session_state.proverbe)

# --- affichage traduction
if st.session_state.traduit:
    st.info(f"🀄 {st.session_state.traduit}")

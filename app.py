import streamlit as st
import streamlit.components.v1 as components
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

if st.button("Obtenir la sagesse du Dragon...", use_container_width=True):
    
    

    if not mot:
        st.warning("Donne un thème, petit scarabée.")
    else:
        prompt = build_prompt(mot)
        st.audio(open("dragon.mp3", "rb").read())
        with st.spinner("Invocation du dragon..."):
            result = query_llm(prompt)

        if result:
            st.success("✨ Sagesse reçue")
            st.write(result)

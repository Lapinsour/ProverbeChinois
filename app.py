import streamlit as st
import requests

# --- CONFIG ---
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
}

# --- UI ---
st.set_page_config(page_title="PetitDragonGPT", page_icon="💬")

st.title("PetitDragonGPT")


# --- INPUT ---
mot = st.text_input("A quoi penses-tu, faible crevette ?", placeholder="ex: courage")



# --- PROMPT BUILDER ---
def build_prompt(mot):
    return f"""
Rôle: Tu es un générateur de proverbes chinois.

Contraintes:
- 1 seule phrase
- maximum 20 mots
- français
- pas d’explication

Ecris comme si tu étais un vieux sage chinois riche en proverbes traditionnels.
Ecris un proverbe sur le thème: {mot}

Message:
"""

# --- API CALL ---
def query_llm(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 60,
                    "temperature": 0.7
                }
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data[0]["generated_text"]

        return None

    except requests.exceptions.RequestException:
        return None

# --- ACTION ---
if st.button("Obtenir la sagesse du Dragon vénérable...", use_container_width=True):

    if not mot:
        st.warning("Veuillez saisir un thème, petit scarabée.")
    else:
        prompt = build_prompt(mot)

        with st.spinner("J'interroge le dragon vénérable..."):
            result = query_llm(prompt)

        if result:
            st.success("✨ Résultat")
            st.write(result.strip())
        else:
            st.error("Erreur lors de la génération (quota ou API).")


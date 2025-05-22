import streamlit as st
from tabs.salary import show_salary_tab
from tabs.SU.su_tab import show_su_tab
from tabs.household import show_household_tab
from tabs.food import show_food_tab
from tabs.chatbot import show_chatbot_tab


# -------- Intro-fanen med hele projektets overblik --------
def show_intro_tab():
    st.title("📌 Projektintroduktion")
    st.subheader("Inflationens påvirkning på løn, SU, mad og husholdning")

    st.markdown("---")
    st.markdown("### 🎯 Projektformål")
    st.markdown("""
    Et Business Intelligence-projekt, der undersøger hvordan inflationen har påvirket:

    - 📊 **Lønudviklingen** (mænd, kvinder og sektorer)
    - 🎓 **SU-modtageres økonomi** og deres købekraft
    - 🛒 **Madvarepriser** og deres stigning
    - 🏠 **Husholdningsudgifter** og deres ændring over tid

    Projektet fokuserer på perioden **2013–2023**, hvor inflationen har påvirket mange danskeres privatøkonomi.
    """)

    st.markdown("---")
    st.markdown("### ❓ Problemstilling")
    st.markdown("""
    - Følger løn og SU med inflationen og prisudviklingen?
    - Hvilke grupper mister reelt købekraft?
    - Er der ubalancer mellem køn, sektorer eller befolkningsgrupper?
    """)

    st.markdown("---")
    st.markdown("### 🔍 Forskningsspørgsmål")
    st.markdown("""
    - Hvordan har **reallønnen** udviklet sig i Danmark?
    - Har **SU-modtagere** mistet købekraft over tid?
    - Hvilke madvarer er steget mest i pris?
    - Hvordan påvirkes en gennemsnitlig **husholdning** økonomisk?
    """)

    st.markdown("---")
    st.markdown("### 🧪 Hypoteser")
    st.markdown("""
    - Løn og SU er **ikke steget i samme takt som inflation og priser**
    - Mad- og husholdningsudgifter er blevet **relativt dyrere**
    - **Kvinder og offentligt ansatte** er blandt de mest økonomisk pressede
    """)

    st.markdown("---")
    st.markdown("### 💡 Løsning: Vores Streamlit BI-løsning")
    st.markdown("""
    - Interaktive faner med data og visualiseringer:
        - **Løn**: Timefortjeneste fordelt på køn, sektor og år
        - **SU**: Udvikling i støttebeløb og sammenligning med leveomkostninger
        - **Mad**: Udvikling i priser på udvalgte varer
        - **Husholdning**: Overslag på budget og udgiftsniveau over tid
        - **Chatbot**: Mulighed for at stille spørgsmål om inflation og økonomi

    - Den forventede løsning er en brugervenlig, interaktiv BI-applikation i Streamlit, som visualiserer og forklarer udviklingen i realløn og inflation.

    - Den giver mulighed for at udforske samfundsøkonomiske trends, foretage sammenligninger og få bedre indsigt i leveomkostninger.

    - Løsningen kan bidrage til bedre beslutninger for:
        - 📌 **Beslutningstagere og politikere** (f.eks. ifm. reformer og tiltag)
        - 🧾 **Borgere og forbrugere** (som ønsker overblik og viden)
        - 🧑‍🏫 **Studerende og undervisere** (til analyse og læring)
        - 🧑‍💼 **Fagforeninger og arbejdsgivere** (til lønforhandling og vurdering af realindkomst)
    """)

    st.markdown("---")
    st.markdown("### 👥 Målgrupper")
    st.markdown("""
    - 📌 **Beslutningstagere og politikere**  
    - 🧑‍🏫 **Undervisere og studerende**  
    - 🧾 **Borgere og forbrugere**  
    - 🧑‍💼 **Fagforeninger og arbejdsgivere**
    """)

    st.success("➡️ Brug fanerne i toppen til at udforske løn, SU, madpriser og husholdningsdata.")
# ------------------------------------------------------------------

# --------- App Layout med faner ---------
st.set_page_config(page_title="Inflation & Økonomi", layout="wide")
st.title("📊 BI Projekt – Inflationens Samfundsmæssige Påvirkning")

tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["📌 Intro", "💼 Salary", "🎓 SU", "🛒 Food", "🏠 Household", "🤖 Chatbot"])

with tab0:
    show_intro_tab()
with tab1:
    show_salary_tab()
with tab2:
    show_su_tab()
with tab3:
    show_food_tab()
with tab4:
    show_household_tab()
with tab5:
    show_chatbot_tab()
    show_household_tab()

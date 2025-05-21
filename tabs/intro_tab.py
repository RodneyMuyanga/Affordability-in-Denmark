import streamlit as st

def show_intro_tab():
    st.title("📌 Projektintroduktion – Inflationens påvirkning på løn")

    st.subheader("🧠 Sprint 1: Problemformulering – Løn vs. Inflation")

    st.markdown("""
    ### 💼 Business Case og Problemformulering

    #### 🔍 Udfordring:
    Vi ønsker at undersøge, hvordan inflation har påvirket lønudviklingen i Danmark over det sidste årti, 
    og om lønningerne reelt har fulgt med de stigende forbrugerpriser. 
    Fokus er især på forskelle mellem mænd, kvinder og forskellige sektorer i perioden 2013–2023.

    #### 🤔 Hvorfor er det vigtigt?
    Løn er en central faktor for økonomisk stabilitet, og hvis den ikke følger med inflationen, mister lønmodtagere reelt købekraft.  
    Det påvirker levevilkår, lighed og samfundsøkonomisk trivsel.  
    Derfor er det vigtigt at analysere om – og hvordan – inflationen udhuler reallønnen, især for udsatte grupper.

    #### 🎯 Formål og Forskningsspørgsmål:
    Formålet er at give en datadrevet indsigt i lønudviklingen på tværs af køn og sektorer, 
    samt vurdere i hvilken grad lønningerne har holdt trit med inflationen.

    **Forskningsspørgsmål:**
    - Hvordan har den standardberegnede timefortjeneste udviklet sig over tid for forskellige grupper?
    - Er der forskelle i lønudviklingen mellem mænd og kvinder?
    - Hvilke sektorer har oplevet den højeste/laveste lønvækst?

    #### 📌 Hypotese:
    Vi antager, at lønudviklingen ikke har holdt trit med inflationen i flere sektorer – særligt i offentlige stillinger og for kvinder.

    #### 💡 Forventet løsning:
    Projektet vil levere en interaktiv Streamlit-løsning, hvor brugeren kan udforske løndata over tid, opdelt på køn og sektorer, 
    og sammenholde det med inflation. Løsningen skal identificere tendenser og forskelle i realløn.

    #### 👥 Potentiel værdi og målgruppe:
    - **Politikere og fagforeninger** kan bruge indsigten til at forme løn- og ligestillingspolitik.
    - **Arbejdsgivere** kan benchmarke lønniveauer og sikre retfærdig kompensation.
    - **Borgere og studerende** får indsigt i deres egen lønudvikling og økonomiske forhold.
    """)

    st.info("➡️ Gå til fanen *Salary* for at udforske timefortjeneste fordelt på køn, sektor og årstal.")

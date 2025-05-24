import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def loadRentData(filepath):
    try:
      
        df = pd.read_excel(filepath, skiprows=2)

        df = df.drop(columns=[df.columns[0], df.columns[1]])

        df.rename(columns={df.columns[0]: "Region"}, inplace=True)

        df = df.dropna(subset=["Region"])

        df.columns = df.columns.astype(str).str.strip()

        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df.set_index("Region", inplace=True)

        return df
    except Exception as e:
        print(f"Fejl under indlæsning: {e}")
        return None


    
def plotRentData(df):
    fig, ax = plt.subplots()
    df.T.plot(marker='o', ax=ax)
    ax.set_title("Udvikling i huslejeindeks 2021 - 2024")
    ax.set_xlabel("Kvartal")
    ax.set_ylabel("Indeks (2021 = 100)")
    ax.legend(title="Region")
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.title("Huslejeindeks i Danmark – 2024 (Almene boliger)")

    df = loadRentData("Data/Rent/Huslejeindeks_2021-2024.xlsx")
    if df is not None:
        st.success("Data indlæst korrekt!")
        st.dataframe(df)

        st.subheader("Huslejeudvikling per region")
        plotRentData(df)
    else:
        st.error("Kunne ikke indlæse datafilen.")


#TEST
if __name__ == "__main__":
    main()

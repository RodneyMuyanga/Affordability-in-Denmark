import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def loadRentData(filepath):
    try:
        df = pd.read_csv(filepath, encoding='utf-8', header=None)

        df = df.drop(columns=[0, 1])
        df.rename(columns={2: 'Region'}, inplace=True)
        kvartaler = ['2024K1', '2024K2', '2024K3', '2024K4']
        df.columns = ['Region'] + kvartaler

        df.set_index('Region', inplace=True)

       # df.colums = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Fejl under indlæsning: {e}")
        return None
    
def plotRentData(df):
    fig, ax = plt.subplots()
    df.T.plot(marker='o', ax=ax)
    ax.set_title("Udvikling i huslejeindeks i 2024")
    ax.set_xlabel("Kvartal")
    ax.set_ylabel("Indeks (2021 = 100)")
    ax.legend(title="Region")
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.title("Huslejeindeks i Danmark – 2024")

    df = loadRentData("Huslejeindeks_2024.csv")
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

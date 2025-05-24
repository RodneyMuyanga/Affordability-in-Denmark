import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


def forecast_rent(df):
    st.subheader("📈 Forecast Rent Index (up to 2035)")

    region = st.selectbox("Select region to forecast:", df.index.tolist())
    future_quarters = st.slider("Select number of quarters to forecast (max = 44 for 11 years)", 4, 44, 12)

    df_T = df.T.reset_index().rename(columns={"index": "Kvartal"})
    df_T["Kvartal_nr"] = range(1, len(df_T) + 1)

    y = df_T[region].values
    X = df_T["Kvartal_nr"].values.reshape(-1, 1)

    #polynomiel regression (grad 3 for kurve)
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)

    # Forudsig fremtidige kvartaler
    future_X = np.array(range(len(X) + 1, len(X) + future_quarters + 1)).reshape(-1, 1)
    future_X_poly = poly.transform(future_X)
    forecasted = model.predict(future_X_poly)

    full_X = np.concatenate([X, future_X])
    full_y = np.concatenate([y, forecasted])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(full_X, full_y, marker="o", label="Actual + Forecast")
    ax.axvline(len(X), color="red", linestyle="--", label="Forecast starts here")
    ax.set_xlabel("Quarter Number")
    ax.set_ylabel("Rent Index")
    ax.set_title(f"Forecast of Rent Index – {region}")
    ax.legend()
    st.pyplot(fig)

    last_q = df_T["Kvartal"].iloc[-1]
    last_year = int(last_q[:4])
    last_k = int(last_q[-1])

    kvartaler = []
    for i in range(1, future_quarters + 1):
        k = (last_k + i - 1) % 4 + 1
        y = last_year + (last_k + i - 1) // 4
        kvartaler.append(f"{y}K{k}")

    forecast_df = pd.DataFrame({"Kvartal": kvartaler, "Forecast": forecasted})
    forecast_df["Forecast"] = forecast_df["Forecast"].round(2)

    st.markdown("""---""")
    st.subheader("Forecasted values:")
    st.dataframe(forecast_df, use_container_width=True)

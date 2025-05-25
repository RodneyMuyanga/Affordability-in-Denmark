import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
from tabs.food_presentation.food_clean_data import load_and_clean          
from tabs.food_presentation.food_clean_data_expenditure import load_and_clean_expenditure 

def show_forecast():

    st.header("🔮 Food Prices & Expenditure Forecasting (Machine Learning)")

    st.markdown("""
    In this section, we build and evaluate a **Random Forest regression** model to predict
    next-period household expenditure on each food category, based on:
    1. This period’s **percentage price change**  
    2. Last period’s **actual expenditure**  
    3. The **calendar year**  
    Afterwards, we generate a **10-year forecast** of the *overall* average household expenditure  
    using **Holt–Winters exponential smoothing**.
    """)

    # 1) Load and merge data
    _, price_df, price_years = load_and_clean()
    cons_long, exp_years     = load_and_clean_expenditure()

    # melt price to long form
    price_long = price_df.melt(
        id_vars="Category", 
        var_name="Year", 
        value_name="PriceChange"
    )
    price_long["Year"] = price_long["Year"].astype(int)

    # cons_long is already long
    cons_long["Year"] = cons_long["Year"].astype(int)

    # merge on Category + Year
    df = price_long.merge(cons_long, on=["Category","Year"], how="inner")

    # 2) Feature engineering: add PrevExp and NextExp
    df = df.sort_values(["Category","Year"])
    df["PrevExp"] = df.groupby("Category")["Expenditure"].shift(1)
    df["NextExp"] = df.groupby("Category")["Expenditure"].shift(-1)
    df = df.dropna(subset=["PrevExp","NextExp"])

    # 3) Define features X and target y
    X = df[["PriceChange","PrevExp","Year"]]
    y = df["NextExp"]

    # 4) Cross-validated RMSE
    st.markdown("### Model Evaluation")
    st.markdown("""
    We use **3-fold time-series cross-validation** to measure out-of-sample performance.
    The primary metric is **RMSE (root mean squared error)** in DKK.
    """)
    tscv = TimeSeriesSplit(n_splits=3)
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    scores = cross_val_score(
        model, X, y, 
        cv=tscv, 
        scoring="neg_root_mean_squared_error"
    )
    rmse = -scores.mean()
    st.write(f"📈 Cross-validated RMSE: {rmse:.2f} DKK")

    # 5) Train final model
    model.fit(X, y)

    # 6) Show feature importances
    importances = model.feature_importances_
    feat_imp = pd.Series(importances, index=X.columns).sort_values(ascending=False)
    st.markdown("### Feature Importance")
    st.markdown("""
    The Random Forest’s built-in feature importances tell us how much each input contributes
    to reducing prediction error:
    - **PrevExp:** Last period’s expenditure  
    - **PriceChange:** Year-over-year % change in price  
    - **Year:** Captures any linear trend in the data  
    """)
    st.table(feat_imp.to_frame("Importance"))

    # 7) Plot actual vs. predicted
    y_pred = model.predict(X)
    fig, ax = plt.subplots(figsize=(4, 3), dpi=120)
    ax.scatter(y, y_pred, s=15, alpha=0.7)
    lims = [min(y.min(), y_pred.min()), max(y.max(), y_pred.max())]
    ax.plot(lims, lims, "--", color="grey", linewidth=1)
    ax.set_xlabel("Actual Next-Period Expenditure", fontsize=8)
    ax.set_ylabel("Predicted Next-Period Expenditure", fontsize=8)
    ax.set_title("Predicted vs. Actual Expenditure", fontsize=9)
    ax.tick_params(axis="both", labelsize=6)
    st.pyplot(fig, use_container_width=False)
    st.markdown("### Predicted vs. Actual Next-Period Expenditure")
    st.markdown("""
    A scatterplot of **actual** vs. **predicted** next-period expenditure.  
    • The dashed **45° line** marks perfect predictions.  
    • Points close to the line indicate accurate forecasts.  
    """)

    # ────────────────────────────────────────────────────────────────────
    # 8) 10-Year Forecast of Average Household Expenditure
    st.markdown("### 10-Year Forecast of Average Household Expenditure")
    st.markdown("""
    We aggregate *all categories* to compute the **annual average expenditure**, then fit a
    **Holt–Winters exponential smoothing** model (additive trend, no seasonality) on the historic
    series and forecast the next 10 years.
    """)

    # a) Build historic annual series
    ts = cons_long.groupby("Year")["Expenditure"].mean().sort_index()

    # b) Fit Holt–Winters (additive trend)
    hw = ExponentialSmoothing(ts, trend="add", seasonal=None)
    fit = hw.fit()

    # c) Forecast next 10 years
    steps = 10
    raw_forecast = fit.forecast(steps=steps)

    # d) Re-index to real year labels
    last_year    = ts.index.max()
    future_years = list(range(last_year+1, last_year+steps+1))
    raw_forecast.index = future_years

    # e) Matplotlib plot with integer xticks
    fig, ax = plt.subplots(figsize=(6, 3), dpi=120, constrained_layout=True)
    ax.plot(raw_forecast.index, raw_forecast.values, "-o", color="royalblue", label="Forecast")
    ax.set_title("🔮 10-Year Forecast of Average Expenditure", fontsize=12)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Average Expenditure (DKK)", fontsize=10)
    ax.set_xticks(future_years)
    ax.tick_params(axis="x", labelrotation=0, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper left")
    st.pyplot(fig, use_container_width=True)

    # f) Show numeric values
    st.write(
        "Forecast next 10 years:",
        {str(year): float(raw_forecast.loc[year]) for year in future_years}
    )

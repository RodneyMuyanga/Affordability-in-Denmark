import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.stats import zscore
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

@st.cache_data
def load_and_clean_data(file_stipend, file_antal, file_aarsvaerk, file_home, file_not_home):
    def clean_df(df):
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(r'\n', '', regex=True)
        df.columns = df.columns.str.replace(r'[^\x00-\x7F]+', '', regex=True)
        df.columns = df.columns.str.replace(' ', '_')
        df.rename(columns={df.columns[0]: 'Aar'}, inplace=True)
        df = df[pd.to_numeric(df['Aar'], errors='coerce').notna()]
        df['Aar'] = df['Aar'].astype(int)
        return df

    def clean_living_situation(df):
        df = clean_df(df)
        df['Aar'] = pd.to_numeric(df['Aar'], errors='coerce')
        df = df[['Aar', df.columns[1]]].rename(columns={df.columns[1]: 'Count'})
        return df

    stipend_df = clean_df(pd.read_excel(file_stipend))
    antal_df = clean_df(pd.read_excel(file_antal))
    aarsvaerk_df = clean_df(pd.read_excel(file_aarsvaerk))
    home_df = clean_living_situation(pd.read_excel(file_home))
    not_home_df = clean_living_situation(pd.read_excel(file_not_home))

    stipend_df.rename(columns={
        'Stipendie_(mio._kr)': 'Stipendie',
        '-_Heraf_forsrgertillg_(mio._kr.)': 'Forsorger_tillaeg',
        '-_Heraf_handicaptillg_(mio._kr.)': 'Handicap_tillaeg',
        'Ln_(mio._kr)_*': 'Laan',
        '-_Heraf_slutln_(mio._kr)': 'Slutlaan',
        '-_Heraf_forsrgerln_(mio._kr.)': 'Forsorgerlaan'
    }, inplace=True)

    antal_df.rename(columns={
        'Antal_stttemodtagere': 'Antal_stoettemodtagere',
        '-_Heraf_antal_stttemodtagere_med_handicaptillg': 'Antal_handicap_tillaeg',
        '-_Heraf_antal_stttemodtagere_med_forsrgertillg': 'Antal_forsorger_tillaeg',
        'Antal_lntagere': 'Antal_laan_tagere',
        '-_Heraf_antal_lntagere_med_slutln': 'Antal_slutlaan',
        '-_Heraf_antal_lntagere_med_forsrgerln': 'Antal_forsorgerlaan'
    }, inplace=True)

    merged_df = stipend_df.merge(antal_df, on='Aar').merge(aarsvaerk_df, on='Aar')

    for col in ['Stipendie', 'Forsorger_tillaeg', 'Handicap_tillaeg', 'Laan', 'Slutlaan', 'Forsorgerlaan']:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce') * 1_000_000

    merged_df['SU_pr_student'] = merged_df['Stipendie'] / merged_df['Antal_stoettemodtagere']
    merged_df['SU_pr_handicap'] = merged_df['Handicap_tillaeg'] / merged_df['Antal_handicap_tillaeg']
    merged_df['SU_pr_forsorger'] = merged_df['Forsorger_tillaeg'] / merged_df['Antal_forsorger_tillaeg']

    # Advanced metrics
    merged_df['SU_to_loan_ratio'] = merged_df['Stipendie'] / (merged_df['Laan'] + 1)
    merged_df['Pct_handicap'] = merged_df['Antal_handicap_tillaeg'] / merged_df['Antal_stoettemodtagere']
    merged_df['Pct_forsorger'] = merged_df['Antal_forsorger_tillaeg'] / merged_df['Antal_stoettemodtagere']

    merged_df = merged_df[merged_df['Aar'] >= 2000]

    return merged_df, home_df, not_home_df

def remove_outliers(df, cols, z_thresh=3):
    z_scores = np.abs(zscore(df[cols], nan_policy='omit'))
    mask = (z_scores < z_thresh).all(axis=1)
    return df[mask]

def analyze_missing_values(df):
    missing_summary = df.isnull().sum()
    missing_percent = (missing_summary / len(df)) * 100
    return pd.DataFrame({'Missing Values': missing_summary, 'Percent': missing_percent})

def show_data_quality_checks(df):
    if st.checkbox("Show missing value analysis"):
        st.subheader("Missing Value Summary")
        st.dataframe(analyze_missing_values(df))
    if st.checkbox("Remove outliers (Z-score method)"):
        cols = ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']
        df = remove_outliers(df, cols)
        st.success("Outliers removed.")
    return df

# The rest of your analysis functions (unchanged)
# ... [plot_line_chart, show_conclusions, plot_boxplot, show_summary_stats, etc.]

# Update show_su_tab() to include show_data_quality_checks
def show_su_tab():
    st.title("SU per Student Analysis (2000–2024)")

    file_stipend = 'Data/SU/SU stipendier og lån (mio. kr.).xlsx'
    file_antal = 'Data/SU/Antal støttemodtagere og låntagere.xlsx'
    file_aarsvaerk = 'Data/SU/Støtteårsværk.xlsx'
    file_home = 'Data/SU/students_living_at_home.xlsx'
    file_not_home = 'Data/SU/students_not_living_at_home.xlsx'

    df, home_df, not_home_df = load_and_clean_data(file_stipend, file_antal, file_aarsvaerk, file_home, file_not_home)

    year_min, year_max = int(df['Aar'].min()), int(df['Aar'].max())
    year_range = st.slider('Select year range:', year_min, year_max, (year_min, year_max))
    df_filtered = df[(df['Aar'] >= year_range[0]) & (df['Aar'] <= year_range[1])]

    # Apply data quality checks
    df_filtered = show_data_quality_checks(df_filtered)

    if st.checkbox("Show raw data"):
        st.dataframe(df_filtered)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Line Plot", "Box Plot", "Summary Stats",
        "Regression", "Living Situation", "Conclusion"
    ])

    with tab1:
        st.subheader("Average SU per Student Over Time")
        plot_line_chart(df_filtered)
        show_conclusions(df_filtered)

    with tab2:
        st.subheader("Boxplot of SU Types")
        plot_boxplot(df_filtered)

    with tab3:
        st.subheader("Summary Statistics")
        show_summary_stats(df_filtered)

    with tab4:
        st.subheader("Linear Regression Prediction")
        linear_regression_prediction(df_filtered)

    with tab5:
        plot_living_situation(home_df, not_home_df, year_range)

    with tab6:
        show_final_conclusion(df_filtered)

def main():
    show_su_tab()

if __name__ == "__main__":
    main()

def plot_line_chart(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_filtered['Aar'], df_filtered['SU_pr_student'], marker='o', color='teal', label='Total SU per student')
    ax.plot(df_filtered['Aar'], df_filtered['SU_pr_handicap'], marker='o', color='orange', label='Handicap tillæg per student')
    ax.plot(df_filtered['Aar'], df_filtered['SU_pr_forsorger'], marker='o', color='purple', label='Forsørger tillæg per student')
    ax.set_xlabel('Year')
    ax.set_ylabel('Amount (DKK)')
    ax.set_title('Average SU per Student Over Time')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    st.pyplot(fig)

def show_conclusions(df_filtered):
    st.markdown("**Conclusions:**")
    st.write(f"Average SU per student over selected years: {df_filtered['SU_pr_student'].mean():,.0f} DKK")
    st.write(f"Average Handicap tillæg per eligible student: {df_filtered['SU_pr_handicap'].mean():,.0f} DKK")
    st.write(f"Average Forsørger tillæg per eligible student: {df_filtered['SU_pr_forsorger'].mean():,.0f} DKK")

def plot_boxplot(df_filtered):
    data = pd.melt(df_filtered,
                   id_vars='Aar',
                   value_vars=['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger'],
                   var_name='Type',
                   value_name='Amount')
    type_order = ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']
    labels = ['Total SU', 'Handicap Tillæg', 'Forsørger Tillæg']
    data['Type'] = pd.Categorical(data['Type'], categories=type_order, ordered=True)
    data['Type'] = data['Type'].cat.rename_categories(labels)

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.boxplot(x='Aar', y='Amount', hue='Type', data=data, ax=ax, palette='Set2')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title('Distribution of SU Types per Year')
    fig.tight_layout()
    st.pyplot(fig)

    if st.checkbox("Show boxplot data summary"):
        st.dataframe(data.groupby('Type')['Amount'].describe())

def show_summary_stats(df_filtered):
    st.write(df_filtered[['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']].describe())

def linear_regression_prediction(df_filtered):
    future_year = st.selectbox("Select prediction year (2025–2035):", list(range(2025, 2036)))

    for col, label, color in zip(
        ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger'],
        ['Total SU per student', 'Handicap tillæg', 'Forsørger tillæg'],
        ['teal', 'orange', 'purple']
    ):
        X = df_filtered['Aar'].values.reshape(-1, 1)
        y = df_filtered[col].values

        model = LinearRegression()
        model.fit(X, y)
        pred = model.predict(np.array([[future_year]]))[0]

        st.write(f"📈 Predicted {label} for {future_year}: {pred:,.0f} DKK")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(df_filtered['Aar'], y, color=color)
        ax.plot(df_filtered['Aar'], model.predict(X), linestyle='--', color='black')
        ax.scatter(future_year, pred, color='red', marker='X', s=100)
        ax.set_title(f"Prediction of {label}")
        st.pyplot(fig)

def plot_living_situation(home_df, not_home_df, year_range):
    st.subheader("Students Living at Home vs Not at Home")
    try:
        combined = home_df.merge(not_home_df, on='Aar', suffixes=('_at_home', '_not_home'))
        combined = combined[(combined['Aar'] >= year_range[0]) & (combined['Aar'] <= year_range[1])]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(combined['Aar'], combined['Count_at_home'], marker='o', label='Living at Home', color='blue')
        ax.plot(combined['Aar'], combined['Count_not_home'], marker='o', label='Not Living at Home', color='green')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Students')
        ax.set_title('Student Living Situation Over Time')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        if st.checkbox("Show living situation data"):
            st.dataframe(combined)

        if st.checkbox("Show growth rates for living situations"):
            start, end = combined.iloc[0], combined.iloc[-1]
            total_years = end['Aar'] - start['Aar']
            for col in ['Count_at_home', 'Count_not_home']:
                start_val = start[col]
                end_val = end[col]
                growth = (end_val - start_val) / start_val
                cagr = (end_val / start_val) ** (1 / total_years) - 1
                st.write(f"📊 {col.replace('_', ' ').title()}:")
                st.write(f" - Total growth: {growth*100:.2f}%")
                st.write(f" - CAGR: {cagr*100:.2f}% per year")
    except Exception as e:
        st.error(f"⚠️ Could not process living situation data: {e}")

def show_final_conclusion(df_filtered):
    st.subheader("📘 Final Conclusion & Trends")

    def calculate_growth(col):
        start_year, end_year = df_filtered['Aar'].iloc[0], df_filtered['Aar'].iloc[-1]
        start_val, end_val = df_filtered[col].iloc[0], df_filtered[col].iloc[-1]
        n_years = end_year - start_year
        if start_val > 0 and n_years > 0:
            cagr = (end_val / start_val) ** (1 / n_years) - 1
            total_growth = (end_val - start_val) / start_val
            return {
                'Start': start_val,
                'End': end_val,
                'CAGR': cagr,
                'Total Growth': total_growth
            }
        return None

    stats = {
        'SU_pr_student': calculate_growth('SU_pr_student'),
        'SU_pr_handicap': calculate_growth('SU_pr_handicap'),
        'SU_pr_forsorger': calculate_growth('SU_pr_forsorger')
    }

    for label, result in stats.items():
        if result:
            st.markdown(f"**{label.replace('_', ' ').title()}**")
            st.write(f"- From {result['Start']:,.0f} DKK to {result['End']:,.0f} DKK")
            st.write(f"- Total Growth: {result['Total Growth']*100:.2f}%")
            st.write(f"- Average Annual Growth: {result['CAGR']*100:.2f}% per year")

    max_growth_key = max(stats, key=lambda k: stats[k]['CAGR'] if stats[k] else -1)
    st.success(f"📈 The fastest growing SU component is **{max_growth_key.replace('_', ' ').title()}**.")

def plot_correlation_heatmap(df):
    st.subheader("Correlation Heatmap (Selected Features)")
    # Select fewer features, e.g., those numeric columns most relevant
    cols = ['Aar', 'Antal_stoettemodtagere', 'Antal_handicap_tillaeg', 'Antal_forsorger_tillaeg', 'SU_pr_student']
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax, annot_kws={"size": 10})
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    ax.set_title("Correlation Matrix (Selected Features)")
    st.pyplot(fig)


def train_test_model_analysis(df):
    st.subheader("Train/Test Split and Model Accuracy")

    # Selecting features and target — example using these SU columns and year
    feature_cols = ['Aar', 'Antal_stoettemodtagere', 'Antal_handicap_tillaeg', 'Antal_forsorger_tillaeg']
    target_col = 'SU_pr_student'

    # Clean dataset for NaNs in features or target
    df_clean = df.dropna(subset=feature_cols + [target_col])
    X = df_clean[feature_cols]
    y = df_clean[target_col]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    st.write(f"R² Score: {r2_score(y_test, predictions):.4f}")
    st.write(f"Mean Squared Error (MSE): {mean_squared_error(y_test, predictions):,.0f}")

    # Residual plot
    residuals = y_test - predictions
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(predictions, residuals, alpha=0.7)
    ax.axhline(0, color='red', linestyle='--')
    ax.set_xlabel("Predicted Values")
    ax.set_ylabel("Residuals")
    ax.set_title("Residual Plot")
    st.pyplot(fig)

    # Feature importance using coefficients
    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': model.coef_
    }).sort_values(by='Coefficient', key=abs, ascending=False)
    st.subheader("Feature Importance (Linear Regression Coefficients)")
    st.dataframe(coef_df)

def show_su_tab():
    st.title("SU per Student Analysis (2000–2024)")

    file_stipend = 'Data/SU/SU stipendier og lån (mio. kr.).xlsx'
    file_antal = 'Data/SU/Antal støttemodtagere og låntagere.xlsx'
    file_aarsvaerk = 'Data/SU/Støtteårsværk.xlsx'
    file_home = 'Data/SU/students_living_at_home.xlsx'
    file_not_home = 'Data/SU/students_not_living_at_home.xlsx'

    df, home_df, not_home_df = load_and_clean_data(file_stipend, file_antal, file_aarsvaerk, file_home, file_not_home)

    year_min, year_max = int(df['Aar'].min()), int(df['Aar'].max())
    year_range = st.slider('Select year range:', year_min, year_max, (year_min, year_max))
    df_filtered = df[(df['Aar'] >= year_range[0]) & (df['Aar'] <= year_range[1])]

    # Apply data quality checks
    df_filtered = show_data_quality_checks(df_filtered)

    if st.checkbox("Show raw data"):
        st.dataframe(df_filtered)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Line Plot", "Box Plot", "Summary Stats",
        "Regression", "Model Analysis", "Living Situation", "Conclusion"
    ])

    with tab1:
        st.subheader("Average SU per Student Over Time")
        plot_line_chart(df_filtered)
        show_conclusions(df_filtered)

    with tab2:
        st.subheader("Boxplot of SU Types")
        plot_boxplot(df_filtered)

    with tab3:
        st.subheader("Summary Statistics")
        show_summary_stats(df_filtered)

    with tab4:
        st.subheader("Linear Regression Prediction")
        linear_regression_prediction(df_filtered)

    with tab5:
        plot_correlation_heatmap(df_filtered)
        train_test_model_analysis(df_filtered)

    with tab6:
       plot_living_situation(home_df, not_home_df, year_range)

    with tab7:
        show_final_conclusion(df_filtered)


def main():
    show_su_tab()

if __name__ == "__main__":
    main()
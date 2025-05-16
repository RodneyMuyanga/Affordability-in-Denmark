import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

@st.cache_data
def load_and_clean_data(file_stipend, file_antal, file_aarsvaerk):
    def clean_df(df):
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(r'\n', '', regex=True)
        df.columns = df.columns.str.replace(r'[^\x00-\x7F]+', '', regex=True)
        df.columns = df.columns.str.replace(' ', '_')
        df.rename(columns={df.columns[0]: 'Aar'}, inplace=True)
        df = df[pd.to_numeric(df['Aar'], errors='coerce').notna()]
        df['Aar'] = df['Aar'].astype(int)
        return df

    stipend_df = clean_df(pd.read_excel(file_stipend))
    antal_df = clean_df(pd.read_excel(file_antal))
    aarsvaerk_df = clean_df(pd.read_excel(file_aarsvaerk))

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
        'Antal_lntagere': 'Antal_lantaagere',
        '-_Heraf_antal_lntagere_med_slutln': 'Antal_slutlaan',
        '-_Heraf_antal_lntagere_med_forsrgerln': 'Antal_forsorgerlaan'
    }, inplace=True)

    merged_df = stipend_df.merge(antal_df, on='Aar').merge(aarsvaerk_df, on='Aar')

    for col in ['Stipendie', 'Forsorger_tillaeg', 'Handicap_tillaeg', 'Laan', 'Slutlaan', 'Forsorgerlaan']:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce') * 1_000_000

    merged_df['SU_pr_student'] = merged_df['Stipendie'] / merged_df['Antal_stoettemodtagere']
    merged_df['SU_pr_handicap'] = merged_df['Handicap_tillaeg'] / merged_df['Antal_handicap_tillaeg']
    merged_df['SU_pr_forsorger'] = merged_df['Forsorger_tillaeg'] / merged_df['Antal_forsorger_tillaeg']

    merged_df = merged_df[merged_df['Aar'] >= 2000]

    return merged_df


class SUAnalysis:
    def __init__(self):
        self.file_stipend = 'Data/SU/SU stipendier og lån (mio. kr.).xlsx'
        self.file_antal = 'Data/SU/Antal støttemodtagere og låntagere.xlsx'
        self.file_aarsvaerk = 'Data/SU/Støtteårsværk.xlsx'
        self.df = load_and_clean_data(self.file_stipend, self.file_antal, self.file_aarsvaerk)

    def filter_year_range(self, year_range):
        return self.df[(self.df['Aar'] >= year_range[0]) & (self.df['Aar'] <= year_range[1])]

    def show_raw_data(self, df_filtered):
        st.dataframe(df_filtered[['Aar', 'Stipendie', 'Antal_stoettemodtagere', 'SU_pr_student',
                                  'Handicap_tillaeg', 'Antal_handicap_tillaeg', 'SU_pr_handicap',
                                  'Forsorger_tillaeg', 'Antal_forsorger_tillaeg', 'SU_pr_forsorger']])

    def plot_line_su(self, df_filtered):
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

        st.markdown("**Conclusions:**")
        st.write(f"Average SU per student over selected years: {df_filtered['SU_pr_student'].mean():,.0f} DKK")
        st.write(f"Average Handicap tillæg per eligible student: {df_filtered['SU_pr_handicap'].mean():,.0f} DKK")
        st.write(f"Average Forsørger tillæg per eligible student: {df_filtered['SU_pr_forsorger'].mean():,.0f} DKK")

    def plot_box_su(self, df_filtered):
        data = pd.melt(df_filtered,
                       id_vars='Aar',
                       value_vars=['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger'],
                       var_name='Type',
                       value_name='Amount')

        type_order = ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']
        type_labels = ['Total SU per student', 'Handicap tillæg', 'Forsørger tillæg']
        data['Type'] = pd.Categorical(data['Type'], categories=type_order, ordered=True)
        data['Type'] = data['Type'].cat.rename_categories(type_labels)

        fig, ax = plt.subplots(figsize=(14, 7))
        sns.boxplot(x='Aar', y='Amount', hue='Type', data=data, ax=ax, palette='Set2')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_xlabel('Year')
        ax.set_ylabel('Amount (DKK)')
        ax.set_title('Distribution of SU per Student by Year')
        ax.legend(title='SU Type')
        fig.tight_layout()
        st.pyplot(fig)

        st.markdown("**Summary statistics for selected years:**")
        for t, label in zip(type_order, type_labels):
            mean_val = df_filtered[t].mean()
            st.write(f"{label}: Mean = {mean_val:,.0f} DKK")

    def show_summary_stats(self, df_filtered):
        st.subheader("Summary Statistics of SU per Student")
        st.write(df_filtered[['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']].describe())

    def linear_regression_prediction(self, df_filtered):
        st.subheader("Linear Regression Prediction")

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

            future_pred = model.predict(np.array([[future_year]]))[0]

            st.write(f"📈 **Predicted {label} for {future_year}:** {future_pred:,.0f} DKK")

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.scatter(df_filtered['Aar'], y, color=color, label='Actual')
            ax.plot(df_filtered['Aar'], model.predict(X), color='black', linestyle='--', label='Fit')
            ax.scatter(future_year, future_pred, color='red', label='Prediction', marker='X', s=100)
            ax.set_xlabel('Year')
            ax.set_ylabel('Amount (DKK)')
            ax.set_title(f'Prediction of {label} for {future_year}')
            ax.legend()
            ax.grid(True)
            fig.tight_layout()
            st.pyplot(fig)


def show_su_tab():
    st.title("SU per Student Analysis (2000–2024)")

    analysis = SUAnalysis()

    year_min, year_max = int(analysis.df['Aar'].min()), int(analysis.df['Aar'].max())
    year_range = st.slider('Select year range:', year_min, year_max, (year_min, year_max))

    df_filtered = analysis.filter_year_range(year_range)

    show_data = st.checkbox('Show raw data')
    if show_data:
        with st.expander("Raw Data (click to expand)"):
            analysis.show_raw_data(df_filtered)

    tabs = st.tabs(["Line Plot", "Box Plot", "Summary Stats", "Regression Prediction"])

    with tabs[0]:
        st.subheader("Average SU per Student Over Time")
        analysis.plot_line_su(df_filtered)

    with tabs[1]:
        st.subheader("Distribution of SU per Student by Year")
        analysis.plot_box_su(df_filtered)

    with tabs[2]:
        with st.expander("Summary Statistics (click to expand)"):
            analysis.show_summary_stats(df_filtered)

    with tabs[3]:
        analysis.linear_regression_prediction(df_filtered)


def main():
    show_su_tab()


if __name__ == "__main__":
    main()

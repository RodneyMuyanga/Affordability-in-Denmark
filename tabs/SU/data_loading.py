import pandas as pd
import numpy as np
from scipy.stats import zscore

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

def load_and_clean_data(file_stipend, file_antal, file_aarsvaerk, file_home, file_not_home):
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

def add_living_situation_metrics(home_df, not_home_df):
    # Merge living situation counts by year
    combined = home_df.merge(not_home_df, on='Aar', suffixes=('_home', '_not_home'))

    # Calculate total counts
    combined['Total'] = combined['Count_home'] + combined['Count_not_home']

    # Percent living at home and not at home
    combined['Pct_at_home'] = combined['Count_home'] / combined['Total']
    combined['Pct_not_home'] = combined['Count_not_home'] / combined['Total']

    # Year-over-year growth (%)
    combined['Growth_home'] = combined['Count_home'].pct_change() * 100
    combined['Growth_not_home'] = combined['Count_not_home'].pct_change() * 100

    return combined

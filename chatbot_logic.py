import os
import pandas as pd
from ollama import Client

# ----------------------------------
# Ekstraher indsigt fra løndata
# ----------------------------------
def extract_salary_insights():
    summaries = []
    folder_path = "Data/Salary/Stats all 13 - 23 salary"

    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_excel(file_path, sheet_name="LONS30", header=None)
                df = df.dropna(how="all").dropna(axis=1, how="all")
                df[2] = df[2].astype(str).str.strip()

                match_row = df[df[2].str.lower() == "standardberegnet timefortjeneste"]
                if not match_row.empty:
                    row_idx = match_row.index[0]
                    sectors = df.loc[2, 3:8].tolist()
                    values = df.loc[row_idx, 3:8].tolist()
                    year = file.split()[1].split('.')[0]

                    summary = f"In {year}, the average hourly wages by sector were: " + \
                              ", ".join([f"{s}: {v} DKK" for s, v in zip(sectors, values)])
                    summaries.append(summary)
            except Exception as e:
                summaries.append(f"Error reading {file}: {e}")
    return "\n".join(summaries)


# ----------------------------------
# Ekstraher indsigt fra maddata
# ----------------------------------
def extract_food_insights():
    folder = "Data/Food"
    summaries = []
    for filename in os.listdir(folder):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(folder, filename)
            try:
                df = pd.read_excel(filepath)
                summaries.append(f"📊 {filename}:\n{df.head(3).to_string(index=False)}")
            except Exception as e:
                summaries.append(f"❌ Error reading {filename}: {e}")
    return "\n".join(summaries)


# ----------------------------------
# Ekstraher indsigt fra SU-data
# ----------------------------------
def extract_su_insights():
    folder = "Data/SU"
    summaries = []
    for filename in os.listdir(folder):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(folder, filename)
            try:
                df = pd.read_excel(filepath)
                summaries.append(f"📚 {filename}:\n{df.head(3).to_string(index=False)}")
            except Exception as e:
                summaries.append(f"❌ Error reading {filename}: {e}")
    return "\n".join(summaries)


# ----------------------------------
# Ekstraher indsigt fra Inflation
# ----------------------------------
def extract_inflation_insights():
    try:
        df = pd.read_excel("Data/Inflation.xlsx")
        return f"📈 Inflation overview:\n{df.head(5).to_string(index=False)}"
    except Exception as e:
        return f"❌ Error reading Inflation.xlsx: {e}"


# ----------------------------------
# Chatbot-svar baseret på samlet indsigt
# ----------------------------------
def ask_chatbot_about_data(question):
    client = Client()

    combined_context = "\n".join([
        "📂 Salary Insights:\n" + extract_salary_insights(),
        "🥦 Food Insights:\n" + extract_food_insights(),
        "🎓 SU Insights:\n" + extract_su_insights(),
        "💹 Inflation Insights:\n" + extract_inflation_insights(),
    ])

    response = client.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant answering questions based on data from Denmark (wages, food prices, SU, and inflation)."},
            {"role": "user", "content": combined_context[:8000]},
            {"role": "user", "content": question}
        ]
    )
    return response['message']['content']

# Alias til bagudkompatibilitet
ask_chatbot_about_salary = ask_chatbot_about_data

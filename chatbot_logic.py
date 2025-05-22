# chatbot_logic.py
import os
import pandas as pd
from ollama import Client

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

def ask_chatbot_about_salary(question):
    insights = extract_salary_insights()
    client = Client()

    response = client.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": "You are a helpful assistant answering questions based on salary data from Denmark between 2013–2023."},
            {"role": "user", "content": insights[:8000]},
            {"role": "user", "content": question}
        ]
    )
    return response['message']['content']

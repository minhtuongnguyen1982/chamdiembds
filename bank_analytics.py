import os
import io
import requests
import pandas as pd
import numpy as np

SPREADSHEET_ID = "135fwQiNxNh6b7hQWaepJhDMt3ez5wUbu"

def load_and_clean_bank_data():
    """Tải và làm sạch dữ liệu Bank Churn live từ Google Sheets hoặc file local."""
    local_csv = "private/bank/Bank_Churn_Cleaned.csv"
    if os.path.exists(local_csv):
        df = pd.read_csv(local_csv, encoding='utf-8-sig')
        return df, "Kết nối Dữ liệu Đã Làm Sạch (Local Backup)"

    try:
        url_cust = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Customer_Info"
        url_acc = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Account_Info"
        
        r1 = requests.get(url_cust, timeout=10)
        r2 = requests.get(url_acc, timeout=10)
        
        df_cust = pd.read_csv(io.StringIO(r1.text)).dropna(how='all', axis=1)
        df_acc = pd.read_csv(io.StringIO(r2.text)).dropna(how='all', axis=1)
        
        # Clean Customer_Info
        df_cust = df_cust.drop_duplicates(subset=['CustomerId'])
        
        def std_geo(val):
            v = str(val).strip()
            if v in ['FRA', 'French', 'France']: return 'France'
            if v in ['GER', 'German', 'Germany']: return 'Germany'
            if v in ['ESP', 'Spanish', 'Spain']: return 'Spain'
            return v

        df_cust['Geography'] = df_cust['Geography'].apply(std_geo)
        
        def clean_curr(val):
            if pd.isna(val): return 0.0
            return float(str(val).replace('€','').replace(',','').replace(' ','').strip() or 0)

        df_cust['EstimatedSalary'] = df_cust['EstimatedSalary'].apply(clean_curr)
        df_acc['Balance'] = df_acc['Balance'].apply(clean_curr)
        df_cust['Age'] = df_cust['Age'].fillna(df_cust['Age'].median()).astype(int)
        
        df_acc = df_acc.drop_duplicates(subset=['CustomerId'])
        
        def clean_bin(val):
            v = str(val).strip().lower()
            return 1 if v in ['1','yes','true'] else 0

        df_acc['HasCrCard'] = df_acc['HasCrCard'].apply(clean_bin)
        df_acc['IsActiveMember'] = df_acc['IsActiveMember'].apply(clean_bin)
        df_acc['Exited'] = pd.to_numeric(df_acc['Exited'], errors='coerce').fillna(0).astype(int)
        
        df_merged = pd.merge(df_cust, df_acc, on='CustomerId', how='inner')
        
        # Feature Engineering
        def get_age_group(age):
            if age < 30: return "18-29 (Trẻ)"
            elif age < 40: return "30-39 (Trưởng thành)"
            elif age < 50: return "40-49 (Trung niên)"
            elif age < 60: return "50-59 (Cận hưu trí)"
            else: return "60+ (Hưu trí)"

        df_merged['AgeGroup'] = df_merged['Age'].apply(get_age_group)
        df_merged['HasBalance'] = (df_merged['Balance'] > 0).astype(int)
        df_merged['ActiveStatus'] = df_merged['IsActiveMember'].map({1: "Active", 0: "Inactive"})
        df_merged['ChurnStatus'] = df_merged['Exited'].map({1: "Churned", 0: "Retained"})
        
        # Risk score
        def score_risk(r):
            s = 10
            if r['Geography'] == 'Germany': s += 25
            if 50 <= r['Age'] <= 59: s += 35
            elif 40 <= r['Age'] <= 49: s += 15
            if r['NumOfProducts'] == 3: s += 45
            elif r['NumOfProducts'] >= 4: s += 60
            if r['IsActiveMember'] == 0: s += 20
            if r['Balance'] > 0: s += 10
            return min(100, s)

        df_merged['RiskScore'] = df_merged.apply(score_risk, axis=1)
        
        def risk_level(s):
            if s >= 70: return "Rất Cao (Critical)"
            elif s >= 50: return "Cao (High)"
            elif s >= 30: return "Trung Bình (Medium)"
            else: return "Thấp (Low)"

        df_merged['RiskLevel'] = df_merged['RiskScore'].apply(risk_level)
        return df_merged, "Đồng bộ Trực Tiếp từ Google Sheets API"
    except Exception as e:
        return pd.DataFrame(), f"Lỗi tải dữ liệu: {e}"

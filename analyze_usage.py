#!/usr/bin/env python3
"""
Analyze Cursor usage data and calculate CARMA savings
"""

import pandas as pd
import numpy as np

def analyze_usage():
    # Read the CSV file
    df = pd.read_csv('usage-events-2025-09-23.csv')
    
    print('=== RAW DATA PREVIEW ===')
    print(f'Total rows: {len(df)}')
    print(f'Columns: {list(df.columns)}')
    print()
    print('First 5 rows:')
    print(df.head())
    print()
    
    print('=== COST COLUMN ANALYSIS ===')
    print(f'Cost column type: {df["Cost"].dtype}')
    print(f'Cost column sample: {df["Cost"].head(10).tolist()}')
    print(f'Cost column unique values: {df["Cost"].unique()[:10]}')
    print(f'Cost column null values: {df["Cost"].isnull().sum()}')
    print()
    
    print('=== FILTERED DATA ===')
    df_clean = df[df['Kind'] == 'Included'].copy()
    print(f'Clean rows: {len(df_clean)}')
    print(f'Clean cost sum: {df_clean["Cost"].sum()}')
    print(f'Clean cost mean: {df_clean["Cost"].mean()}')
    print(f'Clean cost std: {df_clean["Cost"].std()}')
    print()
    
    # Calculate totals
    total_cost = df_clean['Cost'].sum()
    total_tokens = df_clean['Total Tokens'].sum()
    total_input_with_cache = df_clean['Input (w/ Cache Write)'].sum()
    total_input_without_cache = df_clean['Input (w/o Cache Write)'].sum()
    total_cache_read = df_clean['Cache Read'].sum()
    total_output = df_clean['Output Tokens'].sum()
    
    print('=== CURSOR USAGE ANALYSIS ===')
    print(f'Total Cost: ${total_cost:.2f}')
    print(f'Total Tokens: {total_tokens:,}')
    print(f'Total Input (w/ Cache): {total_input_with_cache:,}')
    print(f'Total Input (w/o Cache): {total_input_without_cache:,}')
    print(f'Total Cache Reads: {total_cache_read:,}')
    print(f'Total Output: {total_output:,}')
    print()
    
    print('=== CACHE EFFICIENCY ===')
    cache_hit_rate = total_cache_read / (total_input_without_cache + total_cache_read) * 100
    cache_savings_tokens = total_input_without_cache - total_input_with_cache
    cache_savings_percent = (cache_savings_tokens / total_input_without_cache) * 100 if total_input_without_cache > 0 else 0
    print(f'Cache Hit Rate: {cache_hit_rate:.1f}%')
    print(f'Cache Savings (Tokens): {cache_savings_tokens:,}')
    print(f'Cache Savings (%): {cache_savings_percent:.1f}%')
    print()
    
    print('=== COST PER TOKEN ===')
    cost_per_token = total_cost / total_tokens if total_tokens > 0 else 0
    print(f'Cost per Token: ${cost_per_token:.6f}')
    print()
    
    print('=== ESTIMATED CARMA SAVINGS ===')
    # CARMA achieves 90% token reduction for repeated context
    carma_savings_tokens = total_input_without_cache * 0.9
    carma_savings_cost = carma_savings_tokens * cost_per_token
    print(f'CARMA Token Savings (90%): {carma_savings_tokens:,.0f} tokens')
    print(f'CARMA Cost Savings: ${carma_savings_cost:.2f}')
    print(f'CARMA Cost Reduction: {(carma_savings_cost/total_cost)*100:.1f}%')
    print()
    
    print('=== DAILY PROJECTIONS ===')
    daily_cost = total_cost
    monthly_cost = daily_cost * 30
    yearly_cost = daily_cost * 365
    print(f'Daily Cost: ${daily_cost:.2f}')
    print(f'Monthly Cost: ${monthly_cost:.2f}')
    print(f'Yearly Cost: ${yearly_cost:.2f}')
    print()
    
    print('=== CARMA SAVINGS PROJECTIONS ===')
    carma_daily_savings = carma_savings_cost
    carma_monthly_savings = carma_daily_savings * 30
    carma_yearly_savings = carma_daily_savings * 365
    print(f'CARMA Daily Savings: ${carma_daily_savings:.2f}')
    print(f'CARMA Monthly Savings: ${carma_monthly_savings:.2f}')
    print(f'CARMA Yearly Savings: ${carma_yearly_savings:.2f}')

if __name__ == "__main__":
    analyze_usage()

import pandas as pd

# Load the data
df = pd.read_csv('SEA_Oct_2024 (1).csv')

# Clean data: Remove special characters from column names and handle missing values
df.columns = df.columns.str.replace(' ', '_')
df['Leads_Number'] = df['Leads_Number'].replace(0, pd.NA)  # Handle 0 leads

# Calculate key metrics
def calculate_metrics(df):
    # Cost Per Lead (CPL)
    df['CPL'] = df['Cost'] / df['Leads_Number']
    
    # Conversion Rate (Leads/Clicks)
    df['Conversion_Rate'] = df['Leads_Number'] / df['Clicks']
    
    # Click-Through Rate (CTR) - already exists, but we'll format it
    df['CTR'] = df['CTR'] * 100  # Convert to percentage
    
    return df

df = calculate_metrics(df)

# Identify top/bottom performers
def analyze_performance(df):
    # Filter out markets with no leads
    valid_markets = df[df['Leads_Number'] > 0]
    
    # Sort by key metrics
    top_cpl = valid_markets.sort_values('CPL').head(3)
    top_conversion = valid_markets.sort_values('Conversion_Rate', ascending=False).head(3)
    top_ctr = df.sort_values('CTR', ascending=False).head(3)
    
    # Identify worst performers
    bottom_cpl = valid_markets.sort_values('CPL', ascending=False).head(3)
    bottom_ctr = df.sort_values('CTR').head(3)
    
    return {
        'top_cpl': top_cpl,
        'top_conversion': top_conversion,
        'top_ctr': top_ctr,
        'bottom_cpl': bottom_cpl,
        'bottom_ctr': bottom_ctr
    }

analysis = analyze_performance(df)

# Generate budget recommendations
def budget_recommendations(analysis):
    increase = []
    decrease = []
    
    # Markets to increase
    for market in analysis['top_cpl']['Market']:
        increase.append(market)
    for market in analysis['top_ctr']['Market']:
        if market not in increase:
            increase.append(market)
            
    # Markets to decrease
    for market in analysis['bottom_cpl']['Market']:
        decrease.append(market)
    for market in analysis['bottom_ctr']['Market']:
        if market not in decrease:
            decrease.append(market)
    
    # Remove duplicates
    increase = list(set(increase))
    decrease = list(set(decrease))
    
    return {'increase': increase, 'decrease': decrease}

recommendations = budget_recommendations(analysis)

# Print results
print("Key Performance Analysis")
print("="*50)
print("\nTop 3 Markets by Cost Per Lead:")
print(analysis['top_cpl'][['Market', 'CPL', 'Conversion_Rate', 'CTR']])
print("\nTop 3 Markets by CTR:")
print(analysis['top_ctr'][['Market', 'CTR', 'CPL', 'Conversion_Rate']])

print("\n\nBudget Reallocation Recommendations")
print("="*50)
print(f"Increase budget for: {', '.join(recommendations['increase'])}")
print(f"Decrease budget for: {', '.join(recommendations['decrease'])}")

# Optional: Export to Excel for visualization
df.to_excel('SEA_analysis.xlsx', index=False)

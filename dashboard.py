import streamlit as st 
import pandas as pd 
import io 
import matplotlib.pyplot as plt

def about_df(df): 
    # Sample view (min use kiya hai taake agar rows 10 se kam hon to error na aaye)
    df_sample = df.sample(min(10, len(df))) 
    size = df.shape 
    buffer = io.StringIO() 
    df.info(buf=buffer) 
    info = buffer.getvalue() 
    columns = df.dtypes 
    missing_values = df.isnull().sum() 
    # Isko stats_dataset rakha hai taake customer wale stats se mix na ho
    stats_dataset = df.describe(include='all') 
    return df_sample, size, info, columns, missing_values, stats_dataset 

def customer_statistics(df): 
    average_age = df.iloc[:, 1].mean() 
    average_tenure = df.iloc[:, 3].mean() 
    total_spend = df.iloc[:, 9].sum() 
    average_support_calls = df.iloc[:, 5].mean() 
    churn_rate = df.iloc[:, 11].mean() * 100 
    payment_delay_std_dev = df.iloc[:, 6].std() 
    
    statistics = { 
        'Average Age': average_age, 
        'Average Tenure': average_tenure, 
        'Total Spend': total_spend, 
        'Average Support Calls': average_support_calls, 
        'Churn Rate (%)': churn_rate, 
        'Payment Delay Std Dev': payment_delay_std_dev 
    } 
    return statistics 

def future_insights(df): 
    average_monthly_spend = df.iloc[:,9].mean() 
    projected_total_spend_year = average_monthly_spend * 12 * len(df) 
    churn_rate = df.iloc[:,11].mean() 
    projected_churn_next_year = churn_rate * len(df) 
    average_support_calls = df.iloc[:,5].mean() 
    projected_support_calls_increase = average_support_calls * 1.1 
    average_payment_delay = df.iloc[:,6].mean() 
    projected_payment_delay_increase = average_payment_delay * 1.05 
    standard_and_basicd_users = df[(df.iloc[:,7] == 'Standard') | (df.iloc[:,7] == 'Basic')] 
    projected_upgrades = len(standard_and_basicd_users) * 0.15 
    average_tenure = df.iloc[:,3].mean() 
    project_tenure_growth_year = average_tenure * 1.2 
    
    insights = { 
        'Project Total Spend Next year': projected_total_spend_year, 
        'Project Churn Next year': projected_churn_next_year, 
        'Project Support Calls Increase': projected_support_calls_increase, 
        'Project Payment Delay Increase': projected_payment_delay_increase, 
        'Project Subscription Upgrade': projected_upgrades, 
        'Project Tenure Growth': project_tenure_growth_year 
    } 
    return insights 

#dashboard function here====================================================
def age_distribution_graph(df):
    fig, ax = plt.subplots()
    df['Age'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title("Distribution of Age")
    ax.set_xlabel("Age")    
    ax.set_ylabel("Frequency")
    return fig

# Average Total Spend by Subscription Type
def avg_total_spend_subscription_type(df):
    fig, ax = plt.subplots()
    df.groupby('Subscription Type')['Total Spend'].mean().plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Average Total Spend by Subscription Type')
    ax.set_xlabel('Subscription Type')
    ax.set_ylabel('Average Total Spend')
    return fig

def gender_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df['Gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Gender Distribution')
    ax.set_ylabel('')
    return fig

# Total Spend Distribution by Contract Length
def total_spend_distribution_by_contract_length(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby('Contract Length')['Total Spend'].sum().plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'], ax=ax)
    ax.set_title('Total Spend Distribution by Contract Length')
    ax.set_ylabel('')
    return fig

# Churn Rate by Gender
def churn_rate_by_gender(df):
    fig, ax = plt.subplots()
    churn_rate_by_gender = df.groupby('Gender')['Churn'].mean() * 100
    churn_rate_by_gender.plot(kind='bar', color='coral', ax=ax)
    ax.set_title('Churn Rate by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Churn Rate (%)')
    return fig

# Age Distribution by Gender
def age_distribution_by_gender(df):
    fig, ax = plt.subplots()
    df[df['Gender'] == 'Male']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='blue', label='Male', ax=ax)
    df[df['Gender'] == 'Female']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='red', label='Female', ax=ax)
    ax.set_title('Age Distribution by Gender')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    ax.legend()
    return fig


#python main==================================================================
if __name__ == "__main__": 
    st.title("Customer Churn App") 
    st.subheader("Data Analysis Dashboard With Visualizations and future insights") 
    st.write("----------------------------------------------------------------------------") 
    
    st.sidebar.title("churn Analysis") 
    uploaded_file = st.sidebar.file_uploader("Choose a csv file", type='csv') 
    
    if uploaded_file is not None: 
        df = pd.read_csv(uploaded_file) 
        
        # Aapke purane variables ke names button se baahar define kar diye hain
        df_sample, size, info, columns, missing_values, stats_dataset = about_df(df)
        stats = customer_statistics(df)
        future_ints = future_insights(df)
        
        # About Dataset Button
        if st.sidebar.button("About Dataset"): 
            st.subheader("About Dataset") 
            st.subheader('Dataframe Sample:') 
            st.write(df_sample) 
            st.subheader('DataFrame Size:') 
            st.write(size) 
            st.subheader('DataFrame Info:') 
            st.text(info) 
            st.subheader('Column Names and Types:') 
            st.write(columns) 
            st.subheader('Missing Values:') 
            st.write(missing_values) 
            st.subheader('Statistics:') 
            st.write(stats_dataset) 
            
        # Customer Statistics Button
        if st.sidebar.button("Customer Statistics"): 
            st.subheader("Customer Statistics") 
            for key, value in stats.items(): 
                if isinstance(value, (int, float)): 
                    st.write(f"{key}: {round(value, 2)}") 
                else: 
                    st.write(f"{key}: {value}") 
                    
        # Future Insights Button
                # Future Insights Button
        if st.sidebar.button("Future Insights"): 
            st.subheader("Future Statistics (Insights)") 
            for key, value in future_ints.items(): 
                if isinstance(value, (int, float)): 
                    st.write(f"{key}: {round(value, 2)}") 
                else: 
                    st.write(f"{key}: {value}")

        # ✅ Customer dashboard ab bilkul sahi jagah par hai
        # Customer dashboard============================================================
        if st.sidebar.button("Customer dashboard"):
            st.subheader("Customer dashboard")
       
            #age, and spend
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader('Age Distribution')
                fig = age_distribution_graph(df)
                st.pyplot(fig)
                
            with col2:
                st.subheader('Avg Sub Spend Type')
                fig = avg_total_spend_subscription_type(df)
                st.pyplot(fig)    
            
            col1, col2 = st.columns(2)
                        
            with col1:
                st.subheader('Gender Distribution')
                fig = gender_distribution(df)
                st.pyplot(fig)
                
            with col2:
                st.subheader('T/Spend Contract Length')
                fig = total_spend_distribution_by_contract_length(df)
                st.pyplot(fig)    
                                
            col1, col2 = st.columns(2)
                                    
            with col1:
                st.subheader('Churn Rate By Gender')
                fig = churn_rate_by_gender(df)
                st.pyplot(fig)
                            
            with col2:
                st.subheader('Age Dist By Gender')
                fig = age_distribution_by_gender(df)
                st.pyplot(fig)        
                
                
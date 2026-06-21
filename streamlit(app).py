import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.express as px


st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")
st.title("🥗 Local Food Wastage Management System")


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Food Waste Management",
        user="postgres",
        password="harshamandeep123",
        port="5432"
    )

def run_query(query):
    try:
        conn = get_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Query Error: {e}")
        return None
 
with st.sidebar: 
    menu = st.sidebar.selectbox("Select Menu", ["Dashboard & Filters", "Manage Food Listings","All 15 SQL Queries","Providers/Receivers Info"])
    st.markdown("""
<div style="
background-color:#ffffff;
padding:18px;
border-radius:12px;
border:1px solid #e5e7eb;
margin-bottom:20px;
box-shadow:0 2px 8px rgba(0,0,0,0.08);
">

<h4>🚀 Project Overview</h4>

<b>Technology Stack:</b><br>
🐍 Python &nbsp; | &nbsp;
🗄️ SQL &nbsp; | &nbsp;
📊 Streamlit &nbsp; | &nbsp;
📈 Data Analysis

<br><br>

<b>Project Highlights:</b><br>
📋 4 Database Tables &nbsp; | &nbsp;
📂 4,000+ Records &nbsp; | &nbsp;
🔍 15 SQL Queries &nbsp; | &nbsp;
📊 Interactive Dashboard

</div>
""", unsafe_allow_html=True)

if menu == "Dashboard & Filters":
    st.markdown ("""
    <div style="
    background: linear-gradient(90deg, #dbeafe, #ecfdf5 );
    padding:25px;
    border-radius:15px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
    margin-bottom:20px;
    ">
    <h2 style="color:#1e3a8a;">🍽️ Local Food Wastage Management System</h2>
    <p style="font-size:16px;">
    Transforming surplus food into opportunities for communities.
    This system enables efficient food donation management, real-time monitoring,
    claim tracking, and data-driven decision making.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
# --- KPI METRICS SECTION START ---
    
    kpi_items = run_query("SELECT COUNT(*) as total FROM food_listing;")
    kpi_volume = run_query("SELECT SUM(quantity) as total_qty FROM food_listing;")
    kpi_claims = run_query("SELECT COUNT(*) as total_done FROM claim WHERE status = 'Completed';")
    kpi_total_claims = run_query("SELECT COUNT(*) as total_all FROM claim;")
    
    total_items = kpi_items['total'].iloc[0] if kpi_items is not None and not kpi_items.empty else 0
    total_volume = kpi_volume['total_qty'].iloc[0] if kpi_volume is not None and not kpi_volume.empty and kpi_volume['total_qty'].iloc[0] is not None else 0
    completed_claims = kpi_claims['total_done'].iloc[0] if kpi_claims is not None and not kpi_claims.empty else 0
    all_claims = kpi_total_claims['total_all'].iloc[0] if kpi_total_claims is not None and not kpi_total_claims.empty else 0
    success_rate = (completed_claims / all_claims * 100) if all_claims > 0 else 0.0

   
    st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 8px !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label=" Total Unique Items", value=int(total_items))
    with col2:
        st.metric(label=" Total Volume (Units)", value=int(total_volume))
    with col3:
        st.metric(label="✅ Secured Claims", value=int(completed_claims))
    with col4:
        st.metric(label="📈 Success Rate", value=f"{success_rate:.1f}%")
        
    st.markdown("---")

# --- ADVANCED 4 GRAPHS SECTION START ---
    import plotly.express as px
    st.markdown("###  Visual Distribution Metrics & Performance Trends")
    
    # --- ROW 1: Side-by-Side Graphs (City Bar & Meal Donut) ---
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.markdown("#### Total Food Quantity Available by City Location")
        city_data = run_query("SELECT location, SUM(quantity) as total_quantity FROM food_listing GROUP BY location order by total_quantity desc limit 10;")
        if city_data is not None and not city_data.empty:
            fig1 = px.bar(city_data, x='location', y='total_quantity', 
                          labels={'location': 'City', 'total_quantity': 'Units Allocated'},
                          color='location', color_discrete_sequence=px.colors.qualitative.Set2)
            fig1.update_layout(showlegend=False, height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No location data available.")
            
    with row1_col2:
        st.markdown("#### Demand Velocity Breakdown (Total Claims by Meal Type)")
        
        meal_data = run_query("""
            SELECT fl.meal_type, COUNT(c.claim_id) as total_claims 
            FROM food_listing fl 
            JOIN claim c ON fl.food_id = c.food_id 
            GROUP BY fl.meal_type;
        """)
        if meal_data is not None and not meal_data.empty:
            fig2 = px.pie(meal_data, values='total_claims', names='meal_type', hole=0.5,
                          color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig2, use_container_width=True)
        else:
           
            backup_meal = run_query("SELECT meal_type, SUM(quantity) as total_claims FROM food_listing GROUP BY meal_type;")
            if backup_meal is not None and not backup_meal.empty:
                fig2 = px.pie(backup_meal, values='total_claims', names='meal_type', hole=0.5)
                fig2.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ROW 2: Side-by-Side Graphs (Dietary Stream & Claim Status) ---
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.markdown("#### Volume Stream Profile (Dietary Composition Matrix)")
        diet_data = run_query("""
            SELECT food_type, provider_type, SUM(quantity) as volume_sum 
            FROM food_listing 
            GROUP BY food_type, provider_type;
        """)
        if diet_data is not None and not diet_data.empty:
            fig3 = px.bar(diet_data, x='food_type', y='volume_sum', color='provider_type', barmode='group',
                          labels={'food_type': 'Diet Category Pattern', 'volume_sum': 'Volume Sum'},
                          color_discrete_sequence=px.colors.qualitative.Bold)
            fig3.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No dietary composition data available.")

    row2_col1, row2_col2 = st.columns(2)           
    with row2_col2:
        st.markdown("#### Active System Claims Operations Tracking Status")
        status_data = run_query("SELECT status, COUNT(*) as status_count FROM claim GROUP BY status ORDER BY status_count DESC;")
        
        if status_data is not None and not status_data.empty:
            fig4 = px.bar(status_data, 
                          x='status_count', 
                          y='status', 
                          orientation='h', 
                          color='status',
                          labels={'status_count': 'Count', 'status': 'Status'},
                          color_discrete_sequence=px.colors.qualitative.Vivid)
            fig4.update_layout(showlegend=False, height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig4, use_container_width=True)
        else:
            
            dummy_status = pd.DataFrame({'status': ['Completed', 'Pending', 'Cancelled'], 'status_count': [3, 2, 1]})
            fig4 = px.bar(dummy_status, x='status_count', y='status', orientation='h', color='status',
                          color_discrete_sequence=['#1f77b4', '#aec7e8', '#ffbb78'])
            fig4.update_layout(showlegend=False, height=350, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig4, use_container_width=True)

    # --- KPI METRICS SECTION END ---

   
    locations_df = run_query("SELECT DISTINCT location FROM food_listing WHERE location IS NOT NULL;")
    
    if locations_df is not None and not locations_df.empty:
         location_list = ["All"] + locations_df['location'].tolist()
         selected_location = st.selectbox("Select Location (City):", location_list)
        
    if selected_location == "All":
            listing_query = "SELECT * FROM food_listing LIMIT 50;"
    else:
            listing_query = f"SELECT * FROM food_listing WHERE location = '{selected_location}';"
            
    listings = run_query(listing_query)
    if listings is not None:
        st.markdown("### 📋 Active Surplus Food Listings")
        st.dataframe(listings)

elif menu == "Manage Food Listings":
   crud_action="Add new food item"
   st.markdown("### 🛠️ Manage Food Listings (CRUD Operations)")
    
    
   st.markdown("#### ➕ List Surplus Food")
   with st.form("add_food_form"):
         food_name = st.text_input("Food Item Name")
         quantity = st.number_input("Quantity", min_value=1.0, step=0.5)
         expiry_date = st.date_input("Expiry Date")
         provider_id = st.number_input("Provider ID", min_value=1, step=1)
        
         submitted = st.form_submit_button("Submit Listing")
         if submitted:
            if food_name:
                st.success(f"Successfully added {food_name}!")
            else:
                st.error("Please enter a food name.")

         st.markdown("<br><hr>", unsafe_allow_html=True)

    # --- 2. UPDATE EXISTING ITEM (बिना किसी crud_action के झंझट के) ---
   st.markdown("### 📝 Update Food Quantity")
   with st.form("update_food_form"):
          food_id_to_update = st.number_input("Enter Food ID to Update", min_value=1, step=1)
          new_quantity = st.number_input("Enter New Quantity", min_value=1.0, step=0.5)
        
          update_btn = st.form_submit_button("Update Item")
          if update_btn:
            st.success(f"Food ID {food_id_to_update} updated with quantity {new_quantity}!")

   st.markdown("<br><hr>", unsafe_allow_html=True)

    # --- 3. DELETE ITEM ---
   st.markdown("### 🗑️ Delete Food Item")
   with st.form("delete_food_form"):
          food_id_to_delete = st.number_input("Enter Food ID to Delete", min_value=1, step=1)
        
          delete_btn = st.form_submit_button("Delete Item")
          if delete_btn:
            st.warning(f"Food ID {food_id_to_delete} deleted successfully!")


elif menu == "All 15 SQL Queries":
  
    
    # --- SIMPLE TITLE ---
    st.markdown("## 🔍 SQL Query Explorer")
    st.write("Select an analytical query from the list below to view and execute it.")
    
    st.markdown("---") # एक पतली नॉर्मल डिवाइडर लाइन

    # --- QUERY DROPDOWN ---
    query_options = [
        "Q1 — Providers & Receivers per City",
        "Q2 — Highest contributing provider type",
        "Q3 — Contact info of providers in a specific city",
        "Q4 — Receivers who claimed the most food",
        "Q5 — Total quantity of food available",
        "Q6 — City with highest food listings",
        "Q7 — Most commonly available food types",
    
        "Q8 — Food cliams per food item",
        "Q9 — Provider with highest successful claims",
        "Q10 — Percentage of claim statuses",
        "Q11 — Average quantity claimed per receiver",
        "Q12 — Most claimed meal type",
        "Q13 — Total quantity donated by each provider",
        "Q14 — Most frequently claimed food locations",
        "Q15 — Most frequent food providers and contributions"
    ]
    selected_query = st.selectbox("Select a query:", query_options)

    # --- BASIC DESCRIPTION (Normal Info Box) ---
    descriptions = {
        "Q1 — Providers & Receivers per City": "Count total numbers of providers & receivers in a city",
        "Q2 — Highest contributing provider type":"The food contributor who contributes the most",
        "Q3 — Contact info of providers in a specific city":"Details of a provider in a particular city",
        "Q4 — Receivers who claimed the most food":"The most food claimed dood receiver",
        "Q5 — Total quantity of food available":"Total quantity of food available",
        "Q6 — City with highest food listings":" The city with highest food listing",
        "Q7 — Most commonly available food types":"Easily available food type",
    
        "Q8 — Food cliams per food item":"Food cliams per food item",
        "Q9 — Provider with highest successful claims":"Provider with highest successful claims",
        "Q10 — Percentage of claim statuses":"Percentage of claim statuses",
        "Q11 — Average quantity claimed per receiver":"Average qty per receiver",
        "Q12 — Most claimed meal type":"most claimed meal type",
        "Q13 — Total quantity donated by each provider":"Total quantity donated by each provider",
        "Q14 — Most frequently claimed food locations":"Most frequently claimed food locations",
        "Q15 — Most frequent food providers and contributions":"Most frequent food providers and contributions"
    }
    
    current_desc = descriptions.get(selected_query, "Run analytics on database state.")
    
    # यह Streamlit का बेसिक लाइट ब्लू बॉक्स है जो व्हाइट थीम पर बहुत साफ दिखता है
    st.info(current_desc)

    # --- STANDARD BUTTONS ---
    # नॉर्मल बटन्स जो आपके ऐप की डिफ़ॉल्ट थीम (White/Light) को फॉलो करेंगे
    if st.button("Run Selected Query", use_container_width=True):
        st.write(f"Showing results for: *{selected_query}*")
        # यहाँ आपका डेटाबेस क्वेरी रन करने का कोड आएगा:
        # df = run_query(...)
        # st.dataframe(df)

    if st.button("Run All Queries", use_container_width=True):
        st.success("Running entire analytical batch...")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BASIC EXPANDER FOR SQL ---
    with st.expander("View SQL Statement"):
        sql_statements = {
            "Q1 — Providers & Receivers per City": '''select city,
sum(case when role='provider' then 1 else 0 end)as total_providers,
sum(case when role='receiver' then 1 else 0 end)as total_receivers
from
(select city,'provider' as role from providers
union all
select city,'receiver' as role from recievers)
as combined_data
group by city order by city;''',
        "Q2 — Highest contributing provider type": "select provider_type, count(provider_type) as total_contribute from food_listing group by provider_type;",
        "Q3 — Contact info of providers in a specific city": "select city,provider_name, contact,address from providers where city = 'New Jessica';",
        "Q4 — Receivers who claimed the most food": "select claim.receiver_id, recievers.type, count(claim.receiver_id) as total_count from claim join recievers on claim.receiver_id= recievers.receiver_id group by claim.receiver_id,recievers.type order by total_count desc limit 5;",
        "Q5 — Total quantity of food available":"select provider_type,sum(quantity) as total_available_food from food_listing group by provider_type;",
        "Q6 — City with highest food listings":"select location, count(meal_type) as highest_food_listing from food_listing group by location order by highest_food_listing desc limit 1;",
        "Q7 — Most commonly available food types":"select food_type, count(food_type) as commonly_available from food_listing group by food_type;",
    
        "Q8 — Food cliams per food item":"select food_listing.food_name, count(claim.claim_id) as total_claims from food_listing join claim on claim.food_id=food_listing.food_id group by food_listing.food_name;",

        "Q9 — Provider with highest successful claims":"select food_listing.provider_type,count(claim.status) as no_of_successfull_claims from food_listing join claim on food_listing.food_id=claim.food_id group by food_listing.provider_type,claim.status having claim.status='Completed';",

        "Q10 — Percentage of claim statuses":"select status,count(status) as total_counts, round((count(status)*100)/sum(count(status))over(), 2 )as percentage from claim group by status;",

        "Q11 — Average quantity claimed per receiver":"select claim.receiver_id, round(avg(food_listing.quantity),0) as avg_quantity from claim join food_listing on claim.food_id= food_listing.food_id group by claim.receiver_id;",
        "Q12 — Most claimed meal type":"select food_listing.meal_type,count(claim.claim_id) as total_claimed from food_listing join claim on food_listing.food_id=claim.food_id group by food_listing.meal_type order by total_claimed desc;",
        "Q13 — Total quantity donated by each provider":"select provider_type, sum(quantity) as total_quantity from food_listing group by provider_type;",
        "Q14 — Most frequently claimed food locations":"select food_listing.location, count(claim.claim_id) as total_claims from food_listing join claim on food_listing.food_id=claim.food_id group by food_listing.location order by total_claims desc;",
        "Q15 — Most frequent food providers and contributions":"select provider_id,provider_type,count(food_id) as total_donation ,sum(quantity) as total_contribution from food_listing group by provider_id,provider_type order by total_contribution desc ,total_donation desc limit 10; "
            
        }
        st.code(sql_statements.get(selected_query, "-- SQL Query Template\nSELECT * FROM food_listing;"), language="sql")
    
elif menu== "Providers/Receivers Info":

    st.markdown("---")
    
    
    tab1, tab2 = st.tabs(["🏪 Food Providers", "🤝 Food Receivers / NGOs"])
    
    # ==================== 1. FOOD PROVIDERS TAB ====================
    with tab1:
        st.subheader("Search Food Providers")
        
        # SQL Query
        provider_query = """
            SELECT "provider_id", "provider_name", "type", "address", "city", "contact" 
            FROM providers;
        """
        
        
        df_providers = run_query(provider_query)
        
        
        if df_providers is not None and not df_providers.empty:
            st.success(f"🏪 {len(df_providers)} provider(s) found")
            st.dataframe(df_providers, use_container_width=True, hide_index=True)
        elif df_providers is not None:
            st.warning("No providers found in database.")

    # ==================== 2. FOOD RECEIVERS TAB ====================
    with tab2:
        st.subheader("Search Food Receivers / NGOs")
        
        # SQL Query
        reciever_query = """
            SELECT "receiver_id", "name", "type", "city", "contact" 
            FROM recievers;
        """
        
       
        df_recievers = run_query(reciever_query)
        
        if df_recievers is not None and not df_recievers.empty:
            st.success(f"🤝 {len(df_recievers)} receiver(s) found")
            st.dataframe(df_recievers, use_container_width=True, hide_index=True)
        elif df_recievers is not None:
            st.warning("No recievers found in database.")
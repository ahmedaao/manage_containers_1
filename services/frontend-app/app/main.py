import streamlit as st
import requests
import os

API_GATEWAY_URL = os.getenv('API_GATEWAY_URL')

st.title("🎬 Movie Platform")

# Tabs to separate Inventory and Billing
tab1, tab2 = st.tabs(["📦 Inventory", "💳 Billing"])

with tab1:
    st.header("Inventory Management")
    
    # GET all movies
    if st.button("View All Movies"):
        response = requests.get(f"{API_GATEWAY_URL}/api/movies")
        if response.status_code == 200:
            movies = response.json()
            if movies:
                st.success(f"Found {len(movies)} movies")
                for movie in movies:
                    st.write(f"**{movie.get('title')}** (ID: {movie.get('id')})")
                    st.write(f"Description: {movie.get('description', 'N/A')}")
                    st.write("---")
            else:
                st.info("No movies found")
        else:
            st.error("Error fetching movies")
    
    # GET movie by ID
    col1, col2 = st.columns(2)
    with col1:
        movie_id = st.number_input("Movie ID", min_value=1, step=1, key="get_id")
        if st.button("Get Movie by ID"):
            response = requests.get(f"{API_GATEWAY_URL}/api/movies/{movie_id}")
            if response.status_code == 200:
                st.success("Movie found!")
                st.json(response.json())
            else:
                st.error("Movie not found")
    
    # GET movies by title search
    with col2:
        search_title = st.text_input("Search by title")
        if st.button("Search Movies") and search_title:
            response = requests.get(f"{API_GATEWAY_URL}/api/movies?title={search_title}")
            if response.status_code == 200:
                movies = response.json()
                if movies:
                    st.success(f"Found {len(movies)} movies")
                    for movie in movies:
                        st.write(f"**{movie.get('title')}** (ID: {movie.get('id')})")
                else:
                    st.info("No movies found with that title")
            else:
                st.error("Search error")
    
    # POST new movie
    with st.form("add_movie"):
        st.subheader("Add New Movie")
        title = st.text_input("Title *")
        description = st.text_area("Description")
        if st.form_submit_button("Add Movie"):
            if title:
                data = {"title": title, "description": description}
                response = requests.post(f"{API_GATEWAY_URL}/api/movies", json=data)
                if response.status_code == 201:
                    st.success("Movie added successfully!")
                    st.json(response.json())
                else:
                    st.error("Error adding movie")
            else:
                st.error("Title is required")
    
    # PUT update movie
    with st.form("update_movie"):
        st.subheader("Update Movie")
        update_id = st.number_input("Movie ID to update *", min_value=1, step=1, key="update_id")
        new_title = st.text_input("New Title *")
        new_description = st.text_area("New Description")
        if st.form_submit_button("Update Movie"):
            if update_id and new_title:
                data = {"title": new_title, "description": new_description}
                response = requests.put(f"{API_GATEWAY_URL}/api/movies/{update_id}", json=data)
                if response.status_code == 200:
                    st.success("Movie updated successfully!")
                    st.json(response.json())
                else:
                    st.error("Error updating movie")
            else:
                st.error("ID and title are required")
    
    # DELETE operations
    st.subheader("Delete Operations")
    col3, col4 = st.columns(2)
    
    with col3:
        delete_id = st.number_input("Movie ID to delete", min_value=1, step=1, key="delete_id")
        if st.button("🗑️ Delete Movie by ID", type="secondary"):
            response = requests.delete(f"{API_GATEWAY_URL}/api/movies/{delete_id}")
            if response.status_code == 200:
                st.success("Movie deleted successfully!")
            else:
                st.error("Error deleting movie")
    
    with col4:
        if st.button("🗑️ Delete ALL Movies", type="secondary"):
            if st.session_state.get('confirm_delete_all'):
                response = requests.delete(f"{API_GATEWAY_URL}/api/movies")
                if response.status_code == 200:
                    st.success("All movies deleted!")
                    st.session_state.confirm_delete_all = False
                else:
                    st.error("Error deleting movies")
            else:
                st.session_state.confirm_delete_all = True
                st.warning("⚠️ Click again to confirm deletion of ALL movies!")

with tab2:
    st.header("Billing Management")
    
    # POST new order
    with st.form("add_order"):
        st.subheader("Create New Order")
        user_id = st.text_input("User ID *")
        items = st.number_input("Number of Items *", min_value=1, value=1)
        amount = st.number_input("Total Amount *", min_value=0.01, value=10.0, format="%.2f")
        
        if st.form_submit_button("Create Order"):
            if user_id and items and amount:
                data = {
                    "user_id": user_id,
                    "number_of_items": str(items),
                    "total_amount": str(amount)
                }
                response = requests.post(f"{API_GATEWAY_URL}/api/billing", json=data)
                if response.status_code == 200:
                    st.success("Order sent successfully!")
                    st.info("📨 Order is being processed via RabbitMQ")
                else:
                    st.error("Error sending order")
            else:
                st.error("All fields are required")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(f"API Gateway: {API_GATEWAY_URL}")
st.sidebar.caption("🚀 CRUD Master Py - Microservices Platform")
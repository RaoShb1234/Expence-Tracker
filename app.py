import streamlit as st
import datetime

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
st.title("💰 Personal Expense Tracker")

# --- Initialize Session State ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# --- Functions ---
def add_expense(name, amount, category, date):
    expense = {
        "Expense Name": name,
        "Amount": amount,
        "Category": category,
        "Date": str(date)
    }
    st.session_state.expenses.append(expense)

def delete_expense(index):
    st.session_state.expenses.pop(index)

# --- Task 1: Add Expense Form ---
st.header("Add New Expense")
with st.form("expense_form"):
    col1, col2 = st.columns(2)
    with col1:
        exp_name = st.text_input("Expense Name")
        exp_amount = st.number_input("Amount (Rs)", min_value=1.0, step=10.0)
    with col2:
        exp_category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
        exp_date = st.date_input("Date", datetime.date.today())
    
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        if exp_name.strip() == "":
            st.error("Please enter expense name!")
        else:
            add_expense(exp_name, exp_amount, exp_category, exp_date)
            st.success(f"Expense '{exp_name}' added successfully!")

st.divider()

# --- Sidebar Filters - Task 4 ---
st.sidebar.header("Filters")

search_query = st.sidebar.text_input("Search Expense by Name")

category_options = ["All", "Food", "Travel", "Shopping", "Bills", "Other"]
selected_category = st.sidebar.selectbox("Filter by Category", category_options)

# Amount Filter
if st.session_state.expenses:
    max_amount = max([e["Amount"] for e in st.session_state.expenses])
else:
    max_amount = 10000

amount_range = st.sidebar.slider("Filter by Amount", 0, int(max_amount) if max_amount > 0 else 10000, (0, int(max_amount) if max_amount > 0 else 10000))

# --- Filtering Logic ---
filtered_expenses = st.session_state.expenses

if search_query:
    filtered_expenses = [e for e in filtered_expenses if search_query.lower() in e["Expense Name"].lower()]

if selected_category != "All":
    filtered_expenses = [e for e in filtered_expenses if e["Category"] == selected_category]

filtered_expenses = [e for e in filtered_expenses if amount_range[0] <= e["Amount"] <= amount_range[1]]

# --- Task 2: Dashboard Summary ---
st.header("Dashboard Summary")

if not st.session_state.expenses:
    st.warning("No expenses added yet. Please add an expense to see dashboard.")
    total_exp = 0
    total_trans = 0
    highest_exp = 0
else:
    total_exp = sum([e["Amount"] for e in st.session_state.expenses])
    total_trans = len(st.session_state.expenses)
    highest_exp = max([e["Amount"] for e in st.session_state.expenses])

col1, col2, col3 = st.columns(3)
col1.metric("Total Expenses", f"Rs {total_exp}")
col2.metric("Total Transactions", total_trans)
col3.metric("Highest Expense", f"Rs {highest_exp}")

# --- Task 6: Category-wise Summary ---
st.subheader("Category-wise Total")
if st.session_state.expenses:
    categories = ["Food", "Travel", "Shopping", "Bills", "Other"]
    for cat in categories:
        cat_total = sum([e["Amount"] for e in st.session_state.expenses if e["Category"] == cat])
        if cat_total > 0:
            st.write(f"**{cat}:** Rs {cat_total}")
else:
    st.write("No data for category summary.")

st.divider()

# --- Task 3 & 5: Expense Records + Delete ---
st.header("Expense Records")

if not filtered_expenses:
    st.warning("No expense records found for selected filters.")
else:
    st.dataframe(filtered_expenses, use_container_width=True)

    st.subheader("Delete Expense")
    for i, exp in enumerate(filtered_expenses):
        # Find original index
        original_index = st.session_state.expenses.index(exp)
        if st.button(f"Delete - {exp['Expense Name']} - Rs {exp['Amount']} ({exp['Date']})", key=f"del_{original_index}"):
            delete_expense(original_index)
            st.success("Expense deleted successfully!")
            st.rerun()

# --- Task 6: Highest Expense Display ---
if st.session_state.expenses:
    highest_expense_record = max(st.session_state.expenses, key=lambda x: x["Amount"])
    st.divider()
    st.subheader("Highest Expense Detail")
    st.error(f"Highest: {highest_expense_record['Expense Name']} - Rs {highest_expense_record['Amount']} on {highest_expense_record['Date']}")

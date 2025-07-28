import mysql
import streamlit as st
from mysql.connector import *
from modules.speak import speak


def Bms():
    def create_connection():
        connection = None
        try:
            connection = mysql.connector.connect(host="localhost",user="root",password="R@ghav_2005",database="bms")
        except Error as e:
            st.error(f"The error '{e}' occurred")
        return connection
    def get_users(connection):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    def create_user(connection, name, email, balance):
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, balance) VALUES (%s, %s, %s)", (name, email, balance))
            connection.commit()
        except Error as e:
            st.error(f"Error creating user: {e}")
    def add_transaction(connection, user_id, type, amount):
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)", (user_id, type, amount))
            connection.commit()
        except Error as e:
            st.error(f"Error adding transaction: {e}")
    def update_balance(connection, user_id, amount, is_deposit=True):
        cursor = connection.cursor()
        try:
            if is_deposit:
                cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
            else:
                cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_id))
            connection.commit()
        except Error as e:
            st.error(f"Error updating balance: {e}")
    def get_transactions(connection, user_id):
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transactions WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        return cursor.fetchall()
    def Bms_main():
        st.title("Banking Management System")
        connection = create_connection()
        if connection is None:
            st.error("Failed to connect to the database. Please check the connection settings.")
            return
        menu = ["Create User", "View Users", "Deposit", "Withdraw", "View Transactions"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Create User":
            st.subheader("Create New User")
            name = st.text_input("Name")
            email = st.text_input("Email")
            balance = st.number_input("Initial Balance", min_value=0.0)
            if st.button("Create"):
                create_user(connection, name, email, balance)
                msg=f"User {name} created successfully with balance {balance}"
                st.success(msg)
                speak(text="User Created Successfully")
        elif choice == "View Users":
            st.subheader("View All Users")
            users = get_users(connection)
            for user in users:
                st.write(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Balance: {user['balance']}")
        elif choice == "Deposit":
            st.subheader("Deposit Money")
            user_id = st.number_input("User ID", min_value=1)
            amount = st.number_input("Amount", min_value=0.01)
            if st.button("Deposit"):
                if amount <= 0:
                    speak(text="Amount should be greater than zero")
                    st.error("Amount should be greater than zero")
                else:
                    add_transaction(connection, user_id, 'deposit', amount)
                    update_balance(connection, user_id, amount, is_deposit=True)
                    msg= f"Deposited {amount} to user ID {user_id}"
                    st.success(msg)
                    speak(msg)
        elif choice == "Withdraw":
            st.subheader("Withdraw Money")
            user_id = st.number_input("User ID", min_value=1)
            amount = st.number_input("Amount", min_value=0.01)
            if st.button("Withdraw"):
                if amount <= 0:
                    speak(text="Amount should be greater than zero")
                    st.error("Amount should be greater than zero")
                else:
                    cursor = connection.cursor()
                    cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
                    user_balance = cursor.fetchone()
                    if user_balance[0] >= amount:
                        add_transaction(connection, user_id, 'withdrawal', amount)
                        update_balance(connection, user_id, amount, is_deposit=False)
                        st.success(f"Withdrew {amount} from user ID {user_id}")
                        speak(text=f"Withdrew {amount} from user ID {user_id}")
                    else:
                        speak("Insufficient balance or user not found")
                        st.error("Insufficient balance or user not found")
        elif choice == "View Transactions":
            st.subheader("View User Transactions")
            user_id = st.number_input("User ID", min_value=1)
            if st.button("View Transactions"):
                transactions = get_transactions(connection, user_id)
                if transactions:
                    for transaction in transactions:
                        st.write(f"ID: {transaction['id']}, Type: {transaction['type']}, Amount: {transaction['amount']}, Date: {transaction['created_at']}")
                else:
                    speak("No transactions found for this user.")
                    st.write("No transactions found for this user.")
        connection.close()
    Bms_main()


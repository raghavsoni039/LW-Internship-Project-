import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
def ml():
    st.subheader("📊 Machine Learning Module")
    # Sidebar menu to select predictor
    option = st.sidebar.selectbox(
        "Select a Predictor:",
        ["Marks Predictor", "Startup Profit Predictor"]
    )
    # MARKS PREDICTOR
    if option == "Marks Predictor":
        st.subheader("📘 Marks Predictor based on Study Hours")

        try:
            data = pd.read_csv("marks.csv")
        except Exception as e:
            st.error(f"Error loading 'marks.csv': {e}")
            return

        x = data["hrs"].values.reshape(-1, 1)
        y = data["marks"].values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(x, y)

        hours = st.number_input("📚 Enter hours of study:", min_value=0.0, step=0.5)

        if hours <= 10:
            if st.button("🎯 Predict Marks"):
                prediction = model.predict([[hours]])
                st.success(f"Predicted Marks for {hours} hours: **{prediction[0][0]:.2f}%**")
        else:
            st.error("❌ Hours must be less than or equal to 10.")

    # STARTUP PROFIT PREDICTOR
    elif option == "Startup Profit Predictor":
        st.subheader("💼 Startup Profit Predictor")

        try:
            df = pd.read_csv("50_Startups.csv")
        except Exception as e:
            st.error(f"Error loading '50_Startups.csv': {e}")
            return

        df = pd.get_dummies(df, columns=["State"], drop_first=False)
        X = df.drop("Profit", axis=1)
        Y = df["Profit"]

        model = LinearRegression()
        model.fit(X, Y)

        state_cols = [col for col in X.columns if "State_" in col]
        state_names = [col.replace("State_", "") for col in state_cols]

        st.markdown("### 🔧 Input Parameters")

        rd_spend = st.number_input("R&D Spend", min_value=0.0, value=100000.0, step=1000.0)
        admin = st.number_input("Administration Cost", min_value=0.0, value=100000.0, step=1000.0)
        marketing = st.number_input("Marketing Spend", min_value=0.0, value=400000.0, step=1000.0)
        user_state = st.selectbox("State", state_names)

        if st.button("💡 Predict Profit"):
            input_data = {
                'R&D Spend': rd_spend,
                'Administration': admin,
                'Marketing Spend': marketing
            }

            for col in state_cols:
                input_data[col] = 1 if col == f"State_{user_state}" else 0

            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]

            st.success(f"✅ Predicted Profit: **${prediction:,.2f}**")

            with st.expander("📊 Show Model Coefficients"):
                coef_df = pd.DataFrame({
                    "Feature": X.columns,
                    "Coefficient": model.coef_
                })
                st.dataframe(coef_df, use_container_width=True)

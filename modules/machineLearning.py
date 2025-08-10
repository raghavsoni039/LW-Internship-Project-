import streamlit as st
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

def ml():
    st.subheader("📊 Machine Learning Module")

    # Sidebar menu to select predictor
    option = st.sidebar.selectbox(
        "Select a Predictor:",
        ["Marks Predictor", "Startup Profit Predictor", "Titanic Survival Predictor"]
    )

    # ------------------------------
    # MARKS PREDICTOR
    # ------------------------------
    if option == "Marks Predictor":
        st.subheader("📘 Marks Predictor based on Study Hours")
        try:
            data = pd.read_csv("assets/marks.csv")
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

    # ------------------------------
    # STARTUP PROFIT PREDICTOR
    # ------------------------------
    elif option == "Startup Profit Predictor":
        st.subheader("💼 Startup Profit Predictor")
        try:
            df = pd.read_csv("assets/50_Startups.csv")
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

    # ------------------------------
    # TITANIC SURVIVAL PREDICTOR
    # ------------------------------
    elif option == "Titanic Survival Predictor":
        st.subheader("🚢 Titanic Survival Predictor")

        try:
            dataset = pd.read_csv("assets/Titanic-Dataset.csv")
        except Exception as e:
            st.error(f"Error loading 'Titanic-Dataset.csv': {e}")
            return

        # Target and features
        y = dataset["Survived"]
        x = dataset[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch']]

        # Fill missing ages based on Pclass
        def set_age(data): 
            if pd.isnull(data[1]):
                if data[0] == 1: return 38
                elif data[0] == 2: return 29
                elif data[0] == 3: return 25
            return data[1]

        x['Age'] = x[["Pclass", "Age"]].apply(func=set_age, axis=1)

        # Encoding categorical variables
        gender = pd.get_dummies(x["Sex"])
        x.drop('Sex', axis=1, inplace=True)
        x[['female', 'male']] = gender

        classes = pd.get_dummies(x["Pclass"])
        x[['1stclass', '2ndclass', '3rdclass']] = classes
        x.drop("Pclass", axis=1, inplace=True)

        sibling = pd.get_dummies(x['SibSp'])
        x[['sib0', 'sib1', 'sib2', 'sib3', 'sib4', 'sib5', 'sib8']] = sibling
        x.drop("SibSp", axis=1, inplace=True)

        parch = pd.get_dummies(x['Parch'])
        x[['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6']] = parch
        x.drop("Parch", axis=1, inplace=True)

        # Train model
        model = LogisticRegression()
        model.fit(x, y)

        st.markdown("### 🔧 Input Passenger Details")
        age = st.number_input("Age", min_value=0, max_value=100, value=30)
        sex = st.selectbox("Sex", ["male", "female"])
        pclass = st.selectbox("Passenger Class", [1, 2, 3])
        sibsp = st.selectbox("Number of Siblings/Spouses Aboard", [0, 1, 2, 3, 4, 5, 8])
        parch_val = st.selectbox("Number of Parents/Children Aboard", [0, 1, 2, 3, 4, 5, 6])

        if st.button("🔮 Predict Survival"):
            # Prepare input row
            input_data = {
                "Age": age,
                "female": 1 if sex == "female" else 0,
                "male": 1 if sex == "male" else 0,
                "1stclass": 1 if pclass == 1 else 0,
                "2ndclass": 1 if pclass == 2 else 0,
                "3rdclass": 1 if pclass == 3 else 0,
                "sib0": 1 if sibsp == 0 else 0,
                "sib1": 1 if sibsp == 1 else 0,
                "sib2": 1 if sibsp == 2 else 0,
                "sib3": 1 if sibsp == 3 else 0,
                "sib4": 1 if sibsp == 4 else 0,
                "sib5": 1 if sibsp == 5 else 0,
                "sib8": 1 if sibsp == 8 else 0,
                "p0": 1 if parch_val == 0 else 0,
                "p1": 1 if parch_val == 1 else 0,
                "p2": 1 if parch_val == 2 else 0,
                "p3": 1 if parch_val == 3 else 0,
                "p4": 1 if parch_val == 4 else 0,
                "p5": 1 if parch_val == 5 else 0,
                "p6": 1 if parch_val == 6 else 0
            }

            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]

            if prediction == 1:
                st.success("✅ This passenger is likely to survive.")
            else:
                st.error("❌ This passenger is unlikely to survive.")

        # Train-test split & confusion matrix
        X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.25, random_state=104, shuffle=True)
        y_pred = model.predict(X_test)
        cm = confusion_matrix(Y_test, y_pred)
        with st.expander("📊 Show Confusion Matrix"):
            st.write(pd.DataFrame(cm, index=["Actual: No", "Actual: Yes"], columns=["Predicted: No", "Predicted: Yes"]))

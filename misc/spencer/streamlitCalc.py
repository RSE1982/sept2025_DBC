import math
import streamlit as st

st.set_page_config(page_title="Not so simple calculator", page_icon="🧮")
st.write("The is slightly more useful than a simple calculator")
st.divider()

# Input area
col1, col2, col3 = st.columns(3)

with col1:
    num1 = st.number_input("Enter first number:", value=0.0, step=1.0)
with col2:
    num2 = st.number_input("Enter second number:", value=0.0, step=1.0)
with col3:
    operation = st.selectbox(
        "Select an operation",
        [
            "Add",
            "Subtract",
            "Multiply",
            "Divide",
            "Power (x)",
            "Square Root",
            "Modulus (Remainder)",
            "Average",
        ]
    )

if st.button("Calculate"):
    result = None
    explanation = ""

    try:
        if operation == "Add":
            result = num1 + num2
            explanation = f"{num1} + {num2} = {result}"
        elif operation == "Subtract":
            result = num1 - num2
            explanation = f"{num1} - {num2} = {result}"
        elif operation == "Multiply":
            result = num1 * num2
            explanation = f"{num1} * {num2} = {result}"
        elif operation == "Divide":
            if num2 == 0:
                st.error("You can't divide by zero!")
            else:
                result = num1 / num2
                explanation = f"{num1} / {num2} = {result}"
        elif operation == "Power (x)":
            result = num1 ** num2
            explanation = f"{num1} to the power of {num2} = {result}"
        elif operation == "Square Root":
            if num1 < 0:
                st.error("Cannot take the square root of a negative number")
            else:
                result = math.sqrt(num1)
                explanation = f"square root of {num1} = {result}"
        elif operation == "Modulus (Remainder)":
            result = num1 % num2
            explanation = f"The remainder of {num1} divided by {num2} = {result}"
        elif operation == "Average":
            result = (num1 + num2) / 2
            explanation = f"The average of {num1} and {num2} = {result}"
        # display the result
        if result is not None:
            st.success(f"Result: {result}")
            st.info(explanation)

            # store calculation history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append(explanation)
    except Exception as e:
        st.error(f"Error: {str(e)}")

# history section
st.divider()
st.subheader("Calculation History")

if "history" in st.session_state and st.session_state.history:
    for i, calc in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.write(f"{calc}")
else:
    st.write("No calculation yet.")

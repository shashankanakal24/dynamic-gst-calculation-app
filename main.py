
import pyrebase
import streamlit as st
from datetime import datetime
import requests


#Configuration Key
firebaseConfig = {
  'apiKey': "*********************************",
  'authDomain': "***********************",
  'projectId': "*************************",
'databaseURL':"******************************8",
  'storageBucket': "***************************",
  'messagingSenderId': "****************",
  'appId': "*********************",
  'measurementId': "***************"
};
def send_query_to_flask(user_input):
    print(user_input)
    url = 'http://localhost:5000/test'  # Replace with your Flask server URL
    payload = {'user_input': user_input}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("response", response)
        return response.json().get('result')
    else:
        return f'Error: {response.status_code} - {response.reason}'

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

# Streamlit app
st.sidebar.title("Our GST Calculator")

# Authentication
choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])

# Obtain User Input for email and password
email = st.sidebar.text_input('Please enter your email address')
password = st.sidebar.text_input('Please enter your password', type='password')

# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input('Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created successfully!')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome ' + handle)
        st.info('Login via login drop down selection')

# Login Block
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        bio = st.radio('Jump to', ['Simple Calculator', 'Chatbot', 'Read me', 'Settings'])

        # SETTINGS PAGE
        if bio == 'Settings':
            language_choice = st.selectbox('Select Language of the App', options=['English (Default)', 'Kannada', 'Telugu', 'Marathi', 'Tamil'])

            # Button to confirm language selection
            if st.button('Change Language'):
                st.write(f"Language changed to {language_choice}")

            st.text("")
            st.text("")
            st.text("")
            st.text("")

            st.button('Log Out')

        # SIMPLE CALCULATOR PAGE
        if bio == 'Simple Calculator':
            inbio = st.radio('Jump to', ['Inclusive', 'Exclusive'])
            if inbio == 'Exclusive':
                st.title('Exclusive GST Calculator')
                # Input box for the amount
                amount = st.number_input('Enter the amount:', step=1.0, format="%.2f")

                # Input box for GST rate
                gst_rate = st.number_input('Enter GST rate (%):', step=1.0, format="%.2f")

                # Calculate button
                calculate = st.button('Calculate')

                # Output box
                output = st.empty()

                # Display output when Calculate button is clicked
                if calculate:
                    if amount and gst_rate:
                        gst_amount = (amount * gst_rate) / 100
                        total_amount = amount + gst_amount
                        output.text(f'The GST amount is: {gst_amount:.2f} and the total amount is: {total_amount:.2f}')
                    else:
                        st.warning("Please enter both the amount and the GST rate.")

            if inbio == 'Inclusive':
                st.title('Inclusive GST Calculator')
                amount = st.number_input('Enter the amount:', step=1.0, format="%.2f")

                # Input box for GST rate
                gst_rate = st.number_input('Enter GST rate (%):', step=1.0, format="%.2f")

                # Calculate button
                calculate = st.button('Calculate')

                # Output box
                output = st.empty()

                # Display output when Calculate button is clicked
                if calculate:
                    if amount and gst_rate:
                        gst_amount = amount * (gst_rate / (100 + gst_rate))
                        base_amount = amount - gst_amount
                        output.text(f'The base amount is: {base_amount:.2f} and the GST amount is: {gst_amount:.2f}')
                    else:
                        st.warning("Please enter both the amount and the GST rate.")

        # CHATBOT PAGE
        if bio == 'Chatbot':
            st.title('Welcome to GST Chat Assistance')

            # Create a placeholder for user input
            user_input = st.text_input('Type your message here...')

            # Create a sidebar column for the search button
            col1, col2 = st.columns([5, 1])
            with col2:
                search_button = st.button('Search')

            # Logic to perform action when the button is clicked
            if search_button:
                if user_input:
                    result = send_query_to_flask(user_input)
                    st.info(result)
                else:
                    st.warning('Please enter a query before searching.')

        # READ ME PAGE
        if bio == 'Read me':
            st.title("GST Information")

            st.write("### What is GST?")
            st.write(
                "Goods and Services Tax (GST) is a comprehensive, multi-stage, destination-based tax that is levied on every value addition. It replaced many indirect taxes in India, simplifying the taxation system and promoting ease of doing business. GST is divided into three categories: CGST (Central GST), SGST (State GST), and IGST (Integrated GST).")

            st.write("### What is a GST Calculator?")
            st.write(
                "A GST Calculator is a tool designed to compute the Goods and Services Tax on various goods and services. By entering the net amount and the applicable GST rate, users can easily determine the total tax amount and the gross price.")

            st.write("[Read more about GST](https://www.india.gov.in/spotlight/goods-and-services-tax-gst)")

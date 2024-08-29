# import streamlit as st
# import pandas as pd
# from nixtla import NixtlaClient
# from dotenv import load_dotenv
# from streamlit.web import cli as stcli
# import os

# # Load environment variables from .env file
# load_dotenv()

# api_key = os.getenv('NIXTLA_API_KEY')
# if not api_key:
#     st.error("API Key not found. Please check your .env file.")
# else:
#     nixtla_client = NixtlaClient(api_key=api_key)

#     # File uploader
#     uploaded_file = st.file_uploader("Choose a file - accepts either CSV or Dataframe")
#     if uploaded_file is not None:
#         if uploaded_file.name.endswith('.csv'):
#             def load_data(uploaded_file):
#                 try:
#                     return pd.read_csv(uploaded_file)
#                 except Exception as e:
#                     st.error(f"Error reading {uploaded_file.name}: {e}")
#                     return None

#             df = load_data(uploaded_file)
#             if df is not None:
#                 st.write("Uploaded Dataset Preview:", df.head())

#                 # User input for forecast horizon
#                 h = st.number_input('Enter the forecast horizon (in months):', min_value=1, value=12)

#                 # Button to perform forecasting
#                 if st.button('Forecast'):
#                     forecast_df = nixtla_client.forecast(df=df, h=h, freq='MS', time_col='timestamp', target_col='value')
#                     st.write("Forecasted Data:", forecast_df.head())
#                     # Plot results
#                     nixtla_client.plot(df, forecast_df, time_col='timestamp', target_col='value')
#         else:
#             st.error("Please upload a correct file (csv or dataframe) format.")
#     else:
#         st.write("Upload a pandas dataframe or csv file to begin.")



# import streamlit as st
# import pandas as pd
# from nixtla import NixtlaClient
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# # Initialize the Nixtla client using the API key from the environment variable
# api_key = os.getenv('NIXTLA_API_KEY')
# if not api_key:
#     st.error("API Key not found. Please check your .env file.")
# else:
#     nixtla_client = NixtlaClient(api_key=api_key)

#     # File uploader
#     uploaded_file = st.file_uploader("Choose a CSV file")
#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)
#         st.write("Uploaded Dataset Preview:", df.head())

#         # User input for forecast horizon
#         h = st.number_input('Enter the forecast horizon (in months):', min_value=1, value=12, step=1)

#         # Display recommendation based on the input horizon
#         if h > 12:
#             st.info("We recommend using the 'Long-Horizon Model' for forecasts longer than 12 months.")
#         else:
#             st.info("The 'Standard Model' is suitable for forecasts up to 12 months.")

#         # Dropdown for model selection
#         model_option = st.selectbox(
#             'Choose the forecasting model:',
#             ('Standard Model', 'Long-Horizon Model')
#         )

#         # Map selection to model names used by the API
#         model_dict = {
#             'Standard Model': 'timegpt-1',
#             'Long-Horizon Model': 'timegpt-1-long-horizon'
#         }
#         selected_model = model_dict[model_option]

#         # Button to perform forecasting
#         if st.button('Forecast'):
#             forecast_df = nixtla_client.forecast(df=df, h=h, freq='MS', time_col='timestamp', target_col='value', model=selected_model)
#             st.write("Forecasted Data:", forecast_df.head())
#             # Plot results
#             nixtla_client.plot(df, forecast_df, time_col='timestamp', target_col='value')
#     else:
#         st.write("Upload a CSV file to begin.")

# import streamlit as st
# import pandas as pd
# from nixtla import NixtlaClient
# from dotenv import load_dotenv
# import os
# import matplotlib.pyplot as plt

# # Load environment variables from .env file
# load_dotenv()

# # Initialize the Nixtla client using the API key from the environment variable
# api_key = os.getenv('NIXTLA_API_KEY')
# if not api_key:
#     st.error("API Key not found. Please check your .env file.")
# else:
#     nixtla_client = NixtlaClient(api_key=api_key)

#     # File uploader
#     uploaded_file = st.file_uploader("Choose a CSV file")
#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)
#         st.write("Uploaded Dataset Preview:", df.head())

#         # Frequency and model selections
#         freq_option = st.selectbox('Choose the forecast frequency:', ('Daily', 'Weekly', 'Monthly'), index=2)

#         st.info(f"Please ensure your dataset's frequency matches the selected '{freq_option}' frequency for accurate forecasting.")

#         model_option = st.selectbox('Choose the forecasting model:', ('Standard Model', 'Long-Horizon Model'))
#         model_dict = {'Standard Model': 'timegpt-1', 'Long-Horizon Model': 'timegpt-1-long-horizon'}
#         selected_model = model_dict[model_option]

        
#         # User input for forecast horizon
#         h = st.number_input('Enter the forecast horizon:', min_value=1, value=12)

#         if freq_option == 'Monthly' and h > 12:
#             st.info("The 'Long-Horizon Model' is suitable for forecasts longer than 12 months.")
#         else:
#             st.info("The 'Standard Model' is suitable for forecasts up to 12 months.")

#         # Forecast button
#         if st.button('Forecast'):
#             try:
#                 forecast_df = nixtla_client.forecast(df=df, h=h, freq=freq_option[0], time_col='timestamp', target_col='value', model=selected_model)
#                 forecast_df.rename(columns={'TimeGPT': 'value'}, inplace=True)
#                 st.session_state.forecast_df = forecast_df
#                 st.session_state.forecast_displayed = True
#                 st.session_state.future_dates = pd.date_range(start=pd.to_datetime(df['timestamp'].iloc[-1]), periods=h+1, freq=freq_option[0])[1:]
#                 st.write("Forecasted Data:", forecast_df.head())
#             except Exception as e:
#                 st.error("An error occurred while forecasting. Please check your data and settings.")
        
#         # Display forecast results if available
#         if 'forecast_displayed' in st.session_state and st.session_state.forecast_displayed:
#             st.write("Forecasted Data:", st.session_state.forecast_df.head())

#         # Plot button and logic
#         if st.button('Plot Results'):
#             try:
#                 if 'forecast_df' in st.session_state:
#                     plt.figure(figsize=(10, 5))
#                     plt.plot(pd.to_datetime(df['timestamp']), df['value'], label='Historical Data')
#                     plt.plot(st.session_state.future_dates, st.session_state.forecast_df['value'], label='Forecast', linestyle='--')
#                     plt.title('Historical and Forecasted Values')
#                     plt.xlabel('Date')
#                     plt.ylabel('Value')
#                     plt.legend()
#                     st.pyplot(plt)
#                     st.session_state.plot_displayed = True
#             except Exception as e:
#                 st.error("An error occurred while plotting. Please try again.")

#     else:
#         st.write("Upload a CSV file to begin.")


import streamlit as st
import pandas as pd
from nixtla import NixtlaClient
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

# Initialize the Nixtla client using the API key from the environment variable
api_key = os.getenv('NIXTLA_API_KEY')
if not api_key:
    st.error("API Key not found. Please check your .env file.")
else:
    nixtla_client = NixtlaClient(api_key=api_key)

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Dataset Preview:", df.head())

        # Frequency and model selections
        freq_option = st.selectbox('Choose the forecast frequency:', ('Daily', 'Weekly', 'Monthly'), index=2)
        model_option = st.selectbox('Choose the forecasting model:', ('Standard Model', 'Long-Horizon Model'))
        model_dict = {'Standard Model': 'timegpt-1', 'Long-Horizon Model': 'timegpt-1-long-horizon'}
        selected_model = model_dict[model_option]

        # User input for forecast horizon
        h = st.number_input('Enter the forecast horizon:', min_value=1, value=12)

        # Initialize session state for plot display
        if 'plot_displayed' not in st.session_state:
            st.session_state.plot_displayed = False

        # Forecast button
        if st.button('Forecast'):
            try:
                forecast_df = nixtla_client.forecast(df=df, h=h, freq=freq_option[0], time_col='timestamp', target_col='value', model=selected_model)
                forecast_df.rename(columns={'TimeGPT': 'value'}, inplace=True)
                st.session_state.forecast_df = forecast_df
                st.session_state.forecast_displayed = True
                st.session_state.future_dates = pd.date_range(start=pd.to_datetime(df['timestamp'].iloc[-1]), periods=h+1, freq=freq_option[0])[1:]
                st.success("Forecast successful!")
            except Exception as e:
                st.error("An error occurred while forecasting. Please check your data and settings.")

        # Display forecast results if forecast was successful
        if 'forecast_displayed' in st.session_state and st.session_state.forecast_displayed:
            st.write("Forecasted Data:", st.session_state.forecast_df.head())

        # Plot button and logic
        if st.button('Plot Results') or st.session_state.plot_displayed:
            if 'forecast_df' in st.session_state:
                try:
                    plt.figure(figsize=(10, 5))
                    plt.plot(pd.to_datetime(df['timestamp']), df['value'], label='Historical Data')
                    plt.plot(st.session_state.future_dates, st.session_state.forecast_df['value'], label='Forecast', linestyle='--')
                    plt.title('Historical and Forecasted Values')
                    plt.xlabel('Date')
                    plt.ylabel('Value')
                    plt.legend()
                    st.pyplot(plt)
                    st.session_state.plot_displayed = True
                except Exception as e:
                    st.error("An error occurred while plotting. Please try again.")

    else:
        st.write("Upload a CSV file to begin.")
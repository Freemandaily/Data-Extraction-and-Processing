import time
import streamlit as st
import sys
from TweetData import processor
from priceFeed import token_tweeted_analyzor
from storage import add_to_csv



st.header('Data-Extraction and Processing')
with st.sidebar:
    st.title('Data Configuration')
    username = st.text_input('Enter Influencer X handle\n')
    timeframe = st.selectbox('Choose A TimeFrame',[7,30,90])
    token_choice = st.radio('Search From',['Strict Token','All Tokens'])
    st.divider()
    st.subheader('About')
    About = """
    The Analyst module is tool designed to analyse the impact of influencer tweet on a particular solana based token.
    Built wih the focused on the solana blockchain,the tool scans the twitter activities of the specified influencer within a choosen timeframe and extracts,
    symbols and contract Address(CAs) mentioned in the posts then correlate this mentions with the real times price action
    at 5-minute,10-minute and 15-minuts interval to reveal the impact.
    """

    # def stream():
    #     for word in About.split(" "):
    #         yield word + ' '
    #         time.sleep(0.002)
  
    # @st.fragment       
    # def display():
    #     st.write_stream(stream())

    # display()
    st.write(About)

st.image('data-extract.png')



if st.button('Analyse Tweet'):
    process = processor()
    if not username:
        st.error('Please Enter A Username')
        st.stop()
    else:
        with st.spinner(f'Loading @{username} Handle'):
            userHandler = process.Load_user(username,timeframe=timeframe) 
        if 'Error' in userHandler:
            st.error(userHandler['Error'])
            st.stop() 
        pass
            
    with st.spinner(f'Processing @{username} Tweets'):
        tweeted_token_details = process.processTweets()

    if 'Error' in tweeted_token_details:
        st.error(tweeted_token_details['Error'])
        st.stop()
    else:
        st.toast(f'@{username} Tweets Successfully Processed!')
    # tweeted_token_details = {'2025-04-22 14:27:35':{'Token_names':['$sol','$ray','$wif','$jup'],'contracts':[]}}
    
    # Fetchng tweeted token data
    with st.spinner('Fetching Tweeted Tokens and Price Datas. Please Wait.....'):
        analyzor = token_tweeted_analyzor(tweeted_token_details,token_choice)
    if 'Error' in analyzor:
        st.error(analyzor['Error'])
        st.stop()

    with st.spinner('Storing Tweeted Token(s) Data'):  
        df_data = add_to_csv(username,analyzor)  # Adding the tweeted token to cs file
    if 'Error' in df_data:
        st.error(df_data['Error'])
        st.stop()
    st.success( 'Succesfully Analyzed Tweeted Token(s)',icon="✅")
    time.sleep(5)
    st.dataframe(df_data)


    def convert_for_download(df_data):
        return df_data.to_csv().encode("utf-8")
    csv = convert_for_download(df_data)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
        icon=":material/download:"
    )


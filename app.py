import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

st.sidebar.title("Whatsapp chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_msgs, num_words, num_media = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Total Messages")
            st.title(num_msgs)
        with col2:
            st.header("Total words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)

        colM, colD = st.columns(2)
        with colM:
            # timeline
            st.subheader("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='g')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with colD:

            # daily timeline
            st.subheader("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # activity map
        st.title('Activity Map')
        colmbd, colmbm = st.columns(2)
        with colmbd:
            st.subheader("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with colmbm:
            st.subheader("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.subheader('Weekly Activity')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(user_heatmap)
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)
        # Finding busiest user
        if selected_user == 'Overall':
            st.header('Most Busy Users')
            x, new_df = helper.busy(df)
            name = x.index
            count = x.values
            fig, ax = plt.subplots()
            colA, colB = st.columns(2)
            with colA:
                ax.bar(name, count, color='teal', width=0.5)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with colB:
                fig, ax = plt.subplots()
                ax.pie(new_df['percent'], labels=new_df.index)
                st.dataframe(new_df)
                st.pyplot(fig)
        st.title('Most used words')
        new_df2 = helper.most_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(new_df2[0], new_df2[1], color='turquoise')

        st.pyplot(fig)

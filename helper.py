import pandas as pd

from collections import Counter


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    return num_messages, num_words, num_media


def busy(df):
    x = df['user'].value_counts().head()
    y = df['user'].value_counts()
    nameper = y.index
    countper = y.values
    sum1 = sum(countper)
    contribution = [round((i / sum1) * 100, 2) for i in countper]
    new_df = pd.DataFrame(contribution, nameper, columns=(['percent']))
    return x,new_df


def most_words(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']== selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        words.extend(message.split())
    for i in words:
        if len(i) < 4:
            words.remove(i)
    from collections import Counter
    new_df2 = pd.DataFrame(Counter(words).most_common(20))
    return new_df2


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df [df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df [df['user'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df ['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap


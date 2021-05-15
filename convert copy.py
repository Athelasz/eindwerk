import string


def inv_tojson(sheet):
    #import json module to convert dict to json in the end
    import json
    #import pandas read_excel module to inject an excel into a DataFrame
    from pandas import read_excel
    # make sure we use the first sheet as source for our dataframe
    df = read_excel(sheet,sheet_name=0)
    d = {}
    # for every unique meeting collect all attendees in one list of dictionaries
    # with the needed key-value pairs
    for meeting in df['name_meeting'].unique():
        d[meeting] = [{
        'fn': df['fn_participant'][item],
        'sn': df['sn_participant'][item],
        'email': df['email_participant'][item]} 
        for item in df[df['name_meeting']==meeting].index]
    # convert dict in json
    d_json = json.dumps(d)
    #return json to be further processed
    return d_json

def inv_todict(sheet):
    #import pandas read_excel module to inject an excel into a DataFrame
    from pandas import read_excel
    # make sure we use the first sheet as source for our dataframe
    df = read_excel(sheet,sheet_name=0)
    d = {}
    # for every unique meeting collect all attendees in one list of dictionaries
    # with the needed key-value pairs
    for meeting in df['name_meeting'].unique():
        d[meeting] = [{
        'fn': df['fn_participant'][item],
        'sn': df['sn_participant'][item],
        'email': df['email_participant'][item]} 
        for item in df[df['name_meeting']==meeting].index]
    #return dict to be further processed
    return d

def meet_todict(sheet):
    #import pandas read_excel module to inject an excel into a DataFrame
    sheet = 'list_webex.xlsx'
    from pandas import read_excel,to_datetime,Timestamp
    # make sure we use the first sheet as source for our dataframe
    df = read_excel(sheet,sheet_name=0,usecols=['name_meeting','date_meeting','start_hour','end_hour'])
    df.drop_duplicates(subset='name_meeting',inplace=True)
    df['start'] = to_datetime(df['date_meeting']+' '+df['start_hour'])
    df['end']   = to_datetime(df['date_meeting']+' '+df['end_hour'])
    d = {}

    # set tz to convert date column to ISO8601 extended string
    df['start'] = df['start'].apply(lambda d: Timestamp(d, tz = 'Europe/Brussels').isoformat())
    df['end']   = df['end'].apply(lambda d: Timestamp(d, tz = 'Europe/Brussels').isoformat())
    
    for i in df.index:
        d[df['name_meeting'][i]] = [{
        'start': df['start'][i],
        'end': df['end'][i]}
        ]

    # for every unique meeting collect all attendees in one list of dictionaries
    # with the needed key-value pairs
    #d = df.to_dict
    #return dict to be further processed
    return d

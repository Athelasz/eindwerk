from timeit import Timer
from pandas import read_excel,to_datetime,Timestamp

tzone_str = 'Europe/Brussels'
sheet = 'list_webex.xlsx'
site = 'eindwerk.webex.com'

def parse_time(cols, df, tzo):
    col_list = []
    for c in cols:

        date = to_datetime(df['date_meeting']+' '+df[c+'_hour'])

        col_list.append(date.apply(lambda d: Timestamp(d, tz = tzo).isoformat()))
    return col_list

def inv_select(df):
    inv_dic = {}
    # per meeting collect all attendees in one list of dictionaries
    for mt_name in df['name_meeting'].unique():
        inv_dic[mt_name] = [{
        'displayname': item.fn_participant+' '+item.sn_participant,
        'email': item.email_participant,
        'coHost' : item.host
        }
        for item in df[df['name_meeting']==mt_name].itertuples()]    
    return inv_dic

def main():
    t = Timer()
    #read excel file to panda dataframe
    df = read_excel(sheet,sheet_name=0, dtype=str)
    #transform date and time to iso dates
    df['end'],df['start'] = parse_time(['end','start'], df, tzone_str)
    inv_dict = inv_select(df)
    d = {}
    # loop through a unique meeting list created from the df object
    for name in df['name_meeting'].unique():
        #create a subset containing only the rows linked to this meeting
        for mt in df[df['name_meeting']==name].itertuples():
            #per unique meeting create one dictionary object
            d[name] = {
            'title': name,
            'start': mt.start,
            'end'  : mt.end,
            'timezone': tzone_str,
            'enabledAutoRecordMeeting': False,
            'allowAnyUserToBeCoHost': False,
            #'siteUrl': site,
            'sendEmail': False,
            # per meeting collect all attendees in one list of dictionaries
            'invitees': inv_dict[name]}     
    print(t.timeit())
    #print(d)
    return d

# execute main when called directly
if __name__ == '__main__':
    main()


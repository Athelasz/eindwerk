from pandas import read_excel, to_datetime, Timestamp


def parse_time(cols, df, tzo):
    """**parse_time** - Function to parse strings to time zone aware 
    datetime objects, and then convert them to ISO8601 format strings

    :param cols: list of time columns
    :type cols: list
    :param df: source df to process
    :type df: DataFrame
    :param tzo: time zone
    :type tzo: string
    :return: list of modified columns
    :rtype: list
    """

UnicodeDecodeError
    col_list = []
    for c in cols:
        date = to_datetime(df['date_meeting']+' '+df[c+'_hour'])
        col_list.append(date.apply(lambda d: Timestamp(d, tz=tzo).isoformat()))
    return col_list


def inv_select(df):
    """**inv_select** - Per meeting collect all attendees in one 
    list of dictionaries

    :param df: dataframe to fetch data from
    :type df: DataFrame
    :return: nested dict with all attendees per meeting name
    :rtype: dict
    """
    inv_dic = {}
    for mt_name in df['name_meeting'].unique():
        inv_dic[mt_name] = [{
            'displayname': item.fn_participant+' '+item.sn_participant,
            'email': item.email_participant,
            'coHost': item.host
        }
            for item in df[df['name_meeting'] == mt_name].itertuples()]
    return inv_dic


def main(tzone_str='Europe/Brussels', sheet='list_webex.xlsx'):
    """**main** - Converts an excel file to a dict suitable for creating
    webex meetings via the Webex REST api

    :param tzone_str: desired timezone, defaults to 'Europe/Brussels'
    :type tzone_str: str, optional
    :param sheet: desired source file, defaults to 'list_webex.xlsx'
    :type sheet: str, optional
    :return: a nested dict of unique meetings + participants
    :rtype: dict
    """

    df = read_excel(sheet, sheet_name=0, dtype=str)
    df['end'], df['start'] = parse_time(['end', 'start'], df, tzone_str)
    inv_dict = inv_select(df)
    d = {}
    for name in df['name_meeting'].unique():
        for mt in df[df['name_meeting'] == name].itertuples():
            d[name] = {
                'title': name,
                'start': mt.start,
                'end': mt.end,
                'timezone': tzone_str,
                'enabledAutoRecordMeeting': False,
                'allowAnyUserToBeCoHost': False,
                'sendEmail': True,
                'invitees': inv_dict[name]}
    return d


# execute main when called directly
if __name__ == '__main__':
    main()

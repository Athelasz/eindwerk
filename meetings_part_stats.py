from environment import int_automation as env
import requests
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta  as r_delta
from pandas import pandas as pd, to_datetime as todate
import json

fail_req = []

def get_meetings():
    """**get_meetings** - Retrieve all meetings created by the chosen
    automation account.

    :return: all the meetings adhering to parameters
    :rtype: dict
    """
    params = meeting_params()
    url = "https://webexapis.com/v1/meetings"
    response = requests.get(url, headers=env['headers'], params=params)
    return json.loads(response.text)

def inv_count(meetingId):
    """**inv_count** - Count the invitees for a passed meeting id
    and return them as an integer. On error return 0.

    :param meetingId: a webex meeting
    :type meetingId: str
    :return: total count of invitees
    :rtype: int
    
    |

    """
    params = {
        'meetingId':meetingId,
        'max':100, 
        'hostEmail':env['hostEmail']
        }
    url = "https://webexapis.com/v1/meetingInvitees"
    invitees = requests.get(url, headers=env['headers'], params=params)
    if invitees.status_code == 200:
        inv_count = len(invitees.json()["items"])
        if 'next' in invitees.links:
            page = invitees.links['next']['url']
            while page:
                n_page = requests.get(page, headers=env['headers'], params=params)
                if n_page.status_code == 200:
                    inv_count += len(n_page.json()["items"])
                    if 'next' in n_page.links:
                        page = n_page.links['next']['url']
                    else:
                        page = False
        return inv_count
    else:
        fail_req.append(invitees.status_code)
        return 0


def part_list(meetingId):
    """**part_list** - Performs a GET to retrieve participants of the 
    passed meeting. Returns them as a list if available, 
    logs error code on fail

    :param meetingId: a webex meeting ID
    :type meetingId: str
    :return: the items key value from the get request
    :rtype: list

    |

    """
    url = "https://webexapis.com/v1/meetingParticipants"
    uri = f"{url}?meetingId={meetingId}"
    participants = requests.get(uri, headers=env['headers'])
    if participants.status_code == 200:
        part_dict = json.loads(participants.text)
        return(part_dict["items"])
    else:
        fail_req.append(participants.status_code)
        return None


def get_part_stats(m):
    """**get_part_stats** - Calculate amount of participants and minutes in 
    meeting info of passed meeting.

    :param m: a list of dictionaries with meeting details
    :type m: list
    :return: calculated participant count and attendance per meeting
    :rtype: dict
    
    |

    """
    parts = part_list(m["id"])
    if parts:
        parts_df = pd.DataFrame()
        for part in parts:
            part['devices'][0].update({'coHost': part["coHost"]})
            parts_df = parts_df.append(
                part['devices'][0],
                ignore_index=True
            )

        parts_df.update(todate(parts_df['joinedTime']))
        parts_df['leftTime'] = todate(parts_df['leftTime'])
        parts_df['delta'] = parts_df.apply(
            lambda r: pd.Timedelta
            (r.leftTime - r.joinedTime).seconds
            / 60.0, axis=1
        )
        tot_part_val = len(parts_df) if len(parts_df) > 0 else 1
        tot_inv = inv_count(m["id"])
        attendance = str(int((
            tot_part_val/tot_inv)*100
            ))+'%' if tot_inv > 0 else '0%'
        part_stats_dict = {
            'Meeting': m["title"],
            'Co_Hosts': int((parts_df.where(
                parts_df['coHost']==True)).count().coHost),
            'Invitees': tot_inv,
            'Participants': len(parts_df),
            'Part_Min_Total': int(parts_df['delta'].sum()),
            'Part_Min_Average': int(
                parts_df['delta'].sum()/tot_part_val),
            'Attendance_Pct': attendance
        }
        return part_stats_dict

def meeting_params(months=1):
    """**meeting_params** - Retrieve the parameters needed to
    list meetings for the report.

    :param months: time offset in months, defaults to 1
    :type months: int, optional
    :return: parameters for list meeting request
    :rtype: dict

    |

    """
    date = dt.today() + r_delta(days=+1)
    delta = r_delta(months=months.__neg__())
    date_to = date.strftime(format='%Y-%m-%d')
    date_from = (date + delta).strftime(format='%Y-%m-%d')
    siteUrl = env['siteUrl']
    hostEmail = env['hostEmail']

    params = {
        'from': date_from,
        'to': date_to,
        #'siteUrl': siteUrl,
        #'hostEmail': hostEmail,
        'max': 100,
        'meetingType': 'meeting'
    }
    return params


def main():
    """**main** - In this module we gather statistics about the meetings
    organised by a specific account, presumably the automation account.

    |

    """
    mts_dict = get_meetings()
    mt_list = []
    if mts_dict:
        for m in mts_dict["items"]:
            part_dict = get_part_stats(m)
            if part_dict:
                mt_list.append(part_dict)
        part_stats_df = pd.DataFrame(mt_list)
        part_stats_df.to_excel(
            f'meeting_participant_stats.xlsx',
            sheet_name='participant_stats', index=False
        )

# execute main when called directly
if __name__ == '__main__':
    main()

'''
The add script used for dispatch events. 
'''


import json
import sys
import os
import re

# Add the current directory to the Python path
# current_dir = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(current_dir)

# Get the parent directory of the current file
# parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(parent_dir)


def submit_dispatch():

    from cmipld.git.actions.functions import parse_md, dispatch, update_issue_title

    # generic items to read the issue
    issue_number = os.environ.get('ISSUE_NUMBER')
    issue_title = os.environ.get('ISSUE_TITLE')
    issue_body = os.environ.get('ISSUE_BODY')
    issue_submitter = os.environ.get('ISSUE_SUBMITTER')
    repo = os.environ.get('REPO').replace(
        'https://github.com', 'https://api.github.com/repos')
    token = os.environ.get('GH_TOKEN')

    #  get content.
    parsed = parse_md(issue_body)

    '''
    Lets submit the data to a dispatch event
    '''

    for kind in parsed:
        print(kind)
        data = parsed[kind]

        payload = {
            "event_type": kind,
            "client_payload": {
                # we need this to define the pull request
                "name": data['acronym'],
                "issue": issue_number,
                "author": issue_submitter,
                "data": json.dumps(data)
            }
        }

        update_issue_title(issue_number, kind, payload)

        dispatch(token, payload, repo)

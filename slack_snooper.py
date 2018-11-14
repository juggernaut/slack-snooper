import argparse
import json
import os
import sys
import subprocess

import requests

BASE_URL = 'https://slack.com'

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', default='config.json')
    parser.add_argument('--get-ssid-script', default='get_ssid')
    return parser.parse_args(args)

def main(args):
    args = parse_args(args)
    try:
        token = os.environ['TOKEN']
    except:
        print "Slack token must be set in env var 'TOKEN'!"
        return 2

    with open(args.conf, 'r') as f:
        config = json.load(f)

    ssid = get_ssid(args.get_ssid_script)

    if ssid not in config:
        print "Unknown SSID {}, not making any changes...".format(ssid)
        return 1

    return update_slack_status(token, config[ssid])

def get_ssid(ssid_script):
    return subprocess.check_output(['/bin/sh', ssid_script], shell=False).strip()

def update_slack_status(token, status):
    headers = {'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + token}
    body = {"profile": status}
    r = requests.post(BASE_URL + '/api/users.profile.set', json.dumps(body), headers=headers)
    if r.status_code == 200:
        print "Successfully updated Slack status to {}".format(status['status_text'])
        return 0
    else:
        print "Request to update Slack status failed with status code {} and body {}".format(r.status_code, r.text)
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

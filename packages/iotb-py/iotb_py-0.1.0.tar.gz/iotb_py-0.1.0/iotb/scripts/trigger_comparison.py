################################################
##      Copyright, Tartabit, LLC.             ##
################################################

import argparse
import difflib
import json
from iotb import IotbClient
import datetime

parser = argparse.ArgumentParser(
    prog='IOTB Trigger Comparison',
    description='Compare triggers in two accounts',
    epilog='Copyright 2025 Tartabit, LLC.')
parser.add_argument('-u1', '--url1', help='API URL 1', default="https://bridge-us.tartabit.com/api/v1/")
parser.add_argument('-u2', '--url2', help='API URL 2', default="https://bridge-us.tartabit.com/api/v1/")
parser.add_argument('-t1', '--token1', help='API Token 1', default="AT:gVUV7pVIM........9E4B1XMQP", required=True)
parser.add_argument('-t2', '--token2', help='API Token 2', default="AT:gVUV7pVIM........9E4B1XMQP", required=True)

args = parser.parse_args()

client1 = IotbClient(args.url1, token=args.token1, debug=False)
client2 = IotbClient(args.url2, token=args.token2, debug=False)

fileName = "diff.txt"

with open(fileName, "w") as f:
    resp = client1.request("GET", "account/$self")
    print(f"account 1: [{resp.body['name']}]",file=f)

    resp = client2.request("GET", "account/$self")
    print(f"account 2: [{resp.body['name']}]",file=f)

    resp = client1.request("GET", "trigger")
    triggerList1 = resp.body

    resp = client2.request("GET", "trigger")
    triggerList2 = resp.body

    triggerDist1 = {trigger['name']: trigger for trigger in triggerList1}
    triggerDist2 = {trigger['name']: trigger for trigger in triggerList2}

    for triggerName in triggerDist1:
        if triggerName not in triggerDist2:
            print(f"trigger [{triggerName}]: missing in account 2", file=f)
    for triggerName in triggerDist2:
        if triggerName not in triggerDist1:
            print(f"trigger [{triggerName}]: missing in account 1", file=f)
    for triggerName in triggerDist1:
        if triggerName in triggerDist2:
            trigger1 = triggerDist1[triggerName]
            trigger2 = triggerDist2[triggerName]
            if trigger1['def'] != trigger2['def']:
                print(f"trigger [{triggerName}]: script differs", file=f)
                ret = difflib.unified_diff(trigger1['def'].splitlines(), trigger2['def'].splitlines(), n=5)
                for line in ret:
                    print(f"  {line}", file=f)
            elif trigger1['filterType'] != trigger2['filterType']:
                print(f"trigger [{triggerName}]: filter types differ {trigger1['filterType']} != {trigger2['filterType']}", file=f)
            elif 'filterCustom' in trigger1 and 'filterCustom' in trigger2 and trigger1['filterCustom'] != trigger2['filterCustom']:
                print(f"trigger [{triggerName}]: custom filters differ", file=f)
                for line in difflib.unified_diff(json.dumps(trigger1['filterCustom'], indent=2).splitlines(), json.dumps(trigger2['filterCustom'], indent=2).splitlines(), n=5):
                    print(f"  {line}", file=f)
            else:
                print(f"trigger [{triggerName}]: identical", file=f)
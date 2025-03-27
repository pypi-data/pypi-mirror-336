################################################
##      Copyright, Tartabit, LLC.             ##
################################################

import argparse
import json
from iotb import IotbClient
import datetime

parser = argparse.ArgumentParser(
    prog='IOTB Download Logs',
    description='Downloads logs from the IoT Bridge as a JSON document',
    epilog='Copyright 2025 Tartabit, LLC.')
parser.add_argument('-u', '--url', help='API URL', default="https://bridge-us.tartabit.com/api/v1/")
parser.add_argument('-t', '--token', help='API Token', default="AT:gVUV7pVIM........9E4B1XMQP", required=True)
parser.add_argument('-q', '--query', help='Query to filter logs', default=None)
parser.add_argument('-d', '--days', help='Days of logs to download', default='30')

args = parser.parse_args()

client = IotbClient(args.url, token=args.token, debug=True)

endDate =  datetime.date.today()
startDate =endDate - datetime.timedelta(days=int(args.days))
startDateString = startDate.strftime('%Y-%m-%dT%H:%M:%SZ')
endDateString = endDate.strftime('%Y-%m-%dT%H:%M:%SZ')

fileName = "logs."+endDate.strftime('%Y%m%d%H%M%S') + ".json"

more = True
first = True
with open(fileName, "w") as f:
    print("[", file=f)
    while more:
        resp = client.request("GET", "log", query={"limit": 1000, "query": args.query, "start": startDateString, "end": endDateString})
        if isinstance(resp.body, list):
            print(f"Got {len(resp.body)} records, first record: {resp.body[0]['ts']}, last record: {resp.body[-1]['ts']}")
            for record in resp.body:
                if not first:
                    print(",", file=f)
                first = False
                json.dump(record, f, indent=2)

            endDateString = resp.body[-1]['ts']
        else:
            more = False
    print("]", file=f)

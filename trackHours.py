#!/usr/bin/env python3

import sys
import argparse
from actionHandler import ActionHandler
parser = argparse.ArgumentParser(description="tracks hours and stores them in a file")

parser.add_argument("jobs", metavar="N", type=str, nargs=1, help='the job you are currently working on')
parser.add_argument("-ci", action="store_true")
parser.add_argument("-co", action="store_true")
args = parser.parse_args()

#print(args.jobs)

actionHandler = ActionHandler(args.jobs[0])
if args.ci and not args.co:
	actionHandler.callAction(["clockin"])
	sys.exit(0)
elif args.co and not args.ci:
	actionHandler.callAction(["clockout"])
	sys.exit(0)

while(True):
	sys.stdout.write("Action::: ")
	sys.stdout.flush()
	action = sys.stdin.readline().split();
	actionHandler.callAction(action)

#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

if args.percent:
    for k in counts[args.key]:
        counts[args.key][k]/= counts['_all'][k]

items = sorted(counts[args.key].items(), key=lambda item: (item[1], item[0]), reverse = True)
top_items = items[:10]
keys, values = zip(*top_items)

input_filename = os.path.basename(args.input_path).replace(".json","")

# create bar plot
plt.figure(figsize=(10, 5))
plt.barh(keys, values, color='skyblue')  # Horizontal bar chart
plt.xlabel('Count')
plt.ylabel('Language/Country')
plt.title(f"Top 10 {args.key} Mentions in {input_filename}")
plt.gca().invert_yaxis()

# save the figure
output_filename = f"{input_filename}_{args.key.replace('#', '')}_top_10_bargraph.png"
plt.savefig(output_filename, bbox_inches='tight')
plt.close()
print(f"Saved plot as {output_filename}")

# normalize the counts by the total values
#if args.percent:
#    for k in counts[args.key]:
#        counts[args.key][k] /= counts['_all'][k]

# print the count values
#items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
#for k,v in items:
#    print(k,':',v)

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
with open(args.input_path, 'r', encoding='utf-8') as f:
    counts = json.load(f)

top_items = sorted(counts[args.key].items(), key=lambda item: item[1])[:10]
labels, values = zip(*top_items)
# create bar plot
plt.figure(figsize=(10, 6))
plt.barh(labels, values, color='skyblue')  # Horizontal bar chart
plt.xlabel('Count')
plt.ylabel('Category')
plt.title(f"Top 10 {args.key} Mentions in {os.path.basename(args.input_path)}")
plt.grid(axis='x', linestyle='--', alpha=0.7)

# save the figure
output_filename = f"{args.key}_{os.path.basename(args.input_path).replace('.json', '.png')}"
plt.savefig(output_filename, bbox_inches='tight')
print(f"Saved plot as {output_filename}")

# normalize the counts by the total values
#if args.percent:
#    for k in counts[args.key]:
#        counts[args.key][k] /= counts['_all'][k]

# print the count values
#items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
#for k,v in items:
#    print(k,':',v)

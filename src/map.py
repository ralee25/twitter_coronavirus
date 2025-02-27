#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input_path',help='Path to the input zip file')
parser.add_argument('output_folder',help='Folder to save the output files')
args = parser.parse_args()

# imports
import os
import zipfile
import datetime 
import json
from collections import Counter,defaultdict

# load keywords
hashtags = [
    '#코로나바이러스',  # korean
    '#コロナウイルス',  # japanese
    '#冠状病毒',        # chinese
    '#covid2019',
    '#covid-2019',
    '#covid19',
    '#covid-19',
    '#coronavirus',
    '#corona',
    '#virus',
    '#flu',
    '#sick',
    '#cough',
    '#sneeze',
    '#hospital',
    '#nurse',
    '#doctor',
    ]

# initialize counters
counter_lang = defaultdict(lambda: Counter())
counter_country = defaultdict(lambda: Counter())

# open the zipfile
with zipfile.ZipFile(args.input_path) as archive:
    print(f"Debug: Total files in zip: {len(archive.namelist())}")  # Debugging print

    # loop over every file within the zip file
    for filename in archive.namelist():
        print(datetime.datetime.now(), "Processing file:", filename)

        # open the inner file
        with archive.open(filename) as f:

            # loop over each line in the inner file
            for line_number, line in enumerate(f,1):
                try:
                    tweet= json.loads(line)
                    # load the tweet as a python dictionary
                    tweet_data = tweet.get('data', tweet)

                    # convert text to lower case
                    text = tweet_data.get('text','')

                    if text:
                        text = text.lower()
                    else:
                        text=""


                    if line_number <= 5:
                        print(f"Debug: Tweet Text: {text}")
                    
                    lang = tweet_data.get('lang', 'unknown')

                    country_code = None


                    try:
                        country_code = tweet['place']['country_code']
                    except (KeyError, TypeError):
                        pass

                    if line_number <= 5:
                        print(f"Debug: Lang: {lang}, Country: {country_code}")  # Print first 5 tweets' lang and country


                    # search hashtags
                    for hashtag in hashtags:
                  

                        if hashtag.lower() in text:
                            counter_lang[hashtag][lang] += 1
                            counter_country[hashtag][country_code] += 1
                        
                    counter_lang["_all"][lang] += 1
                    counter_country["_all"][country_code] += 1

                except json.JSONDecodeError:
                    pass

if counter_lang and counter_country:
    # open the outputfile
    # Create output folder if it doesn't exist
    os.makedirs(args.output_folder, exist_ok=True)
    output_path_base = os.path.join(args.output_folder, os.path.basename(args.input_path))

    # Save language data
    output_path_lang = output_path_base + '.lang'
    print('Saving', output_path_lang)
    with open(output_path_lang, 'w') as f:
        json.dump(counter_lang,f,indent=4)

    # Save country data
    output_path_country = output_path_base + '.country'
    print('Saving', output_path_country)
    with open(output_path_country, 'w') as f:
        json.dump(counter_country,f,indent=4)

else:
    print("no hashtags or country data found in tweets")



# imports
import os
import json
from glob import glob
import sys

def combine(file, output_dir):
    """
    Combining all files into a single output file
    """

    combined = {}

    for filename in sorted(glob(file)):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data=json.load(f)

                for key, value in data.items():
                    if key not in combined:
                        combined[key] = {}
                    for subkey, count in value.items():
                        if subkey not in combined[key]:
                            combined[key][subkey]=0
                        combined[key][subkey]+=count
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}:{e}")

    # write the output path
    with open(output_dir,'w',encoding='utf-8') as output:
        json.dump(combined,output,ensure_ascii=False,indent=4)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("usage: python3 reduce.py <output_directory>")
        sys.exit(1)
    output_dir = sys.argv[1]
    combine(os.path.join(output_dir, "*.lang"), os.path.join(output_dir, "all_languages.json"))
    combine(os.path.join(output_dir, "*.country"), os.path.join(output_dir, "all_countries.json"))



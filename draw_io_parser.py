#!/usr/bin/env python

import xml.etree.ElementTree as ET
import re
import csv
import argparse

def parser(input,output):
    # tree = ET.parse(r'Untitled Diagram.xml')
    tree = ET.parse(str(input))
    root = tree.getroot()
    elements = {}
    output_list = [["Source","Description","Target"]]

    for diag in root.iter('mxCell'):
        if diag.get("value"):
            cleaned = diag.get("value").replace("&nbsp;","")
            elements[diag.get("id")] =  re.sub(r'\<[^>]*\>', '', cleaned)
        elif diag.get("id"):
            elements[diag.get("id")] = "none"

    for diag in root.iter('mxCell'):
        if diag.get("source"):
            tmp_list = []
            x = diag.get("style").split(";")
            dic = {}
            for a in x:
                if a:
                    t = a.split("=")
                    dic[t[0]] = t[1]
            try:
                if dic["endArrow"] != "none":
                    tmp_list.append(elements[diag.get('source')])
                    tmp_list.append(elements[diag.get('id')])
                    tmp_list.append(elements[diag.get('target')])
                    # print(f"Source = {elements[diag.get('source')]} Target = {elements[diag.get('target')]}")
                else:
                    tmp_list.append(elements[diag.get('target')])
                    tmp_list.append(elements[diag.get('id')])
                    tmp_list.append(elements[diag.get('source')])
                    # print(f"Source = {elements[diag.get('target')]} Target = {elements[diag.get('source')]}")
                output_list.append(tmp_list)
            except:
                print(f"I have problem with {diag.get('id')}")

    # print(output_list)

    try:
        with open(output, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerows(output_list)
            print("Completed!")
    except:
        print("I can not write to file")


arg_parser = argparse.ArgumentParser(description='Coverts draw.io XML to CSV with inerfaces')
arg_parser.add_argument("--input","-I", required=True,type=str, help='The path to XML exported from draw.io ')
arg_parser.add_argument("--output","-O",required=False,type=str,default="draw_io_parser_output.csv",help="The path to output csv file (default path is \"draw_io_parser_output.csv\")")

args = arg_parser.parse_args()

try:
    parser(args.input,args.output)
except:
    print("Not today:(")
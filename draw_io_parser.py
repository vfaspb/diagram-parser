#!/usr/bin/env python

import xml.etree.ElementTree as ET
import re
import csv
import argparse

def parser(input):
    # tree = ET.parse(r'Untitled Diagram.xml')
    tree = ET.parse(str(input))
    root = tree.getroot()
    elements = {}
    elements_parents = {}
    output_list = [["Source","Description","Target"]]
#Delets html and creates dictionaries with id - value and id parent
    for diag in root.iter('mxCell'): 
        if diag.get("value"):
            cleaned = diag.get("value").replace("&nbsp;","")
            elements[diag.get("id")] =  re.sub(r'\<[^>]*\>', '', cleaned)
        elif diag.get("id"):
            elements[diag.get("id")] = "none"
        if diag.get("parent") != "1" and diag.get("parent") != "0" and diag.get("parent") != None: #Here are some mistakes possible since key may not be uniq
            elements_parents[diag.get("parent")] = diag.get("id")
    # print(elements_parents)

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
                if dic["endArrow"] != "none": #we check if derction is real or not
                    tmp_list.append(elements[diag.get('source')])
                    if elements[diag.get('id')] == "none":
                        tmp_list.append(elements[elements_parents[diag.get('id')]]) #crazy code where value child is used instead of parent value, if parent value is none (the same staff bellow)
                    else:
                        tmp_list.append(elements[diag.get('id')])
                    tmp_list.append(elements[diag.get('target')])
                    # print(f"Source = {elements[diag.get('source')]} Target = {elements[diag.get('target')]}")
                else:
                    tmp_list.append(elements[diag.get('target')])
                    if elements[diag.get('id')] == "none":
                        tmp_list.append(elements[elements_parents[diag.get('id')]])
                    else:
                        tmp_list.append(elements[diag.get('id')])
                    tmp_list.append(elements[diag.get('source')])
                    # print(f"Source = {elements[diag.get('target')]} Target = {elements[diag.get('source')]}")
                output_list.append(tmp_list)
            except:
                print(f"I have problem with {diag.get('id')}")

    return output_list

def csv_export(input_list,output):
    try:
        with open(output, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerows(input_list)
            print("Completed!")
    except:
        print("I can not write to file")



arg_parser = argparse.ArgumentParser(description='Converts draw.io XML to CSV with inerfaces')
arg_parser.add_argument("--input","-I", required=True,type=str, help='The path to XML exported from draw.io ')
arg_parser.add_argument("--output","-O",required=False,type=str,default="draw_io_parser_output.csv",help="The path to output csv file (default path is \"draw_io_parser_output.csv\")")

args = arg_parser.parse_args()

try:
    # print(parser(args.input))
    csv_export(parser(args.input),args.output)
except:
    print("Not today:(")
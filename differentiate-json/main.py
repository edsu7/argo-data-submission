#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Copyright (c) 2022, Your Organization Name

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

  Authors:
    edsu7
"""

import os
import sys
import argparse
import json


def main():
    """
    Python implementation of tool: differentiate-json

    This is auto-differentiated Python code, please update as needed!
    """

    parser = argparse.ArgumentParser(description='differentiate JSON metadata payload for SONG upload')
    parser.add_argument('-a', '--auto_generated', dest="auto_generated", help="auto generated json", required=True)
    parser.add_argument('-b', '--user_provided',dest="user_provided", help="user generated json", required=True)

    results = parser.parse_args()

    for file,var in zip(
        [results.auto_generated,results.user_provided],
        [ag_dict,up_dict]
    ):
        with open(file) as json_file:
            var = json.load(json_file)
            
    with open(json_a) as json_file:
            ag_dict = json.load(json_file)
    with open(json_b) as json_file:
            up_dict = json.load(json_file)
            
    check_values(up_dict,ag_dict)
            
        
                
def check_values(json_a,json_b):
    for key in json_b:
        print(key)
        ###is key in X
        if key not in json_a:
            raise ValueError("'"+key+"' not found in user generated JSON")
        
        ###
        elif type(json_a[key])==dict:
            check_values(json_a[key],json_b[key])
            
        elif type(json_a[key])==list:
            
            for entry in enumerate(json_b[key]):
                if type(entry[1])==dict:
                    check_values(json_a[key][entry[0]],json_b[key][entry[0]])
                else:
                    if json_a[key][entry[0]]!=json_b[key][entry[0]] and json_b[key][entry[0]] !=None:
                        raise ValueError("Differing values found when comparing'"+key+"' :"+str(json_a[key][entry[0]])+" vs computed "+str(json_b[key][entry[0]]))
                    
        
        if json_a[key]!=json_b[key] and json_b[key]!=None:
            raise ValueError("Differing values found when comparing'"+key+"' :"+str(json_a[key])+" vs computed "+str(json_b[key]))
    
    
if __name__ == "__main__":
    main()

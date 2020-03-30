#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from yacc import parser

def frontEnd(input_file_name:str):
    if os.path.splitext(input_file_name)[1] == ".idl":
        return

    idl_data = parser.parse(open(input_file_name).read())

    output_file_name = os.path.splitext(input_file_name)[0]+".idl"
    with open(output_file_name, "w") as f:
        f.write("struct {name} {{\n".format(
            name=idl_data["name"]
        ))
        for param in idl_data["params"]:
            f.write("    {type} {name}".format(
                type=param["type"], name=param["name"]
            ))
            for array_size in param["size"]:
                f.write("[{}]".format(array_size))
            f.write(";\n")
        f.write("};")

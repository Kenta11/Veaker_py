#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import datetime

def fastRTPSStage(input_file_name:str):
    options = []

    if os.path.dirname(input_file_name) != "":
        options += ["-d", os.path.dirname(input_file_name)]

    subprocess.run(\
        ["fastrtpsgen", input_file_name] + options,\
        stdout=open("../../log/temgen"+input_file_name+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".log", "w"),\
        stderr=subprocess.STDOUT\
    )

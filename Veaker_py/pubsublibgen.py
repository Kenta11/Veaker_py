#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from frontend import frontEnd
from fastrtpsgen import fastRTPSStage
from backend import backEnd

def pubsublibgen(input_file_name:str):
    frontEnd(input_file_name)
    fastRTPSStage(os.path.splitext(input_file_name)[0]+".idl")
    backEnd(os.path.splitext(input_file_name)[0])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jinja2
import os
import shutil
import sys
import toml

from pathlib import Path
from logzero import logger

sys.path.append(os.path.dirname(__file__))
from .pubsublibgen import pubsublibgen

def createProject(node_name:str):
    logger.info("Generating project: "+node_name)

    os.chdir(Path("nodes") / node_name)

    alchemist = toml.load(open(".Alchemist.toml"))

    ports:list    = alchemist["node"]["ports"]
    device:dict   = alchemist["device"]
    messages:list = list(map(
        lambda x: (x["name"], "struct {} {{\n    {}}};".format(x["name"], x["message"])),
        alchemist["topics"]
    ))

    # make directories
    for d in ["include","src","test/include","test/src","script","idl","msg"]:
        os.makedirs(d)

    # make source codes
    generateMakefile(node_name, device["board"])
    generateTcl(node_name, device["board"], device["fpga"], device["clock"])
    generateDirectives()
    generateGitignore(node_name)
    for message in messages:
        generateFastrtpslib(message)
    generateSourceCode(node_name, ports)

    os.chdir("../../")

    logger.info("Complete generating project: "+node_name)

def generateMakefile(project:str, solution:str):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            str(Path(os.path.dirname(__file__)) / "template")
        )
    )
    template = env.get_template("Makefile")
    data = {
        "TARGET": project,
        "SOLUTION": solution
    }
    rendered = template.render(data)
    with open("Makefile", "w") as f:
        f.write(str(rendered))

def generateTcl(project:str, board:str, part:str, clock:str):
    ##### cosim.tcl, export.tcl #####
    src_dir = Path(os.path.dirname(__file__)) / "template/tcl"
    for name in ["init", "csim", "cosim", "export"]:
        shutil.copy(src_dir / (name+".tcl"), "script/"+name+".tcl")

    ##### csynth.tcl #####
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            str(Path(os.path.dirname(__file__)) / "template/tcl")
        )
    )
    template = env.get_template("csynth.tcl")
    data = {
        "PART": "{" + part + "}",
        "CLOCK": clock
    }
    rendered = template.render(data)
    with open("script/csynth.tcl", "w") as f:
        f.write(str(rendered))

def generateDirectives():
    Path("directives.tcl").touch()

def generateGitignore(project:str):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            str(Path(os.path.dirname(__file__)) / "template")
        )
    )
    template = env.get_template("gitignore")
    data = {
        "TARGET": project
    }
    rendered = template.render(data)
    with open(".gitignore", "w") as f:
        f.write(str(rendered))

def generateFastrtpslib(message:tuple):
    filename = message[0] + ".msg"
    with open(filename, "w") as f:
        f.write(message[1])

    pubsublibgen(filename)

    for name in ["", "Publisher", "Subscriber"]:
        shutil.move(message[0]+name+".h",  "include/")
        shutil.move(message[0]+name+".cc", "src/")

    shutil.move(message[0]+"PubSubTypes.h",  "test/include/")
    shutil.move(message[0]+"PubSubTypes.cc", "test/src/")

    shutil.move(message[0]+".idl",            "idl/")
    shutil.move(message[0]+".msg",            "msg/")

def generateSourceCode(target:str, ports:list):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            str(Path(os.path.dirname(__file__)) / "template/cc")
        )
    )
    
    # header
    headers = set()
    for port in ports:
        if port["attribute"] == "publisher":
            headers.add(port["topic"] + "Publisher.h")
        elif port["attribute"] == "subscriber":
            headers.add(port["topic"] + "Subscriber.h")
        elif port["attribute"] == "wire":
            headers.add("ap_int.h")

    args = []
    for port in ports:
        dic = {}
        if port["attribute"] == "publisher":
            dic["type"] = port["topic"] + "Publisher"
            dic["name"] = "&" + port["name"]
        elif port["attribute"] == "subscriber":
            dic["type"] = port["topic"] + "Subscriber"
            dic["name"] = "&" + port["name"]
        elif port["attribute"] == "wire":
            dic["type"] = "ap_uint<{}>".format(port["width"])
            dic["name"] = port["name"]
        args.append(dic)

    with open("include/{}.h".format(target), "w") as f:
        template = env.get_template("header.h")
        rendered = template.render({
            "target": target, "headers": headers, "args": args
        })
        f.write(str(rendered))

    # code
    with open("src/{}.cc".format(target), "w") as f:
        template = env.get_template("code.cc")
        rendered = template.render({
            "target": target, "args": args
        })
        f.write(str(rendered))

    # test code
    headers = set()
    for port in ports:
        if port["attribute"] == "publisher":
            headers.add(port["topic"] + "Subscriber.h")
        elif port["attribute"] == "subscriber":
            headers.add(port["topic"] + "Publisher.h")
    with open("test/src/test_{}.cc".format(target), "w") as f:
        template = env.get_template("test-code.cc")
        rendered = template.render({
            "target": target
        })
        f.write(str(rendered))

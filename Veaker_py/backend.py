#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jinja2
import os

from logzero import logger

from yacc import parser

def backEnd(message_name:str):
    adaptToVivadoHLS(message_name)
    generatePublisherClass(message_name)
    generateSubscriberClass(message_name)

def adaptToVivadoHLS(message_name:str):
    renameFiles(message_name)
    insertSynthesisMacro(message_name)

def generatePublisherClass(message_name:str):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.dirname(__file__) + "/template/cc")
    )

    # generate XxxPublisher.h
    template = env.get_template("publisher.h")
    rendered = template.render({ "message_name" : message_name })
    with open(message_name+"Publisher.h", "w") as f:
        f.write(str(rendered))

    # generate XxxPublisher.cc
    template = env.get_template("publisher.cc")
    method = "    int index = 0;\n"
    members = getMembers(message_name)
    for m in members["params"]:
        if m["attribute"] == "unit":
            var_name = {
                "unsigned long long" : ("ul"   , 1),
                "unsigned long"      : ("ui[0]", 2),
                "unsigned short"     : ("us[0]", 4),
                "octet"              : ("uc[0]", 8),
                "long long"          : ("sl"   , 1),
                "long"               : ("si[0]", 2),
                "short"              : ("ss[0]", 4),
                "char"               : ("sc[0]", 8),
                "boolean"            : ("uc[0]", 8)
            }
            if m["type"] in var_name.keys():
                method += "    packet.{} = msg.{}();\n".format(
                    var_name[m["type"]][0], m["name"]
                )
            else:
                logger.error("Illigal message format!: "+m["type"])
                exit(1)
            method += "    this->write(packet.ul);\n"
        elif m["attribute"] == "array":
            var_name = {
                "unsigned long long" : ("ul", 1),
                "unsigned long"      : ("ui[index++]", 2),
                "unsigned short"     : ("us[index++]", 4),
                "octet"              : ("uc[index++]", 8),
                "long long"          : ("sl", 1),
                "long"               : ("si[index++]", 2),
                "short"              : ("ss[index++]", 4),
                "char"               : ("sc[index++]", 8),
                "boolean"            : ("uc[index++]", 8)
            }
            my_indent = " " * 4

            if m["type"] not in var_name.keys():
                logger.error("Illigal message format!")
                exit(1)

            expr = [my_indent, my_indent]
            expr[0] += "packet.{} = msg.{}()".format(
                var_name[m["type"]][0], m["name"]
            )
            expr[0] += "".join(["[{}]".format(
                chr(ord('i')+i)
            ) for i in reversed(range(len(m["size"])))]) + ";"
            if var_name[m["type"]][1] == 1:
                expr[1] += "this->write(packet.ul);"
            else:
                expr[1] += "if (index == {max}) {{".format(max=var_name[m["type"]][1])
                expr.append((my_indent*2)+"index = 0;")
                expr.append((my_indent*2)+"this->write(packet.ul);")
                expr.append(my_indent+"}")
            for i in range(len(m["size"])):
                expr.insert(
                    0,
                    "for (int {cnt} = 0; {cnt} < {max}; {cnt}++) {{".format(
                        cnt=chr(ord('i')+i), max=m["size"][len(m["size"])-i-1]
                    )
                )
                expr.append("}")
                expr = list(map(lambda x: my_indent+x, expr))

            expr.append(my_indent+"if (index != 0) {{".format(max=var_name[m["type"]][1]))
            expr.append((my_indent*2)+"this->write(packet.ul);")
            expr.append(my_indent+"}")
            method += "\n".join(expr)
        else:
            logger.error("Illigal message format!")
            exit(1)

    data = {
        "message_name"   : message_name,
        "publish_method" : method
    }
    rendered = template.render(data)
    with open(message_name+"Publisher.cc", "w") as f:
        f.write(str(rendered))

def generateSubscriberClass(message_name:str):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.dirname(__file__) + "/template/cc")
    )

    # generate XxxSubscriber.h
    template = env.get_template("subscriber.h")
    rendered = template.render({ "message_name": message_name })
    with open(message_name+"Subscriber.h", "w") as f:
        f.write(str(rendered))

    # generate XxxSubscriber.cc
    template = env.get_template("subscriber.cc")
    method  = "    int index = 0;\n"
    members = getMembers(message_name)
    for m in members["params"]:
        if m["attribute"] == "unit":
            var_name = {
                "unsigned long long" : ("ul"   , 1),
                "unsigned long"      : ("ui[0]", 2),
                "unsigned short"     : ("us[0]", 4),
                "octet"              : ("uc[0]", 8),
                "long long"          : ("sl"   , 1),
                "long"               : ("si[0]", 2),
                "short"              : ("ss[0]", 4),
                "char"               : ("sc[0]", 8),
                "boolean"            : ("uc[0]", 8)
            }
            if m["type"] not in var_name.keys():
                logger.error("Illigal message format!: "+m["type"])
                exit(1)

            method += "    packet.ul = this->read();\n"
            method += "    msg.{}() = packet.{};\n".format(
                m["name"], var_name[m["type"]][0]
            )
        elif m["attribute"] == "array":
            var_name = {
                "unsigned long long" : ("ul", 1),
                "unsigned long"      : ("ui[index++]", 2),
                "unsigned short"     : ("us[index++]", 4),
                "octet"              : ("uc[index++]", 8),
                "long long"          : ("sl", 1),
                "long"               : ("si[index++]", 2),
                "short"              : ("ss[index++]", 4),
                "char"               : ("sc[index++]", 8),
                "boolean"            : ("uc[index++]", 8)
            }
            my_indent = " " * 4

            if m["type"] not in var_name.keys():
                logger.error("Illigal message format!")
                exit(1)

            expr = [my_indent]
            if var_name[m["type"]][1] == 1:
                expr[0] += "packet.ul = this->read();"
            else:
                expr[0] += "if (index == 0) {"
                expr.append((my_indent*2)+"packet.ul = this->read();")
                expr.append(my_indent+"}")
            expr.append(my_indent+"msg.{}()".format(
                m["name"]
            )) 
            expr[-1] += "".join(["[{}]".format(
                chr(ord('i')+i)
            ) for i in reversed(range(len(m["size"])))])
            expr[-1] += " = packet.{};".format(
                var_name[m["type"]][0]
            )
            if var_name[m["type"]][1] != 1:
                expr.append(my_indent+"if (index == {}) {{".format(var_name[m["type"]][1]))
                expr.append((my_indent*2)+"index = 0;")
                expr.append(my_indent+"}")

            for i in range(len(m["size"])):
                expr.insert(
                    0,
                    "for (int {cnt} = 0; {cnt} < {max}; {cnt}++) {{".format(
                        cnt=chr(ord('i')+i), max=m["size"][len(m["size"])-i-1]
                    )
                )
                expr.append("}")
                expr = list(map(lambda x: my_indent+x, expr))

            method += "\n".join(expr)
        else:
            logger.error("Illigal message format!")
            exit(1)

    data = {
        "message_name": message_name,
        "subscribe_method": method
    }
    rendered = template.render(data)
    with open(message_name+"Subscriber.cc", "w") as f:
        f.write(str(rendered))

def renameFiles(message_name:str):
    for name in ["", "PubSubTypes"]:
        os.rename(message_name+name+".cxx", message_name+name+".cc")

def insertSynthesisMacro(message_name:str):
    # <Message>.cc
    with open(message_name+".cc") as f:
        text = f.read()
    constructor = message_name+"::"+message_name+"()\n{\n"
    offset = text.find(constructor) + len(constructor)
    text = text[:offset]\
           + "#ifndef __SYNTHESIS__\n"\
           + text[offset:offset+text[offset:].find('}')]\
           + "#endif // __SYNTHESIS__\n"\
           + text[offset+text[offset:].find('}'):]
    with open(message_name+".cc", "w") as f:
        f.write(text)

def getMembers(message_name:str):
    with open(message_name+".msg") as f:
        return parser.parse(f.read())

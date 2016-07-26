import re

rePath = re.compile(r'(<path[^/>]*/>)')
reCircle = re.compile(r'(<circle[^/>]*/>)')
reWH = re.compile(r'<image [^>]*(height="(?P<height>\d+)"[^>]* | width="(?P<width>\d+)"[^>]*){2}[^>]*/>')
reFill = re.compile(r'<path[^/>]*fill\s*=\s*"(?P<fill>[^"]*)"')
reStroke = re.compile(r'<path[^/>]*stroke\s*=\s*"(?P<stroke>[^"]*)"')
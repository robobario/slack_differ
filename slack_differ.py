#!/usr/bin/python
import sh
from os import listdir, mkdir
from os.path import join, realpath, dirname, isdir, isfile
import json
import sys 
print "running slack_differ"
dname = dirname(realpath(__file__))
print "dirname : " + dname
script_dir = join(dname,'scripts')
print "script_dir : " + script_dir
if not isdir(script_dir):
  print "no script dir found"
  scripts = []
else:
  scripts = [f for f in listdir(script_dir) if f.endswith(".json")]
for script in scripts:
  try:
    script_metadata = json.load(open(join(script_dir, script)))
    old_file = join(dname, script + ".old")
    new_file = join(dname, script + ".new")
    new_out = open(new_file,'w')
    command = sh.Command(join(script_dir,script_metadata["script"]))
    print("running " + join(script_dir,script_metadata["script"]))
    command(_out=new_out)
    if not isfile(old_file):
      sh.cp(new_file,old_file)
    diff = sh.diff(old_file,new_file,_ok_code=[0,1])
    if len(diff) > 0:
      message = str(open(new_file).read())
      payload = {
        "channel":script_metadata["channel"],
        "username":script_metadata["user"],
        "text": script_metadata["title"],
        "icon_emoji":script_metadata["emoji"],
        "attachments" : [
          {
            "color":"good",
            "fields":[
              {
                "title":"new value",
                "value":message,
                "short":False
                }
              ]
            }
          ]
        }
      payload = "payload=" + json.dumps(payload)
      sh.mv(new_file,old_file)
      sh.curl(["curl", "-X", "POST" ,"--data-urlencode" ,payload,script_metadata["slack_url"]])
  except Exception as e:
    print "failed on " + script +" :" + str(e) 

if len(sys.argv) > 1 and sys.argv[1] == "example":
    print("initialising example")
    if not isdir(script_dir):
      mkdir(script_dir)
    script = open(join(script_dir,"example.sh"),'w')
    script.write("#!/bin/bash\necho 'hi'")
    metafile = open(join(script_dir,"example.json"),'w')
    meta = {
      "channel":"#example",
      "user":"examplebot",
      "title":"script title",
      "emoji":":metal:",
      "slack_url":"https://hook.slack.com/XXX/YYY",
      "script":"example.sh"
    }
    metafile.write(json.dumps(meta))

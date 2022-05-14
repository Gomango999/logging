#!/usr/bin/env python3
# Opens the log file and creates a new entry to write to

from datetime import datetime, timedelta
import os
import re
import sys

if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 2 and sys.argv[1] == "edit":
        os.system("subl /Users/kevin/projects/logmd")
        os.system("subl /Users/kevin/projects/logmd/log.py")
        exit(0)
else:
    print("Usage: lg [edit]")
    

logfile = "/Users/kevin/Dropbox/caret/log.md"

with open(logfile, 'r+') as file:
    content = file.readlines()

    # Grab most recent date
    line_number = 0
    while (content[line_number].strip() == ""):
        line_number += 1
    firstline = content[line_number].strip()
    
    match = re.search(r"^(### [a-zA-Z]{3} \d{2} [a-zA-Z]{3})", firstline)
    last_date = datetime.strptime(match.group(), "### %a %d %b")

    # Subtract of 6 hours off the current time. This has the effect
    # of starting a new 'day' at 6am, instead of 12.
    now = datetime.now()
    now -= timedelta(hours=6)

    open_location = (1, 1) # line number, column
    if now.day == last_date.day and now.month == last_date.month:
        # Log date already exists, locate the correct line number.
        
        # Find the second header, or the last line of the file if none
        count = 0
        line_number = -1 # default is end of file
        for i, line in enumerate(content):
            if line.startswith("###"):
                count += 1
            if count == 2:
                line_number = i
                break
                
        # Move back up until we find the previous line.
        line_number -= 1
        while content[line_number].strip() == "":
            line_number -= 1
        
        if (content[line_number].strip() == "-"):
            # Empty trailing bullet point. Just reuse this
            open_location = (line_number+1, 3)
        else:
            # Append onto there. We add 2 to account for 0 indexing and going to the next line.
            content[line_number] += "- \n"
            open_location = (line_number+2, 3)
        
    else:
        # Top date is different. Add a new date at the beginning
        new_header = now.strftime("### %a %-d %b")
        content[0] = f"{new_header}\n- \n\n" + content[0]
        open_location = (2, 3)
        
    # Write to file
    file.seek(0)
    file.write("".join(content))
  
os.system(f"subl /Users/kevin/Dropbox/caret/")
os.system(f"subl {logfile}:{open_location[0]}:{open_location[1]}")
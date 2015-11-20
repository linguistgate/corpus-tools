#/bin/sh

bzcat swtrans.cat.txt.bz2 | grep -v FILENAME | grep -v TOPIC\# | grep -v DATE | grep -v TRANSCRIBER | grep -v DIFFICULTY | grep -v TOPICALITY | grep -v NATURALNESS | grep -v ECHO_FROM_B | grep -v ECHO_FROM_A | grep -v STATIC_ON_A | grep -v STATIC_ON_B | grep -v BACKGROUND_A | grep -v BACKGROUND_B | grep -v REMARKS | grep -v "====" | sed -e  's/^.*://' | tr ' ' '\n' | grep '[A-Za-z]' | sed -e 's/[#"(),;\.?}{]//g' | grep -wv "\[laughter\]" | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -n -r | tr -s '[:blank:]' ',' | sed 's/^,//g'

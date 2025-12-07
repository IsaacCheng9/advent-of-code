#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start_date> <end_date>"
    echo "Format: YYYY-MM-DD"
    echo "Example: $0 2023-12-01 2023-12-25"
    exit 1
fi

START_DATE=$1
END_DATE=$2
COOKIE_FILE=".config/cookie"

if [ ! -f "$COOKIE_FILE" ]; then
    echo "Error: Cookie file not found at $COOKIE_FILE"
    exit 1
fi

COOKIE="$(< "$COOKIE_FILE" tr -d '\n')"
CURRENT_DATE="$START_DATE"

# Check if on macOS (Darwin) or Linux for date command
if [[ "$(uname)" == "Darwin" ]]; then
    DATE_CMD="date -j -f %Y-%m-%d"
    ADD_DAY_CMD="date -j -v+1d -f %Y-%m-%d"
else
    # Assume GNU date
    DATE_CMD="date -d"
    ADD_DAY_CMD="date -d"
fi

while [[ "$CURRENT_DATE" < "$END_DATE" || "$CURRENT_DATE" == "$END_DATE" ]]; do
    if [[ "$(uname)" == "Darwin" ]]; then
        YEAR=$($DATE_CMD "$CURRENT_DATE" +%Y)
        DAY=$($DATE_CMD "$CURRENT_DATE" +%-d)
        DAY_PADDED=$($DATE_CMD "$CURRENT_DATE" +%d)
        NEXT_DATE=$($ADD_DAY_CMD "$CURRENT_DATE" +%Y-%m-%d)
    else
        YEAR=$($DATE_CMD "$CURRENT_DATE" +%Y)
        DAY=$($DATE_CMD "$CURRENT_DATE" +%-d)
        DAY_PADDED=$($DATE_CMD "$CURRENT_DATE" +%d)
        NEXT_DATE=$($ADD_DAY_CMD "$CURRENT_DATE + 1 day" +%Y-%m-%d)
    fi

    DIR="$YEAR/day_$DAY_PADDED"
    PROBLEM_FILE="$DIR/problem.txt"

    if [ -d "$DIR" ]; then
        echo "Updating problem for $CURRENT_DATE in $DIR..."
        
        PROBLEM_URL="https://adventofcode.com/$YEAR/day/$DAY"
        TEMP_FILE=$(mktemp)
        
        # Fetch and parse using the Python script
        # Using -k (insecure) to avoid SSL certificate issues in some environments
        if curl "${PROBLEM_URL}" --compressed -s -f -k \
          -H "Cookie: session=${COOKIE}" | python3 -c "
import sys
from html.parser import HTMLParser

class AoC(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.skip = False
        self.data = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            for k, v in attrs:
                if k == 'class' and v and 'day-desc' in v:
                    self.capture = True
        elif tag in ('style', 'script'):
            self.skip = True
            
    def handle_endtag(self, tag):
        if tag == 'article':
            self.capture = False
            self.data.append('\n')
        elif tag in ('style', 'script'):
            self.skip = False
            
    def handle_data(self, data):
        if self.capture and not self.skip:
            self.data.append(data)

p = AoC()
p.feed(sys.stdin.read())
result = ''.join(p.data).strip()
if result:
    print(result)
" > "$TEMP_FILE" && [ -s "$TEMP_FILE" ]; then
            mv "$TEMP_FILE" "$PROBLEM_FILE"
            echo "  Success."
        else
            echo "  Failed to fetch or empty content. Keeping original file."
            rm -f "$TEMP_FILE"
        fi
    else
        echo "Skipping $CURRENT_DATE: Directory $DIR does not exist."
    fi

    CURRENT_DATE="$NEXT_DATE"
done


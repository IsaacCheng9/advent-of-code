COOKIE_FILE=".config/cookie"
if [ ! -f "$COOKIE_FILE" ]; then
  echo "Error: Cookie file not found at $COOKIE_FILE"
  exit 1
fi

# Setup day info
DAY_PADDED=$(date +%d)
YEAR=$(date +%Y)
DAY=$(date +%-d)
YEAR_DIR="$YEAR"
DIR="$YEAR_DIR/day_$DAY_PADDED"
COOKIE="$(< "$COOKIE_FILE" tr -d '\n')"

# First check if we can get the problem description
PROBLEM_URL="https://adventofcode.com/$YEAR/day/$DAY"
TEMP_PROBLEM="temp-problem.txt"

curl "${PROBLEM_URL}" --compressed -f \
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
print(''.join(p.data).strip())
" > "${TEMP_PROBLEM}"

# Check if problem description was fetched successfully
if [ ! -s "${TEMP_PROBLEM}" ]; then
  echo "Error: Could not fetch problem description. Problem may not be released yet."
  rm "${TEMP_PROBLEM}"
  exit 1
fi

# If we get here, the problem exists, so create the directory and files
# Prioritise current year's template, then root, then previous year
if [ -d "$YEAR/day_xx" ]; then
    TEMPLATE_DIR="$YEAR/day_xx"
elif [ -d "day_xx" ]; then
    TEMPLATE_DIR="day_xx"
elif [ -d "$((YEAR - 1))/day_xx" ]; then
    TEMPLATE_DIR="$((YEAR - 1))/day_xx"
else
    echo "Error: Template day_xx not found."
    rm "${TEMP_PROBLEM}"
    exit 1
fi

mkdir -p "$DIR"

# Ensure utils exist for the new year
if [ ! -d "$YEAR_DIR/utils" ] && [ -d "2024/utils" ]; then
    echo "Copying utils from 2024..."
    cp -r "2024/utils" "$YEAR_DIR/"
fi

cp -r "$TEMPLATE_DIR/"* "$DIR/"
sed -i '' "s|day_xx|$DIR|g" "$DIR/main.py"

# Move problem description to final location
mv "${TEMP_PROBLEM}" "$DIR/problem.txt"

# Get the input and save to input.txt for the day
INPUT_URL="$PROBLEM_URL/input"
curl "${INPUT_URL}" --compressed -f \
  -H "Cookie: session=${COOKIE}" \
  -o "$DIR/input.txt"

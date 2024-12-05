COOKIE_FILE=".config/cookie"
if [ ! -f "$COOKIE_FILE" ]; then
    echo "Error: Cookie file not found at $COOKIE_FILE"
    exit 1
fi

# Setup day info
DAY_PADDED=$(date +%d)
DIR="day_$DAY_PADDED"
YEAR=$(date +%Y)
DAY=$(date +%-d)
COOKIE="$(< "$COOKIE_FILE" tr -d '\n')"

# First check if we can get the problem description
PROBLEM_URL="https://adventofcode.com/$YEAR/day/$DAY"
TEMP_PROBLEM="temp-problem.txt"

curl "${PROBLEM_URL}" --compressed -f \
  -H "Cookie: session=${COOKIE}" \
  | grep -A999999 "<article class=\"day-desc\">" \
  | grep -B999999 "</article>" \
  | sed 's/<[^>]*>//g' \
  > "${TEMP_PROBLEM}"

# Check if problem description was fetched successfully
if [ ! -s "${TEMP_PROBLEM}" ]; then
    echo "Error: Could not fetch problem description. Problem may not be released yet."
    rm "${TEMP_PROBLEM}"
    exit 1
fi

# If we get here, the problem exists, so create the directory and files
cp -r "day_xx" "$DIR"
sed -i '' "s/day_xx/$DIR/g" "$DIR/main.py"

# Move problem description to final location
mv "${TEMP_PROBLEM}" "$DIR/problem.txt"

# Get the input and save to input.txt for the day
INPUT_URL="$PROBLEM_URL/input"
TEMP_INPUT="temp-input.txt"
curl "${INPUT_URL}" --compressed -f \
  -H "Cookie: session=${COOKIE}" \
  -o "${TEMP_INPUT}"

cp "${TEMP_INPUT}" "$DIR/input.txt"
rm "${TEMP_INPUT}"
COOKIE_FILE=".config/cookie"
if [ ! -f "$COOKIE_FILE" ]; then
    echo "Error: Cookie file not found at $COOKIE_FILE"
    exit 1
fi

# Create a new directory for the day with the template files for input and code.
DAY_PADDED=$(date +%d)
DIR="day_$DAY_PADDED"
cp -r "day_xx" "$DIR"
sed -i '' "s/day_xx/$DIR/g" "$DIR/main.py"

# Get the input and save to input.txt for the day.
COOKIE="$(< "$COOKIE_FILE" tr -d '\n')"
YEAR=$(date +%Y)
DAY=$(date +%-d)
INPUT_URL="https://adventofcode.com/$YEAR/day/$DAY/input"
TEMP_INPUT="temp-input.txt"
curl "${INPUT_URL}" --compressed \
  -H "Cookie: session=${COOKIE}" \
  -o "${TEMP_INPUT}"

cp ${TEMP_INPUT} "$DIR"/input.txt
rm ${TEMP_INPUT}
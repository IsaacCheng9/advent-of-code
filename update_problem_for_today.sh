# Configuration
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

# Check if the directory exists
if [ ! -d "$DIR" ]; then
    echo "Error: Directory $DIR does not exist. Please create the day's directory first."
    exit 1
fi

# Fetch the problem description
PROBLEM_URL="https://adventofcode.com/$YEAR/day/$DAY"
TEMP_PROBLEM="temp-problem.txt"

echo "Fetching updated problem description from $PROBLEM_URL..."

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

# Move new problem description to final location
mv "${TEMP_PROBLEM}" "$DIR/problem.txt"
echo "Successfully updated problem description in $DIR/problem.txt"
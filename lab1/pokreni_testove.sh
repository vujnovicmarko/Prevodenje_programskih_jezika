#!/bin/bash

TMP_DIR="testovi_tmp"
rm -rf "$TMP_DIR"
mkdir "$TMP_DIR"
unzip -q testovi.zip -d "$TMP_DIR"

PASSED=0
FAILED=0

for TEST_DIR in "$TMP_DIR"/*/; do
    echo "Running test in $(basename "$TEST_DIR")..."
    python GLA.py < "$TEST_DIR/test.lan" > /dev/null
    OUTPUT=$(python analizator/LA.py < "$TEST_DIR/test.in")
    if diff -q <(echo "$OUTPUT") "$TEST_DIR/test.out" > /dev/null; then
        echo "PASSED"
        ((PASSED++))
    else
        echo "FAILED"
        ((FAILED++))
    fi
done

echo
echo "========================="
echo "Tests passed: $PASSED"
echo "Tests failed: $FAILED"

rm -rf "$TMP_DIR"

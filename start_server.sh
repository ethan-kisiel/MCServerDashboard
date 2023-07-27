# cd bedrock-server
# chmod +x bedrock_server
# LD_LIBRARY_PATH=. ./bedrock_server

while true; do
    # Prompt the user for input
    read -p "Enter your input: " input

    # Check if the input is "stop"
    if [ "$input" = "stop" ]; then
        echo "Exiting the loop."
        break  # Exit the loop
    else
        echo "You entered: $input"
    fi
done
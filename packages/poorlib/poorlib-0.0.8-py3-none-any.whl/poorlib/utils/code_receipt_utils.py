def code2receipt(p_receipt: str) -> int:
    # Step 1: Prepare the receipt string with 'MMMM' prefix and remove spaces
    v_temp_receipt = 'MMMM' + p_receipt.replace(' ', '')

    # Step 2: Extract the last 4 characters from v_temp_receipt
    v_receipt = v_temp_receipt[-4:]

    # Step 3: Initialize an empty result string
    v_result = ''

    # Step 4: Create a dictionary for the decoding logic
    decode_map = {
        'M': '0', 'O': '1', 'Y': '2', 'D': '3', 'T': '4', 'U': '5', 'H': '6', 'C': '7', 'I': '8', 'K': '9',
        '5': '0', '0': '1', '2': '2', '1': '3', '7': '4', '4': '5', '9': '6', '8': '7', '3': '8', '6': '9',
        'V': '1', 'W': '8', 'X': '1', 'Z': '3'
    }

    # Step 5: Loop through the first 4 characters of v_receipt and decode using the map
    for i in range(4):
        v_result += decode_map.get(v_receipt[i], '')

    # Step 6: Convert the result string to a number and return
    return int(v_result)


def receipt2code(p_receipt: int) -> str:
    # Step 1: Prepare the receipt string with '0000' prefix and remove spaces
    v_temp_receipt = '0000' + str(p_receipt).replace(' ', '')

    # Step 2: Extract the last 4 characters from v_temp_receipt
    v_receipt = v_temp_receipt[-4:]

    # Step 3: Initialize an empty result string
    v_result = ''

    # Step 4: Create two dictionaries for the decode logic based on conditions
    decode_odd_map = {
        '0': 'M', '1': 'V', '2': 'Y', '3': 'D', '4': 'T', '5': 'U', '6': 'H', '7': 'C', '8': 'W', '9': 'K'
    }

    decode_even_map = {
        '0': '5', '1': 'X', '2': '2', '3': 'Z', '4': '7', '5': '4', '6': '9', '7': '8', '8': '3', '9': '6'
    }

    # Step 5: Loop through the first 4 characters of v_receipt
    for i in range(4):
        # Calculate mod condition based on the current digit, sum of digits, and index (i+1 for 1-based index)
        current_digit = int(v_receipt[i])
        last_digit = int(v_receipt[-1])
        mod_value = (current_digit + last_digit + (i + 1)) % 2

        if mod_value != 0:
            # Use the odd decode map
            v_result += decode_odd_map.get(v_receipt[i], '')
        else:
            # Use the even decode map
            v_result += decode_even_map.get(v_receipt[i], '')

    # Step 6: Return the resulting string
    return v_result
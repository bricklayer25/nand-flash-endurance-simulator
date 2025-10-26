import bitarray as ba
import uuid

# --- Pre-calculated table for which bits each parity bit checks ---
PARITY_BIT_TABLE = {
    p_bit: [bit_pos for bit_pos in range(1, 72) if (bit_pos & p_bit)]
    for p_bit in (1, 2, 4, 8, 16, 32, 64)
}

def encode(data_str: str) -> ba.bitarray:
    """
    Encodes a 64-bit data string into a 72-bit SECDED Hamming codeword.
    This function is correct.
    """
    codeword = ba.bitarray(72)
    codeword.setall(0)
    data_idx = 0

    # Place all 64 data bits
    for i in range(72):
        pos = i + 1 # 1-based position
        is_power_of_two = (pos & (pos - 1) == 0) and pos != 0
        is_oparity_bit = (pos == 72)

        if is_power_of_two or is_oparity_bit:
            continue

        codeword[i] = int(data_str[data_idx])
        data_idx += 1
        
    # Calculate and set the 7 Hamming parity bits 
    for key in PARITY_BIT_TABLE:
        positions_to_check = PARITY_BIT_TABLE[key]
        p_bit = xor_at_positions(codeword, *positions_to_check)
        codeword[key-1] = p_bit 

    # Calculate and set the 8th (Overall) parity bit 
    oparate = 0
    for bit in codeword:
        oparate ^= int(bit)
    
    codeword[71] = oparate
    return codeword


def xor_at_positions(codeword: ba.bitarray, *positions: int) -> int:
    """
    Helper function to XOR bits at specified 1-based positions.
    This function is correct.
    """
    result = 0
    for pos in positions: #these are one based
        idx = pos - 1
        result ^= int(codeword[idx])
    return result


def decode(codeword: ba.bitarray) -> (str, int):
    """
    Decodes a 72-bit SECDED codeword and reports its status.
    Returns a tuple: (status_message, error_position)
    error_position is 0 if no correctable error.
    """
    
    # Calculate the 7-bit Hamming Syndrome
    s_list = []
    for p_bit in (1, 2, 4, 8, 16, 32, 64):
        positions_to_check = PARITY_BIT_TABLE[p_bit]
        check_bit = xor_at_positions(codeword, *positions_to_check)
        s_list.append(check_bit) # List will be [s1, s2, s4, ...]

    # Convert the syndrome list [s1, s2, s4...] into an integer
    # This integer is the "error pointer"
    s_h_int = 0
    for i, bit in enumerate(s_list):
        if bit == 1:
            s_h_int += (1 << i) # Reconstructs the position: 1*s1 + 2*s2 + 4*s4...
            
    # Calculate the 1-bit Overall Parity Syndrome
    s_p = 0
    for bit in codeword:
        s_p ^= int(bit)

    # Interpret the two syndromes together
    
    # s_h_int is the Hamming Syndrome (7 bits)
    # s_p is the Overall Parity (1 bit)

    if s_h_int == 0 and s_p == 0:
        return ("NO_ERROR", 0)
    
    elif s_h_int != 0 and s_p == 1:
        # This is a correctable single-bit error.
        # s_h_int is the 1-based position of the error.
        return ("SINGLE_ERROR", s_h_int)

    elif s_h_int != 0 and s_p == 0:
        # The Hamming bits found an error, but the overall parity
        # is correct. This indicates a double error.
        return ("DOUBLE_ERROR_DETECTED", 0)

    elif s_h_int == 0 and s_p == 1:
        # The Hamming bits are fine, but the overall parity is not.
        # This means the overall parity bit itself (pos 72) is the error.
        return ("SINGLE_ERROR", 72)
    
    # This should not be reachable
    return ("UNKNOWN_ERROR", 0)

def flip_bit(codeword: ba.bitarray, one_based_pos: int):
    """Helper function to test errors."""
    idx = one_based_pos - 1
    codeword[idx] = not codeword[idx]
    print(f"\n--- Flipped bit at position {one_based_pos} ---")


# #  Main execution 
# int_64_str = format(uuid.uuid4().int & (1<<64)-1, '064b')
# print(f"Original data: {int_64_str}")

# encoded_data = encode(int_64_str)
# print(f"Encoded data:  {encoded_data.to01()}")

# # Test 1: Check the clean data
# status, err_pos = decode(encoded_data)
# print(f"Clean data check: {status} (Error at pos: {err_pos})")

# # Test 2: Check a single data bit error
# # flip a data bit (e.g., at position 42)
# flip_bit(encoded_data, 42)
# status, err_pos = decode(encoded_data)
# print(f"Single error check: {status} (Error at pos: {err_pos})")

# # Test 3: Check a double bit error
# # flip another bit (e.g., at position 10)
# flip_bit(encoded_data, 10)
# status, err_pos = decode(encoded_data)
# print(f"Double error check: {status} (Error at pos: {err_pos})")

# # Test 4: Check a single parity bit error
# # re-encode to get a clean copy
# encoded_data = encode(int_64_str)
# # flip a parity bit (e.g., at position 4)
# flip_bit(encoded_data, 4)
# status, err_pos = decode(encoded_data)
# print(f"Single parity error check: {status} (Error at pos: {err_pos})")


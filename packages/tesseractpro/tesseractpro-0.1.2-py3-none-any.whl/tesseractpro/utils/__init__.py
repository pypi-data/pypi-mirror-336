def timeframe_align(input: int, timeframe: int) -> int:
    remainder = input % timeframe
    if remainder < timeframe / 2:
        # Round down if the remainder is less than half of 1920
        aligned_timestamp = input - remainder
    else:
        # Round up if the remainder is greater than or equal to half of 1920
        aligned_timestamp = input + (timeframe - remainder)

    return aligned_timestamp

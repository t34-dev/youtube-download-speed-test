def select_best_format(codecs, resolution):
    # Priority order for codecs
    codec_priority = ['av01', 'vp09', 'avc1']

    # Find the highest priority codec from the input list
    selected_codec = None
    for priority_codec in codec_priority:
        for codec in codecs:
            if priority_codec in codec.lower():
                selected_codec = codec
                break
        if selected_codec:
            break

    # If no preferred codec found, select the first one
    if not selected_codec and codecs:
        selected_codec = codecs[0]

    # Determine the best format
    if selected_codec:
        format = get_optimal_format(selected_codec, resolution)
        return format, selected_codec
    else:
        return None, None  # Return None if no codec found

def get_optimal_format(codec, resolution):
    # Normalize input data
    codec = codec.lower()
    resolution = resolution.lower()

    # Dictionary mapping codecs to their preferred formats
    codec_format_map = {
        'av01': 'mp4',
        'avc1': 'mp4',
        'vp09': 'webm',
        'mp4a': 'mp4',
    }

    # Special cases
    if 'avc1' in codec and resolution in ['360p', '480p']:
        return 'mp4'

    # Look for the codec in the dictionary
    for key in codec_format_map:
        if key in codec:
            return codec_format_map[key]

    # If codec not found, return mp4 as the most universal format
    return 'mp4'

# Example usage
# codecs = ['vp09.00.40.08', 'avc1.4d401f', 'av01.0.12M.08', 'vp09.00.50.08']
# resolution = '720p'
#
# best_format = select_best_format(codecs, resolution)
# print(f"Best format for {resolution}: {best_format}")

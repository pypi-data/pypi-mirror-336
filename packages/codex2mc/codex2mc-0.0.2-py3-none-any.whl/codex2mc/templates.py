def info_dic(target_pattern):
    """
    creates a dictionary with keys mirroring the keys in the target_pattern dictionary.
    The value of each key is an empty string.
    Args:
        target_pattern (dict): dictionary taken from the codex_pattern function.
    Returns:
        dict: template with keys from codex_pattern plus 2 extra keys, full path of image and image name.
    """

    # Initialize dictionary
    template = {"full_path": "", "img_name": "","cycle":"","roi":""}

    for key in target_pattern:
        template[key] = ""

    return template


def codex_pattern(version=1):
    """
    Returns a dictionary with regular expressions to extract metadata from codex filenames.
    Args:
        version (int): version of the codex filenames. Default is 1.
    Returns:
        dict: dictionary with regular expressions to extract metadata from codex filenames.
    """

    if version == 1:
        
        pattern = {
            "tile"     : r"_(.*?)_",
            "plane"    : r"_Z(.*?)_",
            "channel"  : r"_CH(\d+)",
        }

    return pattern

"""
Module for removing namespaces from rpc-reply.
namespaces are keys on a dictionary
"""

from collections import deque
from typing import Any, Dict

KEYS_TO_REMOVE = {"@xmlns", "@xmlns:nc"}


def remove_namespaces_from_dict(
    data: Dict[str, Any], depth_limit=10
) -> Dict[str, Any]:
    """
    Remove specified keys from a dictionary up to a certain depth.

    Args:
        data (Dict[str, Any]): The original dictionary.
        depth_limit (int): The maximum depth to search into the dictionary.
                           Default is 10.
                           After the depth is reached, the remaining
                           dictionaries are copied and not processed.

    Returns:
        Dict[str, Any]: A new dictionary without the specified keys.
    """
    queue = deque([((), data)])
    result = {}

    while queue:
        path, current_data = queue.popleft()
        depth = len(path)

        for key, value in current_data.items():
            if key in KEYS_TO_REMOVE and depth < depth_limit:
                continue

            new_path = path + (key,)

            if isinstance(value, dict) and depth < depth_limit - 1:
                queue.append((new_path, value))
            else:
                current_level = result
                for sub_key in new_path[:-1]:
                    current_level = current_level.setdefault(sub_key, {})
                current_level[new_path[-1]] = value

    return result

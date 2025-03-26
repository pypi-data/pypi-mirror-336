import streamlit.components.v1 as components
import os
_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "message_reflector",
        url="http://localhost:3000"
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")

    _component_func = components.declare_component(
        "message_reflector",
        path=build_dir
    )


def message_reflector(message: str, delay_ms: int = 1000, key: str = None):
    """
    Create a message reflector that reflects messages to the client.
    
    Args:
        message: The message to reflect
        id: The id of the message, if the id is the same as the last message, the message will not be reflected
        delay_ms: The delay time in milliseconds
        key: An optional key for the component
        
    Returns:
        The message if it hasn't been processed before, None if it has been processed
        or if there's no message
    """

    message_data = _component_func(message=message, delay_ms=delay_ms, key=key, default=None)

    return message_data
    

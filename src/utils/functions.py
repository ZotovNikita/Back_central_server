async def is_command(message: str) -> bool:
    return message.startswith('/')

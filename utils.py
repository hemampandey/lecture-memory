
def format_timestamp(seconds: float) -> str:
    """Convert 532.4 → '00:08:52'"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
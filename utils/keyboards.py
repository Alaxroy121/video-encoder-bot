from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import CODEC_OPTIONS, SPEED_OPTIONS, RESOLUTION_OPTIONS

def create_codec_keyboard():
    """Create codec selection buttons"""
    buttons = [
        [InlineKeyboardButton(text=codec, callback_data=f"codec_{codec}") 
         for codec in CODEC_OPTIONS.keys()]
    ]
    return InlineKeyboardMarkup(buttons)

def create_speed_keyboard():
    """Create encoding speed selection buttons"""
    buttons = []
    speeds = list(SPEED_OPTIONS.keys())
    for i in range(0, len(speeds), 3):
        row = [InlineKeyboardButton(text=speed, callback_data=f"speed_{speed}") 
               for speed in speeds[i:i+3]]
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

def create_resolution_keyboard():
    """Create resolution selection buttons"""
    buttons = []
    resolutions = list(RESOLUTION_OPTIONS.keys())
    for i in range(0, len(resolutions), 2):
        row = [InlineKeyboardButton(text=res, callback_data=f"resolution_{res}") 
               for res in resolutions[i:i+2]]
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

def create_crf_keyboard():
    """Create CRF (quality) selection buttons"""
    buttons = []
    crfs = ["Low (18)", "Medium (23)", "High (28)", "Very High (35)", "Maximum (40)"]
    values = [18, 23, 28, 35, 40]
    for crf_text, crf_value in zip(crfs, values):
        button = InlineKeyboardButton(text=crf_text, callback_data=f"crf_{crf_value}")
        buttons.append([button])
    return InlineKeyboardMarkup(buttons)

def create_bitcolor_keyboard():
    """Create 10-bit color option"""
    buttons = [
        [
            InlineKeyboardButton(text="8-bit (Standard)", callback_data="bitcolor_8"),
            InlineKeyboardButton(text="10-bit (HDR)", callback_data="bitcolor_10")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

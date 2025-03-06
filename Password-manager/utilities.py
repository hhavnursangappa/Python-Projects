import enum


class FontStyles(enum.Enum):
	"""Enum class which defines the different font styles"""

	FONT_NAME = 'Constantia'

	HEADING1 = (FONT_NAME, 26, "bold")
	HEADING2 = (FONT_NAME, 16)
	HEADING3 = (FONT_NAME, 14)
	NORMAL_TEXT = (FONT_NAME, 12)

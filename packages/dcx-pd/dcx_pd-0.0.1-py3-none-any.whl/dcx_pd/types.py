from functools import partial as _partial


def _hex2(number: int, leading_zeroes=2, *, upper=True, prefix: str = "0x") -> str:
	"""Slightly more advanced version of builtin `hex()`, offers ability to choose if uppercase and how many leading zeroes."""
	hex_output = hex(number)
	hex_value = hex_output[2:].zfill(leading_zeroes).upper() if upper else hex_output[2:].zfill(leading_zeroes)

	formatted_output = f"{prefix}{hex_value}"
	if not upper:
		formatted_output = formatted_output.lower()

	return formatted_output


class HexInt(int):
	leading_zeroes: int

	def __new__(cls, x, /, *, leading_zeroes=None, prefix=None, **kwargs):
		return super().__new__(cls, x, **kwargs)

	def __init__(self, x, /, *, leading_zeroes=6, prefix="0x", **_):
		self.leading_zeroes = leading_zeroes
		self.prefix = prefix
		super().__init__()

	def __tcr_fmt__(self, fmt_iterable, **kwargs):
		return fmt_iterable(int(self), **{**kwargs, "int_formatter": _partial(_hex2, leading_zeroes=self.leading_zeroes, prefix=self.prefix)})

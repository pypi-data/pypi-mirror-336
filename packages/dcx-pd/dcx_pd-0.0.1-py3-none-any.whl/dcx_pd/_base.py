import pydantic as pd


def _snake_to_camel(s: str, always_uppercase: tuple[str] = (), unless_str_in_always_uppercase: bool = False) -> str:
	if unless_str_in_always_uppercase and s.lower() in always_uppercase:
		return s

	words = s.split("_")
	converted = words[0] + "".join(word.title() for word in words[1:])

	for word in always_uppercase:
		converted = converted.replace(word.title(), word.upper())

	return converted


class BM(pd.BaseModel):
	model_config = pd.ConfigDict(
		extra="ignore",  # change to forbid during feature upgrade
		arbitrary_types_allowed=True,
		validate_assignment=True,
		validate_default=True,
		alias_generator=_snake_to_camel,
	)

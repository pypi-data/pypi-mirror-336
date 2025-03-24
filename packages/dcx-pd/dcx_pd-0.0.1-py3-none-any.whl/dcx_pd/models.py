import datetime as _dt
import json as _json
from enum import StrEnum as _StrEnum
from pathlib import Path as _Path

from . import types as _types
from ._base import BM as _BM
from ._base import pd as _pd


class ColorBM(_BM):
	color: _types.HexInt | None = None

	@_pd.field_validator("color", mode="before")
	@classmethod
	def _convert_color(cls, v):
		if v is None:
			return None

		return _types.HexInt(f"{v}".removeprefix("#"), base=16)


class Guild(_BM):
	id: int
	name: str
	icon_url: str


class ChannelType(_StrEnum):
	TEXT = "GuildTextChat"
	VOICE = "GuildVoiceChat"
	DM = "DirectTextChat"
	GROUP_DM = "DirectGroupTextChat"
	NEWS = "GuildNews"
	THREAD = "GuildPublicThread"
	"""Can be both either free-standing thread, or a forum channel thread."""


class Channel(_BM):
	id: int
	type: ChannelType
	category_id: int | None
	category_name: str | None = _pd.Field(alias="category")
	icon_url: str | None = None
	"""Group DM Icon, None if not a group DM channel."""
	name: str
	topic: str | None


class DateRange(_BM):
	after: _dt.datetime | None
	before: _dt.datetime | None


class MessageType(_StrEnum):
	DEFAULT = "Default"
	REPLY = "Reply"
	CALL = "Call"
	THREAD_CREATED = "ThreadCreated"
	GUILD_MEMBER_JOIN = "GuildMemberJoin"
	PINNED_MESSAGE = "ChannelPinnedMessage"
	GROUP_DM_CHANNEL_NAME_CHANGE = "ChannelNameChange"
	GROUP_DM_CHANNEL_ICON_CHANGE = "ChannelIconChange"
	GROUP_DM_RECIPIENT_ADD = "RecipientAdd"
	GROUP_DM_RECIPIENT_REMOVE = "RecipientRemove"

	# Huh????
	_9 = "9"
	_23 = "23"
	_20 = "20"
	_8 = "8"

	THREAD_FIRST_MESSAGE = "21"
	POLL_WINNING_ANSWER = "46"


class Role(ColorBM):
	id: int
	name: str
	position: int


class User(ColorBM):
	id: int
	name: str
	discriminator: str
	nickname: str | None
	is_bot: bool
	avatar_url: str
	roles: list[Role] | None = None


class Attachment(_BM):
	id: int
	url: str
	filename: str = _pd.Field(alias="fileName")
	size_bytes: int = _pd.Field(alias="fileSizeBytes")


class EmbedAuthor(_BM):
	name: str
	url: str | None
	icon_url: str | None = None


class EmbedThumbnail(_BM):
	url: str
	width: int
	height: int


class EmbedVideoOrImage(_BM):
	url: str
	width: int
	height: int


class EmbedField(_BM):
	name: str
	value: str
	is_inline: bool


class EmbedFooter(_BM):
	text: str
	icon_url: str | None = None


class Emoji(_BM):
	id: int | None
	name: str
	code: str
	is_animated: bool
	image_url: str

	@_pd.field_validator("id", mode="before")
	@classmethod
	def _convert_color(cls, v):
		if v == "":
			return None

		return int(v)


class Embed(ColorBM):
	title: str
	description: str
	url: str | None
	timestamp: _dt.datetime | None
	author: EmbedAuthor | None = None
	thumbnail: EmbedThumbnail | None = None
	video: EmbedVideoOrImage | None = None
	image: EmbedVideoOrImage | None = _pd.Field(exclude=True, default=None)  # Included in images[0]
	images: list[EmbedVideoOrImage]
	fields: list[EmbedField]
	footer: EmbedFooter | None = None
	inline_emojis: list[Emoji] | None = None


class Sticker(_BM):
	id: int
	name: str
	format: str
	source_url: str


class Reaction(_BM):
	emoji: Emoji
	count: int
	users: list[User]


class MessageReference(_BM):
	message_id: int
	channel_id: int
	guild_id: int | None


class MessageInteraction(_BM):
	id: int
	name: str
	user: User


class Message(_BM):
	id: int
	type: MessageType
	timestamp: _dt.datetime
	timestamp_edited: _dt.datetime | None
	timestamp_call_ended: _dt.datetime | None = _pd.Field(alias="callEndedTimestamp")
	is_pinned: bool
	content: str
	author: User
	attachments: list[Attachment]
	embeds: list[Embed]
	stickers: list[Sticker]
	reactions: list[Reaction]
	mentions: list[User]
	inline_emojis: list[Emoji] | None = None
	reference: MessageReference | None = None
	interaction: MessageInteraction | None = None


class Export(_BM):
	guild: Guild
	channel: Channel
	date_range: DateRange
	exported_at: _dt.datetime
	message_count: int = _pd.Field(exclude=True)  # excluded due to possible desync with len(self.messages)
	messages: list[Message]

	@classmethod
	def from_strjson(cls, s: str):
		return cls(**_json.loads(s))

	@classmethod
	def from_path(cls, path: _Path):
		return cls.from_strjson(path.read_text(encoding="utf-8"))

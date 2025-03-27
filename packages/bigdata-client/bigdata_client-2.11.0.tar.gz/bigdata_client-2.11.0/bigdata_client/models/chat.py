from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, computed_field, field_validator

from bigdata_client.connection_protocol import BigdataConnectionProtocol
from bigdata_client.constants import MAX_CHAT_QUESTION_LENGTH, MIN_CHAT_QUESTION_LENGTH
from bigdata_client.enum_utils import StrEnum
from bigdata_client.exceptions import BigdataClientChatInvalidQuestion


class ChatScope(StrEnum):
    EARNING_CALLS = "transcripts"
    FILES = "files"
    NEWS = "news"
    REGULATORY_FILINGS = "filings"


class ChatSource(BaseModel):
    """Represents a source in a chat message"""

    id: str
    headline: str
    url: Optional[str]
    document_scope: Optional[str]
    rp_provider_id: Optional[str]


class InlineAttributionFormatter(ABC):
    """Interface for formatting inline attributions in chat messages"""

    @abstractmethod
    def format(self, index: int, source: ChatSource) -> str:
        """
        Format an inline attribution.

        Args:
            index (int): The index of the attribution within the list of attributions.
            source (ChatSource): The inline attribution to format.

        Returns:
            str: A string representing the formatted attribution.
        """


class DefaultFormatter(InlineAttributionFormatter):
    """Default formatter for inline attributions in chat messages"""

    def format(self, index: int, source: ChatSource) -> str:
        """
        Format an inline attribution using a default reference style.

        Args:
            index (int): The index of the attribution within the list of attributions.
            source (ChatSource): The inline attribution to format.

        Returns:
            str: A string representing the formatted attribution in default reference style.
        """
        return f"`:ref[{index}]` "


class MarkdownLinkFormatter(InlineAttributionFormatter):
    """Formatter for inline attributions in chat messages that uses Markdown links"""

    def __init__(
        self, headline_length: Optional[int] = None, skip_empty_urls: bool = True
    ):
        """
        Initialize the MarkdownLinkInlineAttributionFormatter.

        Args:
            headline_length (int): The maximum length of the headline to be displayed in the link. Default is 10.
        """
        self.headline_length = headline_length

    def format(self, index: int, source: ChatSource) -> str:
        """
        Format an inline attribution as a Markdown link.

        Args:
            index (int): The index of the attribution within the list of attributions.
            source (ChatSource): The inline attribution to format.

        Returns:
            str: A string representing the formatted attribution as a Markdown link.
        """
        hd = source.headline
        if self.headline_length:
            hd = source.headline[: self.headline_length]
        url = source.url or ""
        if url == "":
            return ""
        return f"[{hd}]({url}) "


class ChatInteraction(BaseModel):
    """Represents a single interaction with chat"""

    question: str
    answer: str
    interaction_timestamp: str
    date_created: datetime
    last_updated: datetime
    scope: Optional[ChatScope] = None
    sources: list[ChatSource] = Field(default=[])

    @field_validator("scope", mode="before")
    @classmethod
    def validate_scope(cls, value):
        if isinstance(value, str):
            try:
                return ChatScope(value)
            except ValueError:
                return None
        return value


class Chat(BaseModel):
    id: str
    name: str
    user_id: str
    date_created: datetime
    last_updated: datetime

    @computed_field
    @property
    def interactions(self) -> list[ChatInteraction]:
        if not self._loaded:
            self.reload_from_server()
        return self._interactions

    _api_connection: BigdataConnectionProtocol
    _interactions: list[ChatInteraction]
    _formatter: InlineAttributionFormatter
    _loaded: bool

    def __init__(
        self,
        _api_connection: BigdataConnectionProtocol,
        _interactions: Optional[list[ChatInteraction]],
        _formatter: Optional[InlineAttributionFormatter],
        _loaded: bool = False,
        **values,
    ):
        super().__init__(**values)
        self._api_connection = _api_connection
        self._loaded = _loaded

        if _interactions is not None:
            self._interactions = _interactions

        self._formatter = _formatter or DefaultFormatter()

    def ask(
        self,
        question: str,
        *,
        scope: Optional[ChatScope] = None,
        formatter: Optional[InlineAttributionFormatter] = None,
    ) -> ChatInteraction:
        """Ask a question in the chat"""
        self._validate_question(question)
        formatter = formatter or self._formatter
        chat_scope = scope.value if scope else None
        chat_response = self._api_connection.ask_chat(
            self.id, question, scope=chat_scope
        )
        complete_message = chat_response.complete_message
        answer = complete_message.content_block.get("value", "")
        sources = chat_response.to_chat_source()

        from bigdata_client.api.chat import ChatInteraction as ApiChatInteraction

        answer = ApiChatInteraction._parse_references(answer, sources, formatter)
        now = datetime.utcnow()
        interation = ChatInteraction(
            question=question,
            answer=answer,
            interaction_timestamp=complete_message.interaction_timestamp,
            date_created=now,
            last_updated=now,
            scope=scope,
            sources=sources,
        )
        self._interactions.append(interation)
        return interation

    def reload_from_server(self):
        chat = self._api_connection.get_chat(self.id).to_chat_model(
            self._api_connection, self._formatter
        )
        self.name = chat.name
        self.user_id = chat.user_id
        self.date_created = chat.date_created
        self.last_updated = chat.last_updated
        self._interactions = chat._interactions
        self._loaded = True

    def delete(self):
        """Delete the chat"""
        self._api_connection.delete_chat(self.id)

    @staticmethod
    def _validate_question(question: str):
        message_length = len(question or "")
        if not (MIN_CHAT_QUESTION_LENGTH < message_length < MAX_CHAT_QUESTION_LENGTH):
            raise BigdataClientChatInvalidQuestion(message_length)

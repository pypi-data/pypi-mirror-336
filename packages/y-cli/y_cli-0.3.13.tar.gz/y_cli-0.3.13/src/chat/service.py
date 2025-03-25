from datetime import datetime
import sys
import os
from typing import List, Optional, Dict
from chat.models import Chat, Message
from .repository import ChatRepository
import time

from util import get_iso8601_timestamp, get_unix_timestamp, generate_id
from config import config

IS_WINDOWS = sys.platform == 'win32'

class ChatService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    def _create_timestamp(self) -> str:
        """Create an ISO format timestamp"""
        return get_iso8601_timestamp()

    async def list_chats(self, keyword: Optional[str] = None, model: Optional[str] = None,
                   provider: Optional[str] = None, limit: int = 10) -> List[Chat]:
        """List chats with optional filtering

        Args:
            keyword: Optional text to filter messages by content
            model: Optional model name to filter by
            provider: Optional provider name to filter by
            limit: Maximum number of chats to return (default: 10)

        Returns:
            List of chats filtered by the given criteria, sorted by creation time descending
        """
        return await self.repository.list_chats(keyword=keyword, model=model, provider=provider, limit=limit)

    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        """Get a specific chat by ID"""
        return await self.repository.get_chat(chat_id)

    async def create_chat(self, messages: List[Message], external_id: Optional[str] = None, chat_id: Optional[str] = None) -> Chat:
        """Create a new chat with messages and optional external ID

        Args:
            messages: List of messages to include in the chat
            external_id: Optional external identifier for the chat
            chat_id: Optional chat ID to use (if not provided, one will be generated)

        Returns:
            The created chat object
        """
        timestamp = self._create_timestamp()
        chat = Chat(
            id=chat_id if chat_id else generate_id(),
            create_time=timestamp,
            update_time=timestamp,
            messages=[msg for msg in messages if msg.role != 'system'],
            external_id=external_id
        )
        return await self.repository.add_chat(chat)

    async def update_chat(self, chat_id: str, messages: List[Message], external_id: Optional[str] = None) -> Chat:
        """Update an existing chat's messages"""
        chat = await self.get_chat(chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        chat.update_messages(messages)
        chat.external_id = external_id
        return await self.repository.update_chat(chat)

    async def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat by ID"""
        return await self.repository.delete_chat(chat_id)

    async def generate_share_html(self, chat_id: str) -> str:
        """Generate HTML file for sharing a chat using pandoc

        Args:
            chat_id: ID of the chat to share

        Returns:
            Path to the generated HTML file

        Raises:
            ValueError: If chat not found
        """
        chat = await self.get_chat(chat_id)
        if not chat:
            raise ValueError(f"Chat with id {chat_id} not found")

        # Generate markdown content
        md_content = f"# Chat {chat_id}\n\n"
        for msg in chat.messages:
            if msg.role == 'system':
                continue

            # Add role with model/provider info if available
            header = msg.role.capitalize()
            if msg.model or msg.provider:
                model_info = []
                if msg.model:
                    model_info.append(msg.model)
                if msg.provider:
                    model_info.append(f"via {msg.provider}")
                header += f" <span class='model-info'>({' '.join(model_info)})</span>"

            md_content += f"## {header}\n\n"

            # Add reasoning content in a collapsible section if it exists
            if msg.reasoning_content:
                md_content += f'<details><summary>Reasoning</summary><div class="reasoning-content">\n\n{msg.reasoning_content}\n\n</div></details>\n\n'

            md_content += f"{msg.content}\n\n"
            
            # Add MCP server/tool info if available
            if msg.role == 'assistant' and (msg.server or msg.tool):
                mcp_info = "```\n"
                if msg.server:
                    mcp_info += f"Server: {msg.server}\n"
                if msg.tool:
                    mcp_info += f"Tool: {msg.tool}\n"
                if msg.arguments:
                    import json
                    mcp_info += f"Arguments: {json.dumps(msg.arguments, indent=2, ensure_ascii=False)}\n"
                mcp_info += "```\n"
                md_content += f"{mcp_info}\n"
            
            md_content += f"*{msg.timestamp}*\n\n---\n\n"

        # ensure tmp directory exists
        os.makedirs(config["tmp_dir"], exist_ok=True)

        # Write markdown to temporary file
        md_file = os.path.join(config["tmp_dir"], f"{chat_id}.md")
        html_file = os.path.join(config["tmp_dir"], f"{chat_id}.html")

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Create CSS
        css = '''
<style>
body { max-width: 800px; margin: 0 auto; padding: 2rem; font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; }
h1 { border-bottom: 2px solid #eee; padding-bottom: 0.5rem; }
h2 { margin-top: 2rem; color: #2563eb; }
h3 { color: #4b5563; }
sup { color: #6b7280; }
hr { margin: 2rem 0; border: 0; border-top: 1px solid #eee; }
.references { background: #f9fafb; padding: 1rem; border-radius: 0.5rem; }
.images { margin: 1rem 0; }
details {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    margin: 1rem 0;
    padding: 0.5rem;
}
summary {
    cursor: pointer;
    font-weight: 500;
    color: #4b5563;
}
details[open] summary {
    margin-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.5rem;
}
.reasoning-content {
    padding: 0.5rem;
    color: #4b5563;
}
.model-info {
    font-size: 0.875rem;
    font-weight: normal;
    color: #6b7280;
}
code {
    background: #f1f5f9;
    border-radius: 0.25rem;
    padding: 0.2rem 0.4rem;
    font-size: 0.875rem;
}
pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    padding: 1rem;
    overflow-x: auto;
    margin: 1rem 0;
}
</style>
'''

        # Create temporary CSS file
        css_file = os.path.join(config["tmp_dir"], f"{chat_id}.css")
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(css)

        # Run pandoc
        pandoc_cmd = 'pandoc'
        if IS_WINDOWS:
            pandoc_cmd = os.path.expanduser('~/AppData/Local/Pandoc/pandoc')

        os.system(f'{pandoc_cmd} "{md_file}" -o "{html_file}" -s --metadata title="{chat_id}" --metadata charset="UTF-8" --include-in-header="{css_file}"')

        # Clean up temporary files
        os.remove(css_file)
        os.remove(md_file)

        return html_file

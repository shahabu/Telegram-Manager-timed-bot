class TelegramSession:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_file = f'accounts/{self.api_id}_{self.api_hash}'
        self.channel_count = None
        self.session = TelegramClient(
            self.session_file,
            self.api_id,
            self.api_hash
        )
        self._setup()

    async def view_posts(self):
        async with self.session:
            async for dialog in self.session.iter_dialogs():
                if isinstance(dialog.entity, Channel):
                    message_ids = [
                        msg.id async for msg in self.session.iter_messages(dialog.entity, limit=100)
                    ]
                    await self.session(GetMessagesViewsRequest(
                        peer=dialog,
                        id=message_ids,
                        increment=True
                    ))

import os
import logging

from session import TelegramSession

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
fmt = logging.Formatter('MANAGER | %(levelname)s | %(asctime)s | %(message)s', '%Y-%m-%d %H:%M:%S')
sh.setFormatter(fmt)
logger.addHandler(sh)


class TelegramManager:
    def __init__(self):
        self.sessions = []  # Manage sessions using a list internally
        self.path = 'accounts'
        self._setup()

    def _setup(self):
        if os.path.exists(self.path) and os.path.isdir(self.path):
            logger.info('Sessions folder exists')
            logger.info('Sessions loading started')

            session_files = os.scandir('accounts')
            for session_file in session_files:
                logger.info(f'Session {session_file.name} was found')
                api_id, api_hash = session_file.name.replace('.txt', '').split('_')
                session = TelegramSession(api_id, api_hash)
                self.sessions.append(session)
        else:
            logger.info('Sessions folder does not exist')
            os.mkdir(self.path)
            logger.info('Sessions folder was created')

    def add_session(self, api_id: str, api_hash: str):
        session = TelegramSession(api_id, api_hash)
        self.sessions.append(session)
        logger.info('Session was added')

    def follow_channel(self, channel: str, count: int):
        subscribed = 0
        for account in sorted(self.sessions, key=lambda x: x.channel_count):
            account.follow_channel(channel)
            subscribed += 1
            if subscribed >= count:
                break
        logger.info(f'Subscriptions to the channel {channel} in count {subscribed} of required {count} were added')

    async def view_posts(self, batch_size=10, interval=60):
        """
        View posts using a batch of accounts at a time.

        Args:
            batch_size (int): Number of accounts to process in one interval.
            interval (int): Time in seconds to wait between batches.
        """
        for i in range(0, len(self.sessions), batch_size):
            batch = self.sessions[i:i + batch_size]
            logger.info(f"Processing batch: {i // batch_size + 1}")
            await asyncio.gather(*(account.view_posts() for account in batch))
            if i + batch_size < len(self.sessions):  # Wait only if there are more accounts
                logger.info(f"Waiting {interval} seconds before processing the next batch.")
                await asyncio.sleep(interval)

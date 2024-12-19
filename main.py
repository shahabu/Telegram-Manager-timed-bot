import asyncio
from manager import TelegramManager

if __name__ == '__main__':
    with open('welcome.txt') as f:
        for line in f.readlines():
            print(line.strip())

    running = True
    manager = TelegramManager()

    while running:
        inp = input(
            '[x] 1. Add account to our system\n'
            '[x] 2. Subscribe to channel\n'
            '[x] 3. View all group posts\n'
            '[x] 4. Timed view posts\n'
            'Choose your choice => '
        )

        if inp.upper() == 'Q' or inp.upper() == 'QUIT':
            running = False
        elif inp == '1':
            api_id = input('Enter API_ID: ')
            api_hash = input('Enter API_HASH: ')
            manager.add_session(api_id, api_hash)
        elif inp == '2':
            channel = input('Enter channel username or invite id: ')
            count = int(input('Enter required subscribes count: '))
            manager.follow_channel(channel, count)
        elif inp == '3':
            asyncio.run(manager.view_posts())
        elif inp == '4':
            batch_size = int(input("Enter the number of accounts per batch (e.g., 10): "))
            interval = int(input("Enter the interval time in seconds (e.g., 60): "))
            asyncio.run(manager.view_posts(batch_size=batch_size, interval=interval))

"""cricnotifier - cricket live match score moniting for telegram channels."""
import time
import shelve
import hashlib
import logging
import click
from formatters import MessageFactory


from api import CricAPI
from notifiers import TelegramNotifier
from utils import SimpleKVDB

POLL_INTERVAL = 60

@click.command()
@click.option('--match-url',
              help='Cricbuzz url of the cricket match. Reads MATCH_URL env var.',
              envvar='CRIC_MATCH_URL',
              prompt=True)
@click.option('--score-interval',
              help='Score interval in minutes. To send live score notification intervally.'
                   ' Reads SCORE_INTERVAL env var.',
              envvar='SCORE_INTERVAL',
              default=40)
@click.option('--bot-token',
              help='Telegram bot token. The bot must be admin on the channel.'
                   ' Reads TELEGRAM_BOT_TOKEN env var.',
              envvar='TELEGRAM_BOT_TOKEN',
              prompt=True)
@click.option('--chat-id',
              help=('Numeric ID of a chat or name of a public channel with @.'
                    ' Reads COC_CHAT_ID env var.'),
              envvar='TELEGRAM_CHAT_ID',
              prompt=True)
@click.option('--matchlog',
              help='Matchlog file path.',
              envvar='MATCHLOG',
              default='matchlog.db',
              type=click.Path())
@click.option('--loglevel',
              default='WARNING',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL']),
              help="Set the logging level")


def main(match_url, bot_token, score_interval, chat_id, matchlog, loglevel):
    """Publish cricket live score events to a telegram channel."""
    if loglevel:
        logging.basicConfig(level=loglevel)

    cric_api = CricAPI(match_url)
    notifier = TelegramNotifier(bot_token, chat_id)

    with shelve.open(matchlog, writeback=True) as db:
        dbwrapper = SimpleKVDB(db)
        if match_url not in dbwrapper:
                dbwrapper[match_url] = {}
        monitor = MatchMonitor(dbwrapper, cric_api, notifier, match_url, score_interval)
        try:            
            monitor.start()
        finally:
            db.sync()
            db.close()

########################################################################
# Main Match monitor class
########################################################################

class MatchMonitor(object):
    def __init__(self, db, api, notifier, match_url, score_interval):
        """Scan matchlog for match updates.

        This is the top most class that puts everything together.
        Calling `start` method will block forever. Calling `update`
        will fetch one update, notify the changes and return.

        Arguments:
            db -- A persistant dictionary-like object.
            api -- Api object
            notifier -- Notifier object
        """
        self.db = db
        self.cric_api = api
        self.notifier = notifier
        self.match_url = match_url
        self.msg_factory = MessageFactory()
        self.live_score_interval_count = 0
        self.score_interval = score_interval

    def update(self, match_info):
        self.live_score_interval_count += 1

        if match_info.last_wicket:
            msg = self.msg_factory.create_wicket_msg(match_info.last_wicket)
            self.send_once(msg, match_info.last_wicket)            

        if match_info.bowlerwickets >= 5:
            msg = self.msg_factory.create_5wickets_msg(match_info.bowler)
            self.send_once(msg, match_info.bowler + '5 wicket hual')

        if match_info.batsmanrun >= 50:
            # for msg_id -> convert 155 to 150, 99 to 50 so on...
            century_floor = str(int(match_info.batsmanrun / 50) * 50)
            msg = self.msg_factory.create_player_score_msg(match_info)
            self.send_once(msg, match_info.batsman + century_floor)

        if match_info.match_update:
            self.live_score_interval_count = self.score_interval
            self.send_live_score_msg(match_info)

            msg = self.msg_factory.create_match_update_msg(match_info.match_update)
            self.send_once(msg, match_info.match_update)

        else:
            self.send_live_score_msg(match_info)

    def send_live_score_msg(self, match_info):
        if self.score_interval == self.live_score_interval_count and match_info.live_score:
            self.live_score_interval_count = 0
            msg = self.msg_factory.create_live_score_msg(match_info)
            self.send_once(msg, match_info.live_score)

    def is_msg_sent(self, msg_id):
        return self.db[self.match_url].get(msg_id.lower(), False)

    def mark_msg_as_sent(self, msg_id):
        tmp = self.db[self.match_url]
        tmp[msg_id.lower()] = True
        self.db[self.match_url] = tmp

    def send_once(self, msg, msg_id=None):
        if not msg_id:
            msg_id = hashlib.md5(msg.encode('utf-8')).hexdigest()

        if not self.is_msg_sent(msg_id):
            is_sent = self.send(msg)
            if is_sent:
                self.mark_msg_as_sent(msg_id)

    def send(self, msg):
        return self.notifier.send(msg)

    def start(self):
        """Send match events to telegram channel."""
        while True:
            try:
                match_info = self.cric_api.get_live_score()
                if match_info:
                    self.update(match_info)
            except Exception as err:
                if '403' in str(err):
                    print('App 403 error, retrying.')
                elif '500' in str(err):
                    print('App 500 internal server error, retrying.')
                elif '502' in str(err):
                    print('App 502 bad gateway, retrying.')
                elif '503' in str(err):
                    print('App 403 error, retrying.')
                elif '504' in str(err):
                    print('App 504 Gateway Timeout, retrying.')
                else:
                    self.notifier.send("☠️ 😵 App is broken boss! Come over and fix me please!")
                    raise

            time.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    main()

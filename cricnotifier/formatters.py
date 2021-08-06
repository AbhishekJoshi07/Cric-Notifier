########################################################################
# Message formatters
########################################################################

from utils import string_formater, century_calculator

class MessageFactory:

    def create_wicket_msg(self, last_wicket):
        msg_template = """🔴  <b>Wicket !!!</b>

{last_wicket_line1}
{last_wicket_line2}

__________________________________
"""

        data = string_formater(last_wicket).split('-', 1)
        msg = msg_template.format(
            last_wicket_line1 = data[0].strip(),
            last_wicket_line2 = data[1].strip()
        )

        return msg

    def create_live_score_msg(self, match_info):
        msg_template = """🔵  <b>Live :-</b>
        
Score🏏:   {score}

Run rate📈:   {runrate}

{batsman}:   {batssmanrun}{ballfaced}
4️s: {fours}     6️s: {sixes}

Partnership🤝:   {partnership}

Recent 🥎s:   {recentballs}

__________________________________
"""

        score = string_formater(match_info.live_score)
        msg = msg_template.format(
            score = score,
            runrate = match_info.current_runrate,
            batsman = match_info.batsman,
            batssmanrun = match_info.batsmanrun,
            ballfaced = match_info.batsman_ballsfaced,
            fours = match_info.batsaman_fours,
            sixes = match_info.batsaman_sixes,
            partnership = match_info.partnership,
            recentballs = match_info.recentballs
        )

        return msg

    def create_5wickets_msg(self, bowler_name):
        msg_template = """🥳  <b>5 Wicket haul :-</b>
        
{bowler} got 5 wickets !!!

__________________________________
"""

        msg = msg_template.format(
            bowler = string_formater(bowler_name)
        )

        return msg

    def create_player_score_msg(self, match_info):
        msg_template = """🥳  <b>{century_data} !!!</b>

{batsman}:   {batssmanrun}{ballfaced}
4️s: {fours}     6️s: {sixes}

__________________________________
"""

        msg = msg_template.format(
            century_data = century_calculator(match_info.batsmanrun),
            batsman = string_formater(match_info.batsman),
            batssmanrun = match_info.batsmanrun,
            ballfaced = match_info.batsman_ballsfaced,
            fours = match_info.batsaman_fours,
            sixes = match_info.batsaman_sixes
        )

        return msg

    def create_match_update_msg(self, update):
        msg_template = """📢  <b>Update :-</b>
        
{update}

__________________________________
"""

        msg = msg_template.format(update = update)

        return msg
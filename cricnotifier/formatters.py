########################################################################
# Message formatters
########################################################################
class MessageFactory:

    def create_preparation_msg(self, last_wicket):
        msg_template = """{imoji} Wicket !!!

{last_wicket_line1}
{last_wicket_line2}"""

        data = ''.join(last_wicket.split('\\')).split('-', 1)
        msg = msg_template.format(
            imoji = "🔴",
            last_wicket_line1 = data[0].strip(),
            last_wicket_line2 = data[1].strip()
        )

        return msg

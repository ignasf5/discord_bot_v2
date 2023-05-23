from discord.ext import commands

class Output(commands.Cog):
    def __init__(self, output):
        self.bot = output

        self.output = {
            'congrats' :            {'name': 'Congratulations'},
            'failed' :              {'name': 'Failed'},
            'warning' :             {'name': 'Warning'},
            'no_db' :               {'name': 'Sorry cant store data to DB right now'},
            'no_respond' :          {'name': 'Sorry, you took too long to respond'},
            'no_acc' :              {'name': 'No account name was given'},
            'no_user' :             {'name': 'User not found'},
            'no_user_given' :       {'name': 'Missing user'},
            'no_points' :           {'name': 'Missing points'},
            'acc_info' :            {'name': 'Account Info'},
            'registered' :          {'name': 'Registered '},
            'reg' :                 {'name': 'Successfully registered, you receive'},
            'no_reg' :              {'name': 'You have to be registered, use: !reg'},
            'no_reg_user' :         {'name': 'User is not registered'},
            'reg_yes' :             {'name': 'You are already registered, check: !user'},
            'balance' :             {'name': 'Your current balance'},
            'permissions' :         {'name': 'Permissions'},
            'curent_per' :          {'name': 'Current User Permissions:'},
            'acc_use' :             {'name': 'Account already in use: '},
            'no_permissions' :      {'name': 'You dont have permissions'},
            'new_perm' :            {'name': 'New permissions for:'},
            'enter_rank' :          {'name': 'Enter your Valorant rank'},
            'check_ranks' :         {'name': 'Check ranks - !ranks'},
            'check_perm' :          {'name': 'Check permissions - !per'},
            'update_rank' :         {'name': 'Successfully updated rank'},
            'current_rank' :        {'name': 'Your current rank'},
            'last_mod' :            {'name': 'Last modified:'},
            'my_rank' :             {'name': 'My rank:'},
            'no_rank' :             {'name': 'Rank does not exist'},
            'embed_issue' :         {'name': 'Sorry, registration issue with embed'},
            'user_info' :           {'name': 'User information'},
            'user_member_id' :      {'name': 'Member ID:'},
            'user_status' :         {'name': 'User Status:'},
            'user_created' :        {'name': 'User Creation Time:'},
            'status_online' :       {'name': 'Online'},
            'status_dnd' :          {'name': 'Do not disturb'},
            'status_offline' :      {'name': 'Offline'},
            'status_away' :         {'name': 'Away'},
            'youtube_none' :        {'name': 'Please provide search information'},
            'translate_none' :      {'name': 'Please provide information'},
            'no_game_mode' :        {'name': 'Please provide a game mode (bo1 or bo3)'},
            'wrong_game_mode' :     {'name': 'Invalid game mode. Please choose between bo1 and bo3'},
            'game_started' :        {'name': 'Started Valorant Game'},
            'no_game' :             {'name': 'No game is currently active'},
            'game_inprogress' :     {'name': 'The game is already in progress'},
            'game_stop' :           {'name': 'The game has been stopped. You can start a new game'},
            'no_game_per' :         {'name': 'You do not have the necessary permissions to start the game'},
            'already_joined' :      {'name': 'Already joined'},
            'not_joined' :          {'name': 'You are not currently part of the game'},
            'game_full' :           {'name': 'The game is already full'},
            'no_players' :          {'name': 'No players have joined the game yet'},
            'invalid_cmd' :         {'name': 'Invalid command format'},
            'no_args' :             {'name': 'Please provide both the user name and points'},
            'already_in_game' :             {'name': 'You are already in the game!'},
            'missing_w_args' :             {'name': 'Missing arguments. Please provide both game_fact and game_winner'}
        }

    def output_list(self, output:str):
        if output in self.output:
            return self.output[output]
        else:
            return 'None'
        
    def get_output(self):
        return self.output

def setup(bot):
    bot.add_cog(Output(bot))

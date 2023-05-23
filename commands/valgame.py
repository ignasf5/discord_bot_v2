import discord
import os
import sqlite3
import asyncio
import random
import itertools

from datetime import datetime, timedelta
from discord.ext import commands
from ruamel.yaml import YAML
from .discordcolor import DiscordColors
from .valranks import ValorantRanks
from .picture_location import picture, picture_with_path
from .output import Output
from .admins_check import admin_check
from .users_check import users_checker
from .valmaps import ValMaps
from .valpoints import ValorantPoints
from .valaddrem import ValorantAddRemPoints

admins_check = admin_check('')
user_check = users_checker('')
val_maps = ValMaps('')
val_rank_pts = ValorantPoints('')
val_add_points = ValorantAddRemPoints('')

# Environment parameters
output = Output('')
colors = DiscordColors('')
valrank = ValorantRanks('')
pictures = picture('')
picture_path = picture_with_path('')
DB = os.environ['SQL']
path = os.getenv("DIR_PATH")

# Opens config 
yaml = YAML()
with open(path+"configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Game settings:
game_status = 'None'
vote_status = 'None'
team_choice = 'None'
game_mode_set = 'None'
new_game_no = ''
players_list = []
player_list_info = []
map = 'None'
game_admin = ''

class valorant_game(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.vote_options = {}  # Dictionary to store vote options and their counts
        self.voted_users = {}
        self.vote_duration = 2  # Duration of the vote in seconds
        self.vote_end_time = None  # Variable to store the end time of the vote
        self.vote_channel = None  # Channel where the vote was initiated

    def change_game_status(self, new_status):
        global game_status
        game_status = new_status
        return game_status

    @commands.command(aliases=["gs", "gamestatus", "game_status"])
    async def check_game_status(self, ctx):

        global game_status
        return await ctx.send(game_status)

    async def join_game(self, ctx):

        if game_status == 'started':
            if ctx.author in players_list:
                return await ctx.send(output.output_list('already_in_game')['name'])
            else:
                points = (users_checker.user_info(str(ctx.author))[1])
                get_rank = users_checker.user_info(str(ctx.author))[3]
                players_list.append(str(ctx.author))
                await ctx.send(f"```{str(ctx.author)} has joined the game! \n{valrank.rank_list(get_rank)['name']} ({points}) ```")

            if len(players_list) == 1:
                await ctx.send(f"``` ****** We have 10 players  ******\n {str(self.vote_duration)} sec. to choose map by !vote map```")
                await self.start_vote_game(ctx)
        else:
            await ctx.send(output.output_list('game_inprogress')['name'])

    def get_keys_from_dict(dictionary):
        return list(dictionary.keys())

    async def start_vote_game(self,ctx):
        
        global map

        if self.vote_end_time is not None and self.vote_end_time > datetime.now():
            return

        map_list = (list(val_maps.get_maps()))
        options = [item.lower() for item in map_list]

        self.vote_options = {option.lower(): 0 for option in options}
        self.vote_end_time = datetime.now() + timedelta(seconds=self.vote_duration)

        await asyncio.sleep(self.vote_duration)  # Wait for the vote duration
        result = await self.map_result(ctx)
        print('-Vote Ended-')
        map = result[2]
        await self.final_step(ctx)
        self.vote_end_time = None

    async def final_step(self,ctx):

        global game_status
        global vote_status
        global team_choice
        global players_list
        global map
        global game_status
        global new_game_no
        global game_admin
        global game_mode_set

        # Run balancing
        balance = await self.start_balancing_teams(ctx)
       
        # Return game results
        file = discord.File(picture_path.get_picture_path(str(map)+'.png', 'maps'), filename="image.png")
        em = discord.Embed(title="Match Started.", color=colors.color('white'))
        em.set_thumbnail(url="attachment://image.png")
        em.add_field(name="Admin: "+ str(game_admin), value='', inline=False)
        em.add_field(name="Map: "+ str(map).title(), value='', inline=False)

        player_a_items = list(balance['team_a'].items())[:5]  # Select first 5 items
        player_b_items = list(balance['team_b'].items())[:5]  # Select first 5 items
        em.add_field(
            name='Team_A: ({})'.format(str(balance['team_a_total'])),
            value='\n'.join(f"{i + 1}: {name} ({value})" for i, (name, value) in enumerate(player_a_items)),
            inline=False)

        em.add_field(
            name='Team_B: ({})'.format(str(balance['team_b_total'])),
            value='\n'.join(f"{i + 1}: {name} ({value})" for i, (name, value) in enumerate(player_b_items)),
            inline=False)

        em.set_footer(text="Game no: "+ str(new_game_no))
        await ctx.send(embed=em,file=file)

        # Write to DataBase
        connection = sqlite3.connect(DB)
        cursor = connection.cursor()

        #"SELECT * FROM {config['user_acc_table']}"
        cursor.execute(f"Select * FROM {config['valorant_game_history_table']}")
        result = cursor.fetchone()
        team_a_total = balance['team_a_total']
        tam_b_taotal = balance['team_b_total']

        # (str(admin_name), 'bo1', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na', 'na')
        data = (str(game_admin), str(game_mode_set), str(map), 'na', int(team_a_total), int(tam_b_taotal),
                str(player_a_items[0][0]), str(player_a_items[1][0]), str(player_a_items[2][0]), str(player_a_items[3][0]), str(player_a_items[4][0]), 
                str(player_b_items[0][0]), str(player_b_items[1][0]), str(player_b_items[2][0]), str(player_b_items[3][0]), str(player_b_items[4][0]))

        # cursor.execute(f"Select * FROM {config['admin_table']} WHERE Admin_name = ?", (str(admin_name),))
        print(data)
        try:
            cursor.execute(f"""INSERT INTO {config['valorant_game_history_table']} (NO, DATA, ADMIN, SYSTEM, MAP, WINNER,Team_a_rr, Team_b_rr, A1,A2,A3,A4,A5 ,B1,B2,B3,B4,B5) 
                            VALUES (?, DateTime('now'), ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (new_game_no, *data))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)

        await self.start_game()     

        # Clean all stuff end game
        game_status = 'None'
        self.vote_status = 'None'
        self.team_choice = 'None'
        players_list = []
        map = 'None'
        self.vote_options = {}
        self.voted_users = {}
        game_status = 'None'
        new_game_no = ''
        game_admin = ''
        print('-Game End-')
        return
    
    #Close match game
    #TODO iteration compress
    @commands.command(aliases=["w"])
    async def game_fact_set(self, ctx, game_fact=None, game_winner=None):

        admin_permissions_check = admins_check.admin_check(str(ctx.author))
        admin_val_permissions_check = admins_check.admin_check_val_per(str(ctx.author))
        
        if admin_permissions_check and admin_val_permissions_check:
           pass
        else:
            return await ctx.send(output.output_list('no_game_per')['name'])
        
        if game_fact is None or game_winner is None:
            return await ctx.send(output.output_list('missing_w_args')['name'])

        try:
            connection = sqlite3.connect(DB)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {config['valorant_game_history_table']} WHERE no={game_fact}")
            result = cursor.fetchone()
            # connection.close()
            if result[5] != 'na':
                return await ctx.send(f"Already have winner team {result[5]}")
            else:
                cursor.execute(f"UPDATE {config['valorant_game_history_table']} SET winner = ? where no=?", (game_winner, game_fact))

            #Players list
            team_a_player_list = [result[8], result[9], result[10], result[11], result[12]]
            team_b_player_list = [result[13], result[14], result[15], result[16], result[17]]

            #Sum of team RR
            team_a_rr = int(result[6])  # Convert team_a_rr to integer
            team_b_rr = int(result[7])  # Convert team_b_rr to integer

            #Getting team rank
            team_a_rank = val_rank_pts.return_val_rank(team_a_rr)
            team_b_rank = val_rank_pts.return_val_rank(team_b_rr)

            if game_winner == 'a':
                points_give = val_add_points.calculate_points(team_a_rank, team_b_rank)
                
                for team_a_user, team_b_user in zip(team_a_player_list, team_b_player_list):
                    cursor.execute(f"SELECT * FROM {config['user_table']} WHERE user_id = ?", (team_a_user,))
                    result = cursor.fetchone()
                    if result is None:
                        await ctx.send(f"User {team_a_user} - not found")
                    else:
                        old_pts = result[1]
                        new_rank_pts = int(old_pts) + points_give[0]
                        cursor.execute(f"UPDATE {config['user_table']} SET val_pts = ?, UP_DATA = DateTime('now') WHERE user_id = ?", (new_rank_pts, team_a_user))

                    cursor.execute(f"SELECT * FROM {config['user_table']} WHERE user_id = ?", (team_b_user,))
                    result = cursor.fetchone()
                    if result is None:
                        await ctx.send(f"User {team_b_user} - not found")
                    else:
                        old_pts = result[1]
                        new_rank_pts = int(old_pts) + points_give[1]
                        cursor.execute(f"UPDATE {config['user_table']} SET val_pts = ?, UP_DATA = DateTime('now') WHERE user_id = ?", (new_rank_pts, team_b_user))
                   
                    connection.commit()
            else:
                points_give = val_add_points.calculate_points(team_a_rank, team_b_rank)

                # connection = sqlite3.connect(DB)
                # cursor = connection.cursor()

                for team_b_user,team_a_user in zip(team_b_player_list, team_a_player_list):
                    cursor.execute(f"SELECT * FROM {config['user_table']} WHERE user_id = ?", (team_a_user,))
                    result = cursor.fetchone()
                    if result is None:
                        await ctx.send(f"User {team_a_user} - not found")
                    else:
                        old_pts = result[1]
                        new_rank_pts = int(old_pts) + points_give[1]
                        cursor.execute(f"UPDATE {config['user_table']} SET val_pts = ?, UP_DATA = DateTime('now') WHERE user_id = ?", (new_rank_pts, team_a_user))

                    cursor.execute(f"SELECT * FROM {config['user_table']} WHERE user_id = ?", (team_b_user,))
                    result = cursor.fetchone()
                    if result is None:
                        await ctx.send(f"User {team_b_user} - not found")
                    else:
                        old_pts = result[1]
                        new_rank_pts = int(old_pts) + points_give[0]
                        cursor.execute(f"UPDATE {config['user_table']} SET val_pts = ?, UP_DATA = DateTime('now') WHERE user_id = ?", (new_rank_pts, team_b_user))
                        connection.commit()

        except Exception as e:
            print(e)            

        await ctx.send(f"Successfully updated stats and ranks")
        connection.close()

    async def start_balancing_teams(self, ctx):
        global players_list
        global map
        # player_list_of_dict = [{user: users_checker.user_info(str(user))[1]} for user in players_list]
        
        #For testing
        player_list_of_dict = [
            {'goeswild#1': 5000},
            {'goeswild#2': 1600},
            {'goeswild#3': 1000},
            {'goeswild#4': 500},
            {'goeswild#5': 2000},
            {'goeswild#6': 453},
            {'goeswild#7': 7450},
            {'goeswild#8': 500},
            {'goeswild#9': 1800},
            {'goeswild#10': 700},
        ]

        # Sort the list of dictionaries by values in descending order
        sorted_players = sorted(player_list_of_dict, key=lambda x: list(x.values())[0], reverse=True)

        # Calculate the number of players per team
        num_players_per_team = 5

        # Generate all possible combinations of players
        combinations = itertools.combinations(sorted_players, num_players_per_team)

        # Initialize variables to store the best combination and its difference in total values
        best_combination = None
        best_difference = float('inf')

        # Iterate over all combinations and find the one with the closest total values
        for combo in combinations:
            team_a = {list(player_dict.items())[0][0]: list(player_dict.items())[0][1] for player_dict in combo}
            team_b = {list(player_dict.items())[0][0]: list(player_dict.items())[0][1] for player_dict in sorted_players if list(player_dict.items())[0][0] not in team_a}

            team_a_total = sum(team_a.values())
            team_b_total = sum(team_b.values())

            difference = abs(team_a_total - team_b_total)
            if difference < best_difference:
                best_combination = (team_a, team_b)
                best_difference = difference

        team_a, team_b = best_combination
        team_a_total = sum(team_a.values())
        team_b_total = sum(team_b.values())

        balance_result = {
            "team_a": team_a,
            "team_b": team_b,
            "team_a_total": team_a_total,
            "team_b_total": team_b_total
        }
        return balance_result

    @commands.command()
    async def vote(self, ctx, option):
        if self.vote_end_time is None or datetime.now() > self.vote_end_time:
            return await ctx.send("There is no active vote at the moment.")
        
        if str(ctx.author) in players_list:
            pass
        else: return await ctx.send(output.output_list('not_joined')['name'])
        
        option_lower = option.lower()
        if option_lower in self.vote_options:
            if ctx.author.id in self.voted_users:
                # User has already voted, remove their previous vote
                previous_option = self.voted_users[ctx.author.id]
                self.vote_options[previous_option] -= 1

            self.vote_options[option_lower] += 1
            self.voted_users[ctx.author.id] = option_lower
            await ctx.send(f"Your vote for '{option_lower}' has been recorded.")
        else:
            await ctx.send("Invalid vote option.")

    @commands.command(aliases=["pi"])
    async def map_result(self, ctx):

        if self.vote_end_time is None:
            return await ctx.send("There is no active vote at the moment.")

        sorted_options = sorted(self.vote_options.items(), key=lambda x: x[1], reverse=True)

        vote_count = 0
        max_vote_count = sorted_options[0][1]
        tied_maps = []

        result_message = "Vote Results:\n"
        for option, count in sorted_options:
            if count == 0:
                pass
            else:
                result_message += f"{option}: {count} vote(s)\n"
                vote_count += 1
                if count == max_vote_count:
                    tied_maps.append(option)

        if vote_count == 0:
            chosen_map = random.choice(list(val_maps.get_maps()))
            await ctx.send(f"```Since no map was voted, we go random: {chosen_map}```")
        elif len(tied_maps) > 1:
            chosen_map = random.choice(tied_maps)
            result_message += f"\nThe chosen map is: {chosen_map}"
        else:
            chosen_map = tied_maps[0] if tied_maps else None

        await ctx.send(f"```{result_message}```")
        return result_message, vote_count, chosen_map
       
    async def start_game(self):
        global game_status
        game_status = 'started'
        print("The game has started!") 

    @commands.command(aliases=["start"])
    async def start_val_game(self, ctx, game_mode=None):
        global game_status
        if game_status == 'started':
            return await ctx.send(output.output_list('game_inprogress')['name'])

    @commands.command(aliases=["join", "j"])
    async def join_val_game(self, ctx):

        if users_checker.user_check(str(ctx.author)) == 'None':
            return await ctx.send(output.output_list('no_reg')['name'])

        if len(players_list) >= 10:
            return await ctx.send(output.output_list('game_full')['name'])

        if game_status == 'started':
            await self.join_game(ctx)
        else:
            await ctx.send(output.output_list('no_game')['name'])

    @commands.command(aliases=["players"])
    async def show_players(self, ctx):

        if game_status == 'started':
            if len(players_list) == 0:
                return await ctx.send(output.output_list('no_players')['name'])
            else:
                try:
                    players = "\n".join([player for player in players_list])
                    return await ctx.send(f"The registered players are `({len(players_list)}/10)` :\n```{players}```")
                
                except Exception as e:
                    print(e)
        else:
            return await ctx.send(output.output_list('no_game')['name'])

    @commands.command(aliases=["remove", "rem"])
    async def remove_from_game(self, ctx):

        if game_status == 'started':
            if str(ctx.author) in players_list:
                players_list.remove(str(ctx.author))
                await ctx.send(f"{ctx.author.mention} has been removed from the game.")
            else:
                await ctx.send(output.output_list('not_joined')['name'])
        else:
            await ctx.send(output.output_list('no_game')['name'])

    async def start_game(self):
        global game_status
        game_status = 'started'
        print("The game has started!") 

    async def start_game(self):
        global game_status
        game_status = 'started'
        print("The game has started!") 

    @commands.command(aliases=["start"])
    async def start_val_game(self, ctx, game_mode=None):
        
        global game_status
        global new_game_no
        global game_admin
        global game_mode_set

        game_admin=str(ctx.author)

        if game_status == 'started':
            return await ctx.send(output.output_list('game_inprogress')['name'])

        admin_permissions_check = admins_check.admin_check(str(ctx.author))
        admin_val_permissions_check = admins_check.admin_check_val_per(str(ctx.author))

        # Check admin permissions
        if admin_permissions_check and admin_val_permissions_check:
            # result = admins_check.admin_check(str(ctx.author))
            pass
        else:
            return await ctx.send(output.output_list('no_game_per')['name'])

        if game_mode is None:
            return await ctx.send(output.output_list('no_game_mode')['name'])
        if game_mode == "bo1" or game_mode == "bo3":
            game_mode_set = game_mode
            pass
        else:
            return await ctx.send(output.output_list('wrong_game_mode')['name'])


        connection = sqlite3.connect(DB)
        cursor = connection.cursor()
        #"SELECT * FROM {config['user_acc_table']}"
        cursor.execute(f"Select * FROM {config['valorant_game_history_table']} ORDER BY no DESC LIMIT 1")
        result = cursor.fetchone()

        if result is not None:
            new_game_no = int(result[0]) + 1
            print(ctx.author)
            await ctx.send('```Admin: {}\nNo: {} \nGame: {} \n\nJump in - !join to take a place```'.format(str(ctx.author), new_game_no, output.output_list("game_started")["name"]))#, game_mode.upper()))
        else:
            new_game_no = 1
            await ctx.send('```Admin: {}\nNo: {} \nGame: {} \n\nJump in - !join to take a place```'.format(str(ctx.author), new_game_no, output.output_list("game_started")["name"]))#, game_mode.upper()))
        
        await self.start_game()

    @commands.command(aliases=["stop"])
    async def stop_val_game(self, ctx):
        global game_status
        if game_status == 'None':
            return await ctx.send(output.output_list('no_game')['name'])

        admin_permissions_check = admins_check.admin_check(str(ctx.author))
        admin_val_permissions_check = admins_check.admin_check_val_per(str(ctx.author))

        # Check admin permissions
        if admin_permissions_check and admin_val_permissions_check:
            pass
        else:
            return await ctx.send(output.output_list('no_game_per')['name'])

        game_status = 'None'
        print('The game has been stopped')
        await ctx.send(output.output_list('game_stop')['name'])

    @commands.command(aliases=["cp"])
    async def change_points(self, ctx, *, user_name_and_points=None):
        if user_name_and_points is None:
            return await ctx.send(output.output_list('no_args')['name'])

        args = user_name_and_points.split()
        if len(args) < 2:
            return await ctx.send(output.output_list('invalid_cmd')['name'])

        user_name = args[0]
        user_points = args[1]

        try:
            user_points = int(user_points)  # Convert user_points to an integer
        except ValueError:
            return await ctx.send("Invalid points. Please provide a valid integer value.")  
        
        admin_permissions_check = admins_check.admin_check(str(ctx.author))
        admin_val_permissions_check = admins_check.check_master_admin_per(str(ctx.author))

        # Check admin permissions
        if admin_permissions_check and admin_val_permissions_check:
            if users_checker.user_check(str(user_name)) == 'None':
                return await ctx.send(output.output_list('no_user')['name'])
        else:
            return await ctx.send(output.output_list('no_permissions')['name'])

        try: 
            new_rank = valrank.get_closest_rank(user_points)
            content_insert = (int(user_points),str(new_rank),str(user_name))

            connection = sqlite3.connect(DB)
            cursor = connection.cursor()
            cursor.execute(f"""Update {config['user_table']} SET val_pts = ?, rank = ?, UP_DATA = DateTime('now') where user_id = ?""", (content_insert))

            connection.commit()
            cursor.close()
            connection.close()
            return await ctx.send("```"+ (output.output_list('update_rank')['name']) +"```")
        except:
            return await ctx.channel.send(output.output_list('no_db')['name'])
        
def setup(client):
    client.add_cog(valorant_game(client))

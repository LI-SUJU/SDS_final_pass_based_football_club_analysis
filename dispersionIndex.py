
import json

from visualization.passing_network import draw_pitch, draw_dispersion_dot
import os
import matplotlib.pyplot as plt

from utils import read_json
# matches_path = "data/eventing/matches/9/281.json"
# team_id = 904
# team_name = "Bayer Leverkusen"
# match_ids = []

# with open(matches_path, 'r') as file:
#     match_data = json.load(file)
#     for match in match_data:
#         home_team_id = match["home_team"]["home_team_id"]
#         away_team_id = match["away_team"]["away_team_id"]
#         if home_team_id == team_id or away_team_id == team_id:
#             match_ids.append(match["match_id"])
# print the length of the match_ids
# print(len(match_ids))
def draw_plot_for_1_match(match_id, team_name, ax):
    from pandas import json_normalize
    from utils import read_json

    lineups_path = "data/eventing/lineups/{0}.json"
    events_path = "data/eventing/events/{0}.json"

    lineups = read_json(lineups_path.format(match_id))
    names_dict = {player["player_name"]: player["player_nickname"]
                  for team in lineups for player in team["lineup"]}

    events = read_json(events_path.format(match_id))
    df_events = json_normalize(events, sep="_").assign(match_id=match_id)

    if "foul_committed_card_name" in df_events.columns:
        first_red_card_minute = df_events[df_events.foul_committed_card_name.isin(["Second Yellow", "Red Card"])].minute.min()
    else:
        first_red_card_minute = df_events.minute.max()
    first_substitution_minute = df_events[df_events.type_name == "Substitution"].minute.min()
    max_minute = df_events.minute.max()

    num_minutes = min(first_substitution_minute, first_red_card_minute, max_minute)
    # num_minutes

    plot_name = "statsbomb_match{0}_{1}".format(match_id, team_name)

    opponent_team = [x for x in df_events.team_name.unique() if x != team_name][0]
    plot_title ="Dispersion&bias of {0} in a match against {1} (season 2015/2016)".format(team_name, opponent_team)

    plot_legend = "Green dot: center of pitch\nRed dot: players' aggregated positions\nBlue dot: center of squad"

    def _statsbomb_to_point(location, max_width=120, max_height=80):
        '''
        Convert a point's coordinates from a StatsBomb's range to 0-1 range.
        '''
        return location[0] / max_width, 1-(location[1] / max_height)

    df_passes = df_events[(df_events.type_name == "Pass") &
                          (df_events.pass_outcome_name.isna()) &
                          (df_events.team_name == team_name) &
                          (df_events.minute < num_minutes)].copy()

    # If available, use player's nickname instead of full name to optimize space in plot
    df_passes["pass_recipient_name"] = df_passes.pass_recipient_name.apply(lambda x: names_dict[x] if names_dict[x] else x)
    df_passes["player_name"] = df_passes.player_name.apply(lambda x: names_dict[x] if names_dict[x] else x)


    df_passes["origin_pos_x"] = df_passes.location.apply(lambda x: _statsbomb_to_point(x)[0])
    df_passes["origin_pos_y"] = df_passes.location.apply(lambda x: _statsbomb_to_point(x)[1])
    player_position = df_passes.groupby("player_name").agg({"origin_pos_x": "median", "origin_pos_y": "median"})

    player_pass_count = df_passes.groupby("player_name").size().to_frame("num_passes")
    player_pass_value = df_passes.groupby("player_name").size().to_frame("pass_value")

    print(player_pass_count.head(10))

    df_passes["pair_key"] = df_passes.apply(lambda x: "_".join(sorted([str(x["player_name"]), str(x["pass_recipient_name"])])), axis=1)
    # df_passes["pair_key"] = df_passes.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
    pair_pass_count = df_passes.groupby("pair_key").size().to_frame("num_passes")
    pair_pass_value = df_passes.groupby("pair_key").size().to_frame("pass_value")

    # print(pair_pass_count.head(10))



    # ax.patch.set_alpha(0.2)
    # ax = draw_pitch()
    ax, dispersionIndex, left_right_index, forward_backward_index, player_x_mean, player_y_mean = draw_dispersion_dot(ax, player_position)
    # set transparency of the whole plot
    # ax.patch.set_alpha(0.2)
    # plt.savefig("demo/{0}.png".format(plot_name))
    # plt.savefig("demo/1.png")
    return ax, dispersionIndex, left_right_index, forward_backward_index, player_x_mean, player_y_mean

# ax = draw_pitch()
# for match_id in match_ids:
#     ax = draw_plot_for_1_match(match_id, team_name, ax)
# plt.show()

def draw_plot_for_1_club(team_id, team_name, matches_path):
    match_ids = []
    dispersionIndexs = []
    left_right_indexs = []
    forward_backward_indexs = []
    player_x_means = []
    player_y_means = []
    with open(matches_path, 'r') as file:
        match_data = json.load(file)
        for match in match_data:
            home_team_id = match["home_team"]["home_team_id"]
            away_team_id = match["away_team"]["away_team_id"]
            if home_team_id == team_id or away_team_id == team_id:
                match_ids.append(match["match_id"])
    
    plot_title ="Dispersion&bias of {0} (season 2015/2016)".format(team_name)

    plot_legend = "Green dot: center of pitch\nRed dot: players' aggregated positions\nBlue dot: center of squad in one match\nSolid blue dot: center of squad in all matches"
    ax = draw_pitch(title=plot_title, legend=plot_legend)
    for match_id in match_ids:
        ax, dispersionIndex, left_right_index, forward_backward_index, player_x_mean, player_y_mean = draw_plot_for_1_match(match_id, team_name, ax)
        dispersionIndexs.append(dispersionIndex)
        left_right_indexs.append(left_right_index)
        forward_backward_indexs.append(forward_backward_index)
        player_x_means.append(player_x_mean)
        player_y_means.append(player_y_mean)
    average_dispersionIndex = sum(dispersionIndexs) / len(dispersionIndexs)
    average_left_right_index = sum(left_right_indexs) / len(left_right_indexs)
    average_forward_backward_index = sum(forward_backward_indexs) / len(forward_backward_indexs)
    average_player_x_mean = sum(player_x_means) / len(player_x_means)
    average_player_y_mean = sum(player_y_means) / len(player_y_means)
    config = read_json("visualization/plot_config.json")
    height = float(config["height"])
    width = float(config["width"])
    ax.annotate("Dispersion index: " + str(average_dispersionIndex), xy=(0.99*width, 0.02*height),
            ha="right", va="bottom", zorder=7, fontsize=10, color=config["lines_color"])
    ax.annotate("Left-right index: " + str(average_left_right_index), xy=(0.99*width, 0.04*height),
            ha="right", va="bottom", zorder=7, fontsize=10, color=config["lines_color"])
    ax.annotate("Forward-backward index: " + str(average_forward_backward_index), xy=(0.99*width, 0.06*height),
            ha="right", va="bottom", zorder=7, fontsize=10, color=config["lines_color"])
    ax.plot(average_player_x_mean, average_player_y_mean, 'o', color='blue', markersize=10, zorder=5, alpha=1)
    print("length of match_ids", len(match_ids))
    plt.savefig("plots/dispersionIndex_France(2015-2016)/{0}.png".format(team_name))

# draw_plot_for_1_match(3895302, "Bayer Leverkusen", draw_pitch())
# plt.savefig("./plots/dispersionInOneMatch.png")
team_ids = []
team_names = {}
path = "data/eventing/matches/11/27.json"
with open(path, 'r') as file:
    match_data = json.load(file)
    for match in match_data:
        home_team_id = match["home_team"]["home_team_id"]
        away_team_id = match["away_team"]["away_team_id"]
        if home_team_id not in team_ids:
            team_ids.append(home_team_id)
            # change the id into a string
            home_team_id = str(home_team_id)
            team_names[home_team_id] = match["home_team"]["home_team_name"]
        if away_team_id not in team_ids:
            team_ids.append(away_team_id)
            # change the id into a string
            away_team_id = str(away_team_id)
            team_names[away_team_id] = match["away_team"]["away_team_name"]
for team_id in team_ids:
    draw_plot_for_1_club(team_id, team_names[str(team_id)], path)
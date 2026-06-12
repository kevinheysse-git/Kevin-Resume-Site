from django.shortcuts import render
from django.http import JsonResponse
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, shotchartdetail
import json
import time

# Dictionary to map abbreviations to full franchise names
NBA_TEAMS = {
    'ATL': 'Atlanta Hawks', 'BKN': 'Brooklyn Nets', 'BOS': 'Boston Celtics',
    'CHA': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers',
    'LAC': 'LA Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans', 'NYK': 'New York Knicks', 'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHX': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'
}

def player_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        all_players = players.get_players()
        results = [p for p in all_players if query.lower() in p['full_name'].lower()]

    return render(request, 'nba_visualizer/search.html', {
        'players': results,
        'query': query,
    })

def player_stats(request, player_id):
    all_players = players.get_players()
    player = next((p for p in all_players if p['id'] == player_id), None)

    stat_choice = request.GET.get('stat', 'PTS')
    if stat_choice not in ['PTS', 'AST', 'REB', 'STL', 'BLK']:
        stat_choice = 'PTS'

    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season='2025-26'
    ).get_data_frames()[0]

    game_log = game_log.iloc[::-1].reset_index(drop=True)

    labels = game_log['GAME_DATE'].tolist()
    game_ids = game_log['Game_ID'].tolist()
    
    wl_list = game_log['WL'].tolist()
    location_list = ['Away' if '@' in m else 'Home' for m in game_log['MATCHUP'].tolist()]

    matchup_list = []
    for raw_matchup in game_log['MATCHUP'].tolist():
        is_away = "@" in raw_matchup
        delimiter = "@" if is_away else "vs."
        opp_abbrev = raw_matchup.split(delimiter)[-1].strip()
        opp_name = NBA_TEAMS.get(opp_abbrev, opp_abbrev)
        matchup_list.append(f"at {opp_name}" if is_away else f"vs {opp_name}")

    metric_mapping = {
        'PTS': 'PTS',
        'AST': 'AST',
        'REB': 'REB',
        'STL': 'STL',
        'BLK': 'BLK'
    }

    master_stats_bundle = {}
    for tab_name, col_name in metric_mapping.items():
        raw_vals = game_log[col_name].tolist() if col_name in game_log.columns else []
        master_stats_bundle[tab_name] = {
            'values': raw_vals,
            'avg': round(sum(raw_vals) / len(raw_vals), 1) if raw_vals else 0,
            'high': max(raw_vals) if raw_vals else 0,
            'low': min(raw_vals) if raw_vals else 0
        }

    try:
        season_fg_pct = round((game_log['FGM'].sum() / game_log['FGA'].sum()) * 100, 1) if game_log['FGA'].sum() > 0 else 0
        season_3p_pct = round((game_log['FG3M'].sum() / game_log['FG3A'].sum()) * 100, 1) if game_log['FG3A'].sum() > 0 else 0
        season_ft_pct = round((game_log['FTM'].sum() / game_log['FTA'].sum()) * 100, 1) if game_log['FTA'].sum() > 0 else 0
    except KeyError:
        season_fg_pct, season_3p_pct, season_ft_pct = 0, 0, 0

    return render(request, 'nba_visualizer/stats.html', {
        'player': player,
        'labels': json.dumps(labels),
        'game_ids': json.dumps(game_ids),
        'matchups': json.dumps(matchup_list),
        'wl_list': json.dumps(wl_list),
        'location_list': json.dumps(location_list),
        'master_stats_bundle': json.dumps(master_stats_bundle),
        'initial_stat': stat_choice,
        'season_fg_pct': season_fg_pct,
        'season_3p_pct': season_3p_pct,
        'season_ft_pct': season_ft_pct,
    })

def shot_chart_data(request, player_id, game_id):
    try:
        time.sleep(0.5)
        
        shot_chart = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            game_id_nullable=game_id,
            season_nullable='2025-26',
            context_measure_simple='FGA'
        )
        shot_data = shot_chart.get_data_frames()[0]
        shots = shot_data[['LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG', 'ACTION_TYPE', 'SHOT_DISTANCE']].to_dict('records')

        game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season='2025-26'
        ).get_data_frames()[0]
        
        matched_game = game_log[game_log['Game_ID'] == str(game_id)]
        
        matchup_string = ""
        if not matched_game.empty:
            raw_matchup = matched_game.iloc[0]['MATCHUP'] 
            
            is_away = "@" in raw_matchup
            delimiter = "@" if is_away else "vs."
            
            opp_abbrev = raw_matchup.split(delimiter)[-1].strip()
            
            opponent_full_name = NBA_TEAMS.get(opp_abbrev, opp_abbrev)
            
            if is_away:
                matchup_string = f"at {opponent_full_name}"
            else:
                matchup_string = f"vs {opponent_full_name}"

        return JsonResponse({
            'shots': shots,
            'matchup': matchup_string
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
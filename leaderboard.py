import json

# Load leaderboard data from file
def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as lb:
            leaderboard_data = json.load(lb)
    except FileNotFoundError:
        leaderboard_data = {}
    return leaderboard_data

# Save leaderboard data to file
def save_leaderboard(leaderboard_data):
    with open('leaderboard.json', 'w') as lb:
        json.dump(leaderboard_data, lb)

# Update leaderboard data with new score
def update_leaderboard(username, score):
    leaderboard_data = load_leaderboard()
    if username in leaderboard_data:
        if score > leaderboard_data[username]:
            leaderboard_data[username] = score
    else:
        leaderboard_data[username] = score
    save_leaderboard(leaderboard_data)

# Get top N players from leaderboard
def get_top_players():
    
    return top_players

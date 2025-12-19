'''
Created on September 18, 2025

@author: aiden
'''
# atBatDataFormatter.py
TERMINAL_RESULTS = {"BB", "SO", "O", "HBP", "H"}  # At-bat ending results

# Mapping for location input formatting
LOCATION_MAP = {
    "hi-in": "Hi-In",
    "hi-out": "Hi-Out",
    "mi-in": "Mi-In",
    "mi-mi": "Mi-Mi",
    "mi-out": "Mi-Out",
    "lo-in": "Lo-In",
    "lo-out": "Lo-Out"
}

def format_location(user_input):
    key = user_input.strip().lower()
    return LOCATION_MAP.get(key, user_input)  # Return formatted or raw if unknown

def format_count(user_input):
    # Convert '01' → '0-1', '12' → '1-2'
    if len(user_input) == 2 and user_input.isdigit():
        return f"{user_input[0]}-{user_input[1]}"
    return user_input

def get_pitcher_info():
    print("\n=== Enter Pitcher Info ===")
    name = input("Pitcher Name: ")
    team = input("Pitcher Team: ")
    return {"name": name, "team": team, "pitches": []}

def get_batter_info():
    print("\n=== Enter Batter Info ===")
    name = input("Batter Name: ")
    team = input("Batter Team: ")
    lineup_spot = input("Batter Spot in Lineup (1-9): ")
    avg_vs_pitcher = input("Batter's AVG vs Current Pitcher (ex: 2-6): ")
    inning = input("Inning: ")  # Ask inning once per batter
    return {
        "name": name,
        "team": team,
        "lineup_spot": lineup_spot,
        "avg_vs_pitcher": avg_vs_pitcher,
        "inning": inning,
        "pitches": []
    }

def log_pitch(batter_inning):
    print("\n--- Log Pitch ---")
    pitch_type = input("Pitch Type (2FB, 4FB, CB, CT, SL, SNK, SPL, KB, CH, SW, SCRW): ")
    location_input = input("Location (Hi-In, Hi-Out, Mi-Mi, etc): ")
    location = format_location(location_input)
    result = input("Result (S, B, O, BB, HBP, etc): ")
    speed = input("Velocity (mph): ")
    count_input = input("Count (e.g., 01, 12): ")
    count = format_count(count_input)
    return {
        "pitch_type": pitch_type,
        "location": location,
        "result": result,
        "speed": speed,
        "count": count,
        "inning": batter_inning  # Use inning from batter info
    }

def main():
    print("=== Pitch Tracking Logger ===")

    # Initial pitcher
    current_pitcher = get_pitcher_info()
    pitchers_data = {current_pitcher["name"]: current_pitcher}

    while True:
        # New batter
        batter = get_batter_info()
        print(f"\nLogging pitches for {batter['name']} vs {current_pitcher['name']} in Inning {batter['inning']}...\n")

        while True:
            pitch = log_pitch(batter['inning'])
            batter["pitches"].append(pitch)
            current_pitcher["pitches"].append(pitch)

            if pitch["result"] in TERMINAL_RESULTS:
                batter["avg_vs_pitcher"] = input(
                    f"Update {batter['name']}'s AVG vs {current_pitcher['name']} after this AB: "
                )
                break  # End of at-bat

        # Ask if pitcher changed for next inning
        change_pitcher = input("\nNext batter/inning. Is it the same pitcher? (y/n): ").lower()
        if change_pitcher != 'y':
            # Save current pitcher data
            pitchers_data[current_pitcher["name"]] = current_pitcher
            # Get new pitcher info
            current_pitcher = get_pitcher_info()
            if current_pitcher["name"] in pitchers_data:
                current_pitcher["pitches"] = pitchers_data[current_pitcher["name"]]["pitches"]
            pitchers_data[current_pitcher["name"]] = current_pitcher

        continue_logging = input("Log another at-bat? (y/n): ").lower()
        if continue_logging != 'y':
            break

    # --- SESSION SUMMARY ---
    print("\n=== Session Summary ===\n")
    for pname, pdata in pitchers_data.items():
        print(f"Pitcher: {pname} ({pdata['team']}) | Total Pitches: {len(pdata['pitches'])}")
        for i, p in enumerate(pdata['pitches'], start=1):
            print(f"  Pitch {i}: {p['pitch_type']} | {p['location']} | {p['result']} | {p['speed']} mph | Count {p['count']} | Inning {p['inning']}")
        print()

    print("Done! (In real-world usage, this data would be saved to a file.)")

if __name__ == "__main__":
    main()

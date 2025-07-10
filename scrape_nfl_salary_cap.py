import pandas as pd

# List of years to scrape
years = list(range(2015, 2025))  # Adjust as needed

# List of NFL teams formatted for the Spotrac URL structure
teams = [
    "arizona-cardinals", "atlanta-falcons", "baltimore-ravens", "buffalo-bills", "carolina-panthers",
    "chicago-bears", "cincinnati-bengals", "cleveland-browns", "dallas-cowboys", "denver-broncos",
    "detroit-lions", "green-bay-packers", "houston-texans", "indianapolis-colts", "jacksonville-jaguars",
    "kansas-city-chiefs", "las-vegas-raiders", "los-angeles-chargers", "los-angeles-rams", "miami-dolphins",
    "minnesota-vikings", "new-england-patriots", "new-orleans-saints", "new-york-giants", "new-york-jets",
    "philadelphia-eagles", "pittsburgh-steelers", "san-francisco-49ers", "seattle-seahawks",
    "tampa-bay-buccaneers", "tennessee-titans", "washington-commanders"
]

# Base URL format
base_url = "https://www.spotrac.com/nfl/{}/cap/_/year/{}/sort/cap_total"

# Empty list to store all DataFrames
all_data = []

# Loop through each team and year
for team in teams:
    team_name = team.replace("-", " ").title()  # Convert team format for readability
    for year in years:
        url = base_url.format(team, year)  # Construct the full URL
        print(f"Scraping data for {team_name} ({year})...")

        try:
            # Read tables from the webpage
            tables = pd.read_html(url)

            if not tables:  # If no tables were found, skip this iteration
                print(f"No tables found for {team_name} ({year}), skipping...")
                continue

            # Get the reference column count from the first table
            reference_columns = tables[0].columns

            # Process only tables with the same number of columns
            valid_tables = [df for df in tables if df.shape[1] == len(reference_columns)]

            # Keep only tables 1-3 if available
            selected_tables = valid_tables[:3]  # Ensures it only includes up to three tables

            for df in selected_tables:
                df.insert(0, "Year", year)
                df.insert(0, "Team", team_name)
                all_data.append(df)

        except Exception as e:
            print(f"Failed to scrape data for {team_name} ({year}): {e}")

# Combine all DataFrames into one
df_combined = pd.concat(all_data, ignore_index=True)

# Save to CSV
save_path = r"C:\Users\mineg\OneDrive\Desktop\SalaryCapData\all_teams_all_years.csv"
df_combined.to_csv(save_path, index=False)

# Display success message
print(f"CSV file saved as '{save_path}'")



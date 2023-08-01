import streamlit as st
import pandas as pd

def generate_odds_dataframe(increment=0.01):
    min_odds = 1.01
    max_odds = 1001.0

    decimal_odds_list = []
    probabilities_list = []

    current_odds = min_odds
    while current_odds <= max_odds:
        decimal_odds_list.append(round(current_odds, 2))
        probability = round(1 / current_odds, 4)  # Calculate the probability with four decimal places
        probabilities_list.append(probability)
        current_odds += increment

    data = {
        'decimal_odds': decimal_odds_list,
        'probability': probabilities_list
    }

    return pd.DataFrame(data)

# Create the Streamlit app
def main():
    st.title("Sports Betting Profit Calculator")

    # Taking inputs for stake and odds from the sportsbook
    sportsbook_stake = st.number_input("Enter the stake at the sportsbook:", value=100.0, step=0.01)
    sportsbook_odds = st.number_input("Enter the odds taken at the sportsbook:", value=2.0, step=0.01)

    # Adding approximately 13% to the sportsbook odds to find the target lay probability
    target_probability = round(1 / sportsbook_odds + 0.13, 4)

    # Generate the list of odds and probabilities
    odds_dataframe = generate_odds_dataframe()

    matched_odds_row = odds_dataframe[odds_dataframe['probability'] <= target_probability].iloc[0]
    matched_lay_odds = matched_odds_row['decimal_odds']

    lay_potential_winnings = sportsbook_stake + (sportsbook_stake * 0.05)

    # Calculate the potential returns
    sportsbook_win_return = sportsbook_stake * sportsbook_odds
    lay_win_return = lay_potential_winnings * matched_lay_odds
    lay_win_return_with_commission = lay_win_return - (lay_win_return * 0.02)

    # Calculate the overall stake
    overall_stake = round(sportsbook_stake + ((lay_potential_winnings * matched_lay_odds) - lay_potential_winnings), 0)

    # Calculate the margins
    margin_if_sportsbook_wins = round(1 - (overall_stake / sportsbook_win_return), 4)
    margin_if_lay_wins = round(1 - (overall_stake / lay_win_return_with_commission), 4)

    st.write(f"The lay odds that result in at least 1% profit if the lay wins and sportsbook loses: {matched_lay_odds:.2f}")
    st.write(f"Lay stake required to achieve the profit: {abs(overall_stake - sportsbook_stake):.2f}")
    st.write(f"Overall Stake: {overall_stake:.4f}")
    st.write(f"Return if Sportsbook wins: {sportsbook_win_return - overall_stake :.4f}")
    st.write(f"Margin if Sportsbook wins: {margin_if_sportsbook_wins:.4f}%")
    st.write(f"Return if Lay wins: {lay_win_return_with_commission - overall_stake :.4f}")
    st.write(f"Margin if Lay wins: {margin_if_lay_wins:.4f}%")

if __name__ == "__main__":
    main()

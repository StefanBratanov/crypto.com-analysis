import warnings
warnings.filterwarnings("ignore")

import pandas as pd

card_transactions_file = "card_transactions_record_20220224_162315.csv"

card_currencies = ['GBP', 'EUR']
native_currency = "GBP"

print("Native Currency: {}\n".format(native_currency))

static_eur_gbp_exchange_rate = 0.84


def get_years_and_months(days):
    years = int(days / 365.0)
    left_days = days % 365
    months = int(left_days / 30.5)
    return years, months


def get_deposit_descriptions():
    length = len(card_currencies)
    if length == 1:
        currency = card_currencies[0]
        return ['{} -> {}'.format(currency, currency), '{} Deposit'.format(currency)]
    elif length == 2:
        c1 = card_currencies[0]
        c2 = card_currencies[1]
        return ['{} -> {}'.format(c1, c1), '{} -> {}'.format(c2, c1), '{} -> {}'.format(c1, c2),
                '{} -> {}'.format(c2, c2), '{} Deposit'.format(c1), '{} Deposit'.format(c2)]
    else:
        raise Exception(
            "{} card currencies not supported".format(length))


card_txs = pd.read_csv(card_transactions_file, parse_dates=['Timestamp (UTC)'])

earliest_txn_time = card_txs['Timestamp (UTC)'].min()
latest_txn_time = card_txs['Timestamp (UTC)'].max()

date_format = "%d %b %Y"

print("From {} to {}".format(earliest_txn_time.strftime(date_format),
                             latest_txn_time.strftime(date_format)))

total_days = (latest_txn_time - earliest_txn_time).days
years_and_months = get_years_and_months(total_days)

print("{} year(s) and {} month(s)\n".format(
    years_and_months[0], years_and_months[1]))

gbp_deposits = card_txs[card_txs['Transaction Description'].isin(
    get_deposit_descriptions())]

gbp_deposits.loc[gbp_deposits['Native Currency'] !=
                 native_currency, 'Native Amount'] *= static_eur_gbp_exchange_rate

total_deposits = gbp_deposits['Native Amount'].sum()

print("Total deposits to card: " + str(total_deposits))

other_card_txs = card_txs[~card_txs['Transaction Description'].isin(
    get_deposit_descriptions())]

other_card_txs['Transaction Description'] = other_card_txs['Transaction Description'].str.replace('*', ' ', regex=False)
total_spent = abs(other_card_txs['Native Amount'].sum())

print("Total spent on card: " + str(total_spent))

most_common_txns = other_card_txs['Transaction Description'].value_counts()

print("\n5 Most common transactions\n")

print(most_common_txns.head(5).to_string(index=True))

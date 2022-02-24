import pandas as pd

card_transactions_file = "card_transactions_record_20220224_162315.csv"

card_currencies = ['GBP', 'EUR']
native_currency = "GBP"

static_gbp_eur_exchange_rate = 0.84


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


card_txs = pd.read_csv(card_transactions_file)

gbp_deposits = card_txs[card_txs['Transaction Description'].isin(
    get_deposit_descriptions())]

gbp_deposits.loc[gbp_deposits['Native Currency'] !=
                 native_currency, 'Native Amount'] *= static_gbp_eur_exchange_rate

total_deposits = gbp_deposits['Native Amount'].sum()

print("Total Deposit to card: " + str(total_deposits))

other_card_txs = card_txs[~card_txs['Transaction Description'].isin(
    get_deposit_descriptions())]

total_spent = abs(other_card_txs['Native Amount'].sum())

print("Total Spent on card: " + str(total_spent))

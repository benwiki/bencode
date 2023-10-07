def lines(file_path):
    with open(file_path, "r") as file:
        for line in file:
            yield line


def parse_csv(lines):
    for line in lines:
        yield line.strip().split(',')


def update_balance(balance, csv_path):
    # for cells in parse_csv(lines(csv_path)):
    #    try:
    #        transaction_amount = float(cells[1])
    #    except ValueError:
    #        continue
    #    balance += transaction_amount
    for cells in parse_csv(lines(csv_path)):
        transaction_amount = cells[2]
        try:
            transaction_amount = float(transaction_amount)
        except ValueError:
            continue
        balance += transaction_amount
    return balance


if __name__ == "__main__":
    for line in lines("umsatz.csv"):
        print(line)
    f = list(parse_csv(["Datum,Verwendungszweck,Betrag", "30.12.2020,Bafoeg-Foerdergeld,+514.00"]))
    print(f)
    print(update_balance(100.00, "umsatz.csv"))
import backtest, csv, os

commission_val = 0.04
portfolio = 40
stake_val = 1
quantity = 0.01
leverage = 20
start = "2020-01-01"
end = "2020-11-01"
strategies = ['RSISTOCH']
periodRange = range(14, 14)
plot = False

for strategy in strategies:
    for data in os.listdir("./data"):
        data_path = 'data/' + data
        sep = data_path[5:-4].split(sep='_')  # ignore name file 'data/' and '.csv'
        # sep[0] = pair; sep[1] = year start; sep[2] = year end; sep[3] = timeframe

        print('\n ------------', data_path, '\n')

        data_name = 'result/{}_{}_{}_{}_{}.csv'.format(strategy, sep[0], start.replace('_', '-'), end.replace('_', '-'), sep[3])
        csv_file = open(data_name, 'w', newline='')
        result_writer = csv.writer(csv_file, delimiter=',')

        # initié le header du fichier dans résultat
        result_writer.writerow(
            ['Pair', 'TimeFrame', 'Start', 'End', 'Strategy', 'Period', 'Leverage', 'Final value', '%', 'Total win', 'Total loss',
             'SQN'])
        for period in periodRange:
            end_val, total_win, total_loss, pnl_net, sqn = backtest.runStrategy(data_path, start, end, period, leverage, strategy,
                                                                                commission_val, portfolio, stake_val,
                                                                                quantity, plot)
            profit = (pnl_net / portfolio) * 100

            # view the data in the console while processing
            print('data processed: %s, %s (Period %d), %s --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' % (
            data_path[5:], strategy, period, leverage, end_val, total_win, total_loss, sqn))

            result_writer.writerow(
                [sep[0], sep[3], start, end, strategy, period, leverage, round(end_val, 3), round(profit, 3), total_win,
                 total_loss, sqn])

        csv_file.close()

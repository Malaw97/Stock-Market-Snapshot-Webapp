import matplotlib.pyplot as plt
import pull_iex as iex
import time


def choose_iex(list_tickers):
    pull_iex = (iex.main(list_tickers))
    return pull_iex


def choose(list_tickers, source):
    '''
    Data source sorter
    '''
    hasht, valid_vals = {}, []
    for i in range(len(source)):
        if source[i] in hasht.keys():
            hasht[source[i]].append(list_tickers[i])
        else:
            hasht[source[i]] = [list_tickers[i]]
    dict_keys = list(hasht.keys())
    data = []
    for key_num in range(len(dict_keys)):
        if dict_keys[key_num] == 'iex':
            data.append(choose_iex(hasht['iex']))
            valid_vals.append(hasht['iex'])
        elif dict_keys[key_num] == 'some other thing':
            valid_vals.append(hasht['iex'])
        else:
            print(str(dict_keys[key_num]) + ' Is Coming Soon')

    valid_vals2 = []
    for i in valid_vals:
        # Flatten list of lists
        for r in i:
            valid_vals2.append(r)
    return valid_vals2, data


def visual_pipeline(list_tickers, source):
    data = choose(list_tickers, source)
    fig, ax = plt.subplots()
    data_labels = data[0]
    data_points = data[1][0]
    for index in range(len(data_points)):
        ax.plot((data_points[index]['minute']), (data_points[index]['volume']),
                label=data_labels[index])
    ax.set(xlabel='Time (m)', ylabel='Volume', title='Volume over Time')
    ax.grid()
    plt.legend()
    plt.show()


def main():
    t1 = time.time()

    #visual_pipeline(['airi', 'amd', 'ba', 'bmo', 'bns', 'nclh', 'pgm', 'ry', 'wmt', 'spy'], ['iex', 'iex', 'iex', '44', 'iex', 'iex', 'iex', 'iex', 'iex', 'iex'])
    visual_pipeline(['tsla', 'twtr', 'spy'], ['iex', 'iex', 'iex'])

    print('Task took %s seconds' % (time.time() - t1))


if __name__ == "__main__":
    main()

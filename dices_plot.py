import matplotlib.pyplot as plt
import numpy as np


def dices(number_of_dices: int) -> tuple:
    ''' returns a tuple with two lists. The first list contain all the possible sums of the dices choosen. The other list contains the probability for each unique number'''
    dice1 = [y for y in range(1, 7)]
    dice1 = np.array(dice1)
    outcome = dice1

    for _ in range(number_of_dices-1):
        outcome = np.add.outer(dice1, outcome)

    unique_values = np.unique(outcome)
    flat_array = outcome.flatten()
    counts_dice = np.bincount(flat_array-number_of_dices)

    freq = [round(c/len(flat_array), 3) for c in counts_dice]

    return unique_values, freq


def barplot(plot_name='', *args, percent=False):
    '''Plots the probability for each sum of n dices. set percent=True to display the probability in %'''
    n_plots = len(args)
    rows = (n_plots + 1) // 2
    cols = 2
    fig, axs = plt.subplots(rows, cols, figsize=(12, 6))

    fig.suptitle(plot_name)
    for index, ax in enumerate(axs.flat):
        if len(args) < len(axs.flat):
            if index == len(args):
                break
        if percent:
            test = [num*100 for num in args[index][1]]
            y_lable = 'Probability (%)'
        else:
            test = args[index][1]
            y_lable = 'Probability'
        ax.bar(args[index][0], test)
        ax.set_xticks(args[index][0])
        ax.set_ylabel(y_lable)
        ax.set_xlabel('Sum of dices')
        ax.grid()

    for i in range(n_plots, rows * cols):
        fig.delaxes(axs.flatten()[i])

    plt.tight_layout()
    plt.show()

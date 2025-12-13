import matplotlib.pyplot as plt

from utils import (generate_network, Timer, Solver)
from tsp_plot import (plot_network, plot_tour, plot_solutions, plot_coverage,
                      plot_queue_size,
                      plot_solution_evolution,
                      plot_edge_probability)
from tsp_run import format_text_summary, format_plot_summary


def main(n, find_tour: Solver, sec_find_tour: Solver, timeout=60, **kwargs):
    # Generate network
    print(f'Generating network of size {n} with args: {kwargs}')
    locations, edges = generate_network(n, **kwargs)

    # Solve
    timer1 = Timer(timeout)
    stats1 = find_tour(edges, timer1)
    name1 = find_tour.__name__

    timer2 = Timer(timeout)
    stats2 = sec_find_tour(edges, timer2)
    name2 = sec_find_tour.__name__

    print(format_text_summary(name1, stats1[-1]))
    print(format_text_summary(name2, stats2[-1]))

    all_stats = {
        name1: stats1,
        name2: stats2
    }

    # Report and Plot
    n_plots = 6

    fig, axs = plt.subplots(n_plots, 1, figsize=(8, 8 * n_plots))
    if n_plots > 1:
        axs = axs.flatten()
    else:
        axs = [axs]

    draw_edges = n <= 10

    # Plot network and solution
    ax = axs[0]
    plot_network(locations, edges, edge_alpha=0.5 if draw_edges else 0.1, ax=ax)

    if stats1[-1].tour:
        plot_tour(locations, stats1[-1].tour, ax=ax)
    if stats2[-1].tour:
        plot_tour(locations, stats2[-1].tour, ax=ax)

    ax.set_title("Final tours: greedy vs backtracking")

    # Plot stats
    plot_solutions(all_stats, axs[1])
    plot_coverage(all_stats, ax=axs[2])
    plot_queue_size(all_stats, ax=axs[3])
    plot_edge_probability(all_stats, edges, ax=axs[4])
    for name, stats in all_stats.items():
        plot_solution_evolution([st.tour for st in stats], ax=axs[5])

    axs[6].set_title("Solution evolution (greedy vs backtracking)")
    print(len(plt.get_fignums()))
    plt.savefig("baseline_vs_core_empirical.png", bbox_inches="tight", dpi=300)
    plt.show()


if __name__ == '__main__':
    from tsp_solve_backtracking import (random_tour, greedy_tour, backtracking, backtracking_bssf)

    main(
        15,
        # random_tour,
        greedy_tour,
        backtracking,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=306,
        timeout=60
    )

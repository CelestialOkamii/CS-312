import math
import matplotlib.pyplot as plt

from utils import generate_network, Timer
from tsp_solve_backtracking import greedy_tour, backtracking


def run_scaling_experiment(
    ns,
    timeout=60,
    seed=306,
    **kwargs
):
    greedy_times = []
    backtracking_times = []

    for n in ns:
        print(f"Running n = {n}")

        locations, edges = generate_network(n, seed=seed, **kwargs)

        # --- Greedy ---
        timer = Timer(timeout)
        g_stats = greedy_tour(edges, timer)
        greedy_times.append(g_stats[-1].time)

        # --- Backtracking ---
        timer = Timer(timeout)
        b_stats = backtracking(edges, timer)
        backtracking_times.append(b_stats[-1].time)

    return greedy_times, backtracking_times


def plot_empirical_vs_theoretical(ns, greedy_times, backtracking_times):
    plt.figure(figsize=(8, 6))

    # Empirical curves
    plt.plot(ns, greedy_times, marker='o', label="Greedy (empirical)")
    plt.plot(ns, backtracking_times, marker='o', label="Backtracking (empirical)")

    # --- Theoretical curves (scaled for shape comparison) ---
    n0 = ns[0]

    greedy_theory = [greedy_times[0] * (n / n0) ** 2 for n in ns]
    backtracking_theory = [
        backtracking_times[0] * math.factorial(n) / math.factorial(n0)
        for n in ns
    ]

    plt.plot(ns, greedy_theory, linestyle='--', label="Greedy O(n²)")
    plt.plot(ns, backtracking_theory, linestyle='--', label="Backtracking O(n!)")

    plt.xlabel("Problem size (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Empirical Runtime vs Theoretical Growth")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("empirical_vs_theoretical_runtime.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    ns = [5, 7, 9, 11]  # adjust upward carefully

    greedy_times, backtracking_times = run_scaling_experiment(
        ns,
        timeout=60,
        euclidean=True,
        reduction=0.2,
        normal=False
    )

    plot_empirical_vs_theoretical(ns, greedy_times, backtracking_times)
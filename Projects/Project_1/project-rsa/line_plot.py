import matplotlib.pyplot as plt
import time

t_data = {
    64: 671,
    128: 10740,
    256: 171798,
    512: 2748800,
    1024: 43980000,
    2048: 703687000
}

line_y = [n * n * n * n * 0.00004 for n in t_data.keys()]

plt.scatter(
    t_data.keys(),
    t_data.values(),
    marker='o',
    c="red"
)

plt.plot(
    t_data.keys(),
    line_y,
    c='grey',
    ls=':',
    lw=2,
    alpha=0.5
)

e_data = {
    64: 0.00138,
    128: 0.00283,
    256: 0.01724,
    512: 0.31531
}

line_x = [n * n * n * n * 0.000000000004 for n in e_data.keys()]

plt.scatter(
    e_data.keys(),
    e_data.values(),
    marker='o',
    c="green"
)

plt.plot(
    e_data.keys(),
    line_x,
    c='grey',
    ls=':',
    lw=2,
    alpha=0.5
)

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Bit size (n)")
plt.ylabel("Time (ms)")
plt.title("Theoretical vs Experimental Prime Generation Times")
plt.legend(["Theoretical", "Measured", "Empirical"])
plt.show()
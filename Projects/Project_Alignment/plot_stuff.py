import matplotlib.pyplot as plt
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


runtimes = [(100, 0.0007154941558837891), (100, 0.0007033348083496094), (100, 0.0010044574737548828), (1000, 0.008655786514282227), (1000, 0.008903741836547852), (1000, 0.009397506713867188), (5000, 0.045005083084106445), (5000, 0.05087542533874512), (5000, 0.045900583267211914), (10000, 0.1157083511352539), (10000, 0.11524224281311035), (10000, 0.10196781158447266), (15000, 0.18511557579040527), (15000, 0.16797566413879395), (15000, 0.16700124740600586), (20000, 0.24405503273010254), (20000, 0.2392122745513916), (20000, 0.23413777351379395), (25000, 0.30519914627075195), (25000, 0.2939577102661133), (25000, 0.2862553596496582), (30000, 0.3138718605041504), (30000, 0.3268163204193115), (30000, 0.35035037994384766)]
unbanded_runtimes = [(500, 0.10601472854614258), (500, 0.13294315338134766), (500, 0.11905789375305176), (500, 0.08493828773498535), (500, 0.06403326988220215), (500, 0.07627081871032715), (1000, 0.44745850563049316), (1000, 0.5315663814544678), (1000, 0.5018796920776367), (1000, 0.3302013874053955), (1000, 0.3386540412902832), (1000, 0.2896137237548828), (1500, 0.9810831546783447), (1500, 1.2260863780975342), (1500, 1.1203899383544922), (1500, 0.6788647174835205), (1500, 0.715376615524292), (1500, 0.6862666606903076), (2000, 1.5694489479064941), (2000, 2.302990674972534), (2000, 2.2912449836730957), (2000, 1.4801151752471924), (2000, 1.1945626735687256), (2000, 1.1617915630340576), (2500, 2.5897397994995117), (2500, 3.5380523204803467), (2500, 3.7394769191741943), (2500, 2.246110200881958), (2500, 1.985309362411499), (2500, 1.980726718902588), (3000, 3.5843565464019775), (3000, 4.960872411727905), (3000, 5.574654817581177), (3000, 3.0882933139801025), (3000, 2.746901273727417), (3000, 2.863389492034912)]

def main():
    # Define this
    def theoretical_big_o(v, e):
        return (v * e)

    # Fill in from result using compute_coefficient
    coeff = (0.0000104475 + 0.000010430947045485178 + 0.00001059) / 3
    coeff_unbanded = (0.000721491551410908 + 0.001002412505944569 + 0.000944227026568518 + 0.000952505353640577 + 0.000957606755362616 + 0.00097253 + 0.00099775 + 0.00060343 + 0.00054177 + 0.00053788) / 10

    vv, times = zip(*runtimes)
    #
    # vv = [v for v, _, _ in runtimes]
    # ee = [e for _, e, _ in runtimes]
    #
    # times = [t for _, _, t in runtimes]

    # Plot empirical values
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(vv, times, marker='o')
    #
    # predicted_runtime = [
    #     coeff * theoretical_big_o(v, v)
    #     for v, t in runtimes
    # ]
    #
    # # Plot theoretical fit
    # ax.plot(
    #     vv,
    #     vv,
    #     predicted_runtime,
    #     c='k',
    #     ls=':',
    #     lw=2,
    #     alpha=0.5
    # )
    #
    # # Update title, legend, and axis labels as needed
    # ax.legend(['Observed', 'Theoretical O(nm)'])
    # ax.set_xlabel('n')
    # ax.set_ylabel('m')
    # ax.set_zlabel('Runtime')
    # ax.set_title('Time for Alignment of Sequeneces')
    #
    # # You are welcome to play with the view angle as you'd like
    # # elev=0 with azim=0 and azim=90 might be interesting
    # ax.view_init(elev=10, azim=-60)
    #
    # fig.show()
    # fig.savefig('baseline_empirical.svg')

    data_banded = [
        (100, 0.0007154941558837891), (100, 0.0007033348083496094), (100, 0.0010044574737548828),
        (1000, 0.008655786514282227), (1000, 0.008903741836547852), (1000, 0.009397506713867188),
        (5000, 0.045005083084106445), (5000, 0.05087542533874512), (5000, 0.045900583267211914),
        (10000, 0.1157083511352539), (10000, 0.11524224281311035), (10000, 0.10196781158447266),
        (15000, 0.18511557579040527), (15000, 0.16797566413879395), (15000, 0.16700124740600586),
        (20000, 0.24405503273010254), (20000, 0.2392122745513916), (20000, 0.23413777351379395),
        (25000, 0.30519914627075195), (25000, 0.2939577102661133), (25000, 0.2862553596496582),
        (30000, 0.3138718605041504), (30000, 0.3268163204193115), (30000, 0.35035037994384766)
    ]

    # === Prepare data ===
    n = np.array([x[0] for x in data_banded])
    k = n.copy()  # assume k and n vary together
    runtime = np.array([x[1] for x in data_banded])

    # === Fit constant for theoretical model: Runtime = k_fit * k * n ===
    k_fit = (np.sum(runtime * (k * n)) / np.sum((k * n) ** 2)) * 1.5

    # === Theoretical curve ===
    n_theoretical = np.arange(100, 30001, 5000)
    k_theoretical = n_theoretical.copy()
    runtime_theoretical = k_fit * k_theoretical * n_theoretical

    # === Create 3D plot ===
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Observed points
    ax.scatter(k, n, runtime, label='Observed', s=40)

    # Theoretical line
    ax.plot(k_theoretical, n_theoretical, runtime_theoretical, label='Theoretical O(kn)', linewidth=2)

    # Labels & title
    ax.set_title("Time for Banded Sequence Alignment", fontsize=14, pad=12)
    ax.set_xlabel("k", fontsize=12)
    ax.set_ylabel("n", fontsize=12)
    ax.set_zlabel("Runtime", fontsize=12)
    ax.legend()

    # Save as SVG
    plt.tight_layout()
    plt.savefig("core_emperical.svg", format='svg', bbox_inches='tight')

    print(f"Fitted k = {k_fit:.6e}")
    print("Saved as: time_banded_alignment_fitted.svg")

    plt.show()


if __name__ == '__main__':
    main()

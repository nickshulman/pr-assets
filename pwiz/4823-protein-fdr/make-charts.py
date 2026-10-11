import csv, sqlite3, sys
E = 'D:/GlobalQValueDemo/Entrapment/'
def from_tsv(p):
    with open(p, newline='') as f:
        r = csv.reader(f, delimiter='\t'); next(r)
        return [(row[0], float(row[4])) for row in r]
def from_blib(p):
    c = sqlite3.connect('file:' + p + '?mode=ro', uri=True)
    return [(a, q) for a, q in c.execute('select accession, QValue from Proteins') if q is not None]
def fdp(rows, cut):
    t = e = 0
    for acc, q in rows:
        if q > cut: continue
        accs = acc.split(';')
        if all('_p_target|' in a for a in accs): e += 1
        else: t += 1
    return t, e, (200.0 * e / (t + e) if t + e else 0)
sources = {
  'astral_old_tsv': lambda: from_tsv(E + 'astral-natural/osprey_project/osprey.protein_groups.tsv'),
  'astral_baseline': lambda: from_blib(E + 'astral-natural/osprey_project/osprey-baseline.blib'),
  'astral_paired': lambda: from_blib(E + 'astral-natural/osprey_project/osprey-paired.blib'),
  'astral_paired_all': lambda: from_blib(E + 'astral-natural/osprey_project/osprey-paired-all.blib'),
  'astral_paired_picked': lambda: from_blib(E + 'astral-natural/osprey_project/osprey-paired-picked.blib'),
  'astral_new': lambda: from_tsv(E + 'astral-natural/osprey_project_branch/osprey.protein_groups.tsv'),
  'astral_diann': lambda: from_blib(E + 'astral-natural/diann/diann-entrapment.blib'),
  'stellar_old': lambda: from_tsv(E + 'stellar-natural/osprey_project/osprey.protein_groups.tsv'),
  'stellar_new': lambda: from_tsv(E + 'stellar-natural/osprey_project_branch/osprey.protein_groups.tsv'),
}
for name, load in sources.items():
    rows = load()
    print(name, len(rows), [fdp(rows, c) for c in (0.001, 0.01, 0.05, 1.0)])

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out = sys.argv[1]
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
cuts = [i / 1000.0 for i in range(1, 51)]
def curve(rows): return [fdp(rows, c)[2] for c in cuts]
x = [c * 100 for c in cuts]
data = {k: sources[k]() for k in ('astral_baseline', 'astral_new', 'astral_diann', 'stellar_old', 'stellar_new',
                                   'astral_paired', 'astral_paired_picked')}
OLD, NEW, DIANN = '#d62728', '#1f77b4', '#7f7f7f'

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
for ax, title, old, new, diann in ((axes[0], 'Astral HeLa, 3 runs', 'astral_baseline', 'astral_new', 'astral_diann'),
                                    (axes[1], 'Stellar HeLa, 3 runs', 'stellar_old', 'stellar_new', None)):
    ax.plot([0, 5], [0, 5], ls='--', color='black', lw=1, label='Ideal (measured = reported)')
    ax.plot(x, curve(data[old]), color=OLD, lw=2.5, label='Osprey before (every group q = 0)')
    ax.plot(x, curve(data[new]), color=NEW, lw=2.5, label='Osprey with this PR')
    if diann:
        ax.plot(x, curve(data[diann]), color=DIANN, lw=1.5, ls=':', label='DIA-NN 2.2, same library')
    ax.set_title(title)
    ax.set_xlabel('Reported protein-group q-value cutoff (%)')
    ax.set_xlim(0, 5); ax.set_ylim(0, 8)
    ax.grid(alpha=0.3)
axes[0].set_ylabel('Measured FDP from entrapment (%)')
fig.legend(*axes[0].get_legend_handles_labels(), loc='lower center', ncol=4, frameon=False, fontsize=10)
fig.suptitle('Protein-group FDR: reported q-value vs. false discovery proportion measured with Arabidopsis entrapment', fontsize=12)
fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig(out + '/protein-fdr-calibration.png', dpi=150)

labels = ['Osprey before', 'Pair decoys\nby base id', '+ compete every\nlibrary protein', '+ score from the\nfirst pass (this PR)']
keys = ['astral_baseline', 'astral_paired', 'astral_paired_picked', 'astral_new']
vals = [fdp(data[k], 0.01) for k in keys]
fig, ax = plt.subplots(figsize=(9, 4.8))
bars = ax.bar(labels, [v[2] for v in vals], color=[OLD, OLD, OLD, NEW], width=0.6)
ax.axhline(1.0, color='black', ls='--', lw=1)
ax.text(-0.45, 1.12, 'reported 1%', ha='left', fontsize=10)
for b, (t, e, f) in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, max(f, 1.0) + 0.15, '%.2f%%\n%s groups' % (f, format(t + e, ',')), ha='center', fontsize=10)
ax.set_ylabel('Measured FDP at reported q <= 1% (%)')
ax.set_ylim(0, 8.5)
ax.set_title('Astral: each defect fixed in turn. Only first-pass scores calibrate the competition')
fig.tight_layout()
fig.savefig(out + '/protein-fdr-ablation.png', dpi=150)

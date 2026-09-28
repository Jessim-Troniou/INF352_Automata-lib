from automata.fa.dfa import DFA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyArrowPatch


def etats_distinguables(Q, Sigma, delta, q_init, F):
    """
    Algorithme des états distinguables.
    """
    D = {(p, q) for p in F for q in Q - F} | {(q, p) for p in F for q in Q - F}
    D_pre = set()
    while D_pre != D:
        D_pre = set(D)
        X = {
            (p, q)
            for p in Q
            for q in Q
            if any((delta[p][a], delta[q][a]) in D for a in Sigma)
        }
        D = D | X
    return D


def relation_equivalence(Q, Sigma, delta, q_init, F):
    """
    Relation d'équivalence (complémentaire de la distinguabilité).
    """
    R = {(p, q) for p in F for q in F} | {(p, q) for p in Q - F for q in Q - F}
    R_pre = set()
    while R_pre != R:
        R_pre = set(R)
        X = {(p, q) for (p, q) in R if any((delta[p][a], delta[q][a]) not in R for a in Sigma)}
        R = R - X
    return R


def classes_equivalence(Q, R):
    """Transforme la relation d'équivalence en partition de Q."""
    classes = []
    for q in Q:
        classe = frozenset(p for p in Q if (p, q) in R)
        if classe not in classes:
            classes.append(classe)
    return classes


def minimal_partition_classes(dfa):
    """Retourne les classes finales de minimisation par partition."""
    Q = set(dfa.states)
    Sigma = set(dfa.input_symbols)
    delta = dfa.transitions
    F = set(dfa.final_states)

    classes = [set(F), set(Q - F)]
    classes = [c for c in classes if c]
    changed = True
    while changed:
        changed = False
        new_classes = []
        for cls in classes:
            buckets = {}
            for q in cls:
                signature = []
                for a in sorted(Sigma):
                    target = delta[q][a]
                    for idx, c in enumerate(classes):
                        if target in c:
                            signature.append(idx)
                            break
                signature = tuple(signature)
                buckets.setdefault(signature, set()).add(q)
            new_classes.extend(buckets.values())
        if sorted(map(frozenset, new_classes)) != sorted(map(frozenset, classes)):
            changed = True
            classes = [set(c) for c in new_classes]
    return [sorted(c) for c in classes]


def draw_minimal_graph(states, alphabet, transitions, start, finals, title, filename):
    pos = {
        'A': (0, 0),
        'B': (2.5, 1.5),
        'C': (2.5, -1.5),
    }
    if states != {'A', 'B', 'C'}:
        pos = {s: (i * 2.2, 0 if i % 2 == 0 else 1.5) for i, s in enumerate(sorted(states))}
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(-1.5, 6.5)
    ax.set_ylim(-2.5, 2.8)
    ax.axis('off')
    ax.set_title(title, fontsize=12)

    for s in states:
        x, y = pos[s]
        face = '#dfefff' if s in finals else '#f4f4f4'
        edge = 'black'
        circle = Circle((x, y), 0.55, facecolor=face, edgecolor=edge, lw=1.5)
        ax.add_patch(circle)
        ax.text(x, y, s, ha='center', va='center', fontsize=12, fontweight='bold')
        if s == start:
            ax.text(x - 0.9, y + 0.8, 'start', fontsize=9)

    for s in states:
        for a in sorted(alphabet):
            t = transitions[s][a]
            x1, y1 = pos[s]
            x2, y2 = pos[t]
            dx, dy = x2 - x1, y2 - y1
            norm = (dx ** 2 + dy ** 2) ** 0.5
            if norm == 0:
                continue
            nx, ny = dx / norm, dy / norm
            start_x = x1 + nx * 0.55
            start_y = y1 + ny * 0.55
            end_x = x2 - nx * 0.55
            end_y = y2 - ny * 0.55
            arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y), arrowstyle='->', mutation_scale=14, lw=1.2)
            ax.add_patch(arrow)
            mx, my = (start_x + end_x) / 2, (start_y + end_y) / 2
            ax.text(mx, my + 0.2, a, ha='center', va='center', fontsize=10, color='black')

    plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.close(fig)


# Automate d1 du notebook

d1 = DFA(
    states={"1", "2", "3", "4"},
    input_symbols={"a", "b"},
    transitions={
        "1": {"a": "2", "b": "3"},
        "2": {"a": "1", "b": "1"},
        "3": {"a": "2", "b": "4"},
        "4": {"a": "4", "b": "4"},
    },
    initial_state="1",
    final_states={"2", "3", "4"},
)

# Automate d2 du notebook

d2 = DFA(
    states={"1", "2", "3", "4", "5", "6"},
    input_symbols={"0", "1"},
    transitions={
        "1": {"0": "6", "1": "2"},
        "2": {"0": "5", "1": "3"},
        "3": {"0": "6", "1": "6"},
        "4": {"0": "5", "1": "6"},
        "5": {"0": "3", "1": "4"},
        "6": {"0": "6", "1": "6"},
    },
    initial_state="1",
    final_states={"1", "5"},
)

# Résultats calculés
classes1 = classes_equivalence(d1.states, relation_equivalence(d1.states, d1.input_symbols, d1.transitions, d1.initial_state, d1.final_states))
classes2 = classes_equivalence(d2.states, relation_equivalence(d2.states, d2.input_symbols, d2.transitions, d2.initial_state, d2.final_states))

# Minimal forms
minimal_d1 = {
    'states': {"1", "2", "3", "4"},
    'alphabet': {"a", "b"},
    'transitions': {
        "1": {"a": "2", "b": "3"},
        "2": {"a": "1", "b": "1"},
        "3": {"a": "2", "b": "4"},
        "4": {"a": "4", "b": "4"},
    },
    'start': "1",
    'finals': {"2", "3", "4"},
    'title': "Automate minimal de d1"
}

minimal_d2 = {
    'states': {"A", "B", "C"},
    'alphabet': {"0", "1"},
    'transitions': {
        "A": {"0": "C", "1": "B"},
        "B": {"0": "A", "1": "C"},
        "C": {"0": "C", "1": "C"},
    },
    'start': "A",
    'finals': {"A"},
    'title': "Automate minimal de d2"
}

# Génération PDF
pdf_path = 'exercice_33_solution.pdf'
with PdfPages(pdf_path) as pdf:
    fig = plt.figure(figsize=(8.5, 11))
    fig.text(0.06, 0.95, 'Exercice 33 — Déterminer si un automate est minimal ou non', fontsize=18, fontweight='bold')
    fig.text(0.06, 0.88, 'On considère les deux automates de la Figure 6.3. On applique l\'algorithme des états distinguables puis la relation d\'équivalence.', fontsize=12)
    fig.text(0.06, 0.82, '1) Méthode des états distinguables', fontsize=13, fontweight='bold')
    fig.text(0.06, 0.77, 'd1 : D = {(1,2),(1,3),(1,4),(2,1),(2,3),(2,4),(3,1),(3,2),(3,4),(4,1),(4,2),(4,3)}', fontsize=10)
    fig.text(0.06, 0.73, 'd2 : D contient toutes les paires entre classes distinctes et les paires (1,5), (5,1), (2,4), (4,2), (3,6), (6,3)', fontsize=10)
    fig.text(0.06, 0.68, '2) Méthode des classes d\'équivalence', fontsize=13, fontweight='bold')
    fig.text(0.06, 0.63, 'd1 : classes = [[1], [2], [3], [4]]', fontsize=10)
    fig.text(0.06, 0.59, 'd2 : classes = [[1,5], [2,4], [3,6]]', fontsize=10)
    fig.text(0.06, 0.54, 'Conclusion :', fontsize=13, fontweight='bold')
    fig.text(0.06, 0.49, '- d1 est minimal : chaque état est distinct et aucune fusion n\'est possible.', fontsize=11)
    fig.text(0.06, 0.45, '- d2 n\'est pas minimal : 1 ≡ 5, 2 ≡ 4, 3 ≡ 6. On réduit donc à 3 états.', fontsize=11)
    fig.text(0.06, 0.38, '3) Représentation de l\'automate minimal', fontsize=13, fontweight='bold')
    fig.text(0.06, 0.33, 'd1 minimal : états 1,2,3,4 (inchangés).', fontsize=10)
    fig.text(0.06, 0.29, 'd2 minimal : A={1,5}, B={2,4}, C={3,6}; état initial A; états finaux {A}.', fontsize=10)
    fig.text(0.06, 0.22, 'Table de transition du minimal d2 :', fontsize=11)
    fig.text(0.06, 0.17, '        0        1', fontsize=10)
    fig.text(0.06, 0.13, 'A -> C     ; A -> B', fontsize=10)
    fig.text(0.06, 0.09, 'B -> A     ; B -> C', fontsize=10)
    fig.text(0.06, 0.05, 'C -> C     ; C -> C', fontsize=10)
    pdf.savefig(fig)
    plt.close(fig)

    # Graphique minimal d1
    fig = plt.figure(figsize=(7.5, 4))
    fig.text(0.1, 0.92, 'Automate minimal d1', fontsize=12, fontweight='bold')
    ax = fig.add_axes([0.08, 0.09, 0.84, 0.75])
    states = sorted(minimal_d1['states'])
    pos = {s: (i * 2, 0) for i, s in enumerate(states)}
    for s in states:
        x, y = pos[s]
        c = Circle((x, y), 0.55, facecolor='#e8f2ff' if s in minimal_d1['finals'] else '#f4f4f4', edgecolor='black', lw=1.2)
        ax.add_patch(c)
        ax.text(x, y, s, ha='center', va='center', fontsize=12)
        if s == minimal_d1['start']:
            ax.text(x - 0.9, y + 0.8, 'start', fontsize=9)
    for s in states:
        for a in sorted(minimal_d1['alphabet']):
            t = minimal_d1['transitions'][s][a]
            x1, y1 = pos[s]
            x2, y2 = pos[t]
            arrow = FancyArrowPatch((x1 + 0.5, y1), (x2 - 0.5, y2), arrowstyle='->', mutation_scale=14)
            ax.add_patch(arrow)
            ax.text((x1 + x2) / 2, 0.35, a, ha='center', fontsize=10)
    ax.set_xlim(-1, max(2 * len(states), 5))
    ax.set_ylim(-1.8, 1.8)
    ax.axis('off')
    pdf.savefig(fig)
    plt.close(fig)

    # Graphique minimal d2
    fig = plt.figure(figsize=(7.5, 4))
    fig.text(0.1, 0.92, 'Automate minimal d2', fontsize=12, fontweight='bold')
    ax = fig.add_axes([0.08, 0.09, 0.84, 0.75])
    states = sorted(minimal_d2['states'])
    pos = {'A': (0, 0), 'B': (2.5, 1.3), 'C': (2.5, -1.3)}
    for s in states:
        x, y = pos[s]
        c = Circle((x, y), 0.55, facecolor='#e8f2ff' if s in minimal_d2['finals'] else '#f4f4f4', edgecolor='black', lw=1.2)
        ax.add_patch(c)
        ax.text(x, y, s, ha='center', va='center', fontsize=12)
        if s == minimal_d2['start']:
            ax.text(x - 0.9, y + 0.8, 'start', fontsize=9)
    for s in states:
        for a in sorted(minimal_d2['alphabet']):
            t = minimal_d2['transitions'][s][a]
            x1, y1 = pos[s]
            x2, y2 = pos[t]
            arrow = FancyArrowPatch((x1 + 0.5, y1), (x2 - 0.5, y2), arrowstyle='->', mutation_scale=14)
            ax.add_patch(arrow)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.2, a, ha='center', fontsize=10)
    ax.set_xlim(-1, 4.5)
    ax.set_ylim(-2.2, 2.2)
    ax.axis('off')
    pdf.savefig(fig)
    plt.close(fig)

print(f'PDF generated: {pdf_path}')

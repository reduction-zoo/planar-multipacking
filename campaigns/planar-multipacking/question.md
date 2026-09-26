# Planar subcubic Independent Set → Planar Multipacking

Category: Complexity open

## Source

The source gives a planar graph of maximum degree three and a bound k. Its outputs are independent vertex sets of size at least k, or NO-SOLUTION.

## Target

Given a planar graph G and integer t, find at least t vertices M such that every radius-r ball contains at most r members of M for every vertex and every integer 1≤r≤the number of vertices, or report NO-SOLUTION.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

Multipacking links metric packing constraints to domination-type graph parameters; planar hardness would clarify how geometry affects its complexity.

## Difficulty

Local gadgets must satisfy constraints at every radius, not just nearest-neighbor exclusions.

## Literature context

The target imposes packing constraints at every graph radius. Planar Independent Set hardness alone does not supply a reduction respecting those constraints.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [On the Complexity of Multipacking](https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/LIPIcs.ESA.2026.152/LIPIcs.ESA.2026.152.pdf): Das, Islam and Lokshtanov, On the Complexity of Multipacking, ESA 2026, Section 6, printed page 152:16, explicitly leaves planar complexity unresolved. Its general and restricted-class hardness results do not impose planarity. Directed planar hardness uses different distance semantics. The February preprint, Section 6, asks the same question; the conference version was published on August 25.
- [February preprint](https://arxiv.org/html/2602.07982v1): Das, Islam and Lokshtanov, On the Complexity of Multipacking, ESA 2026, Section 6, printed page 152:16, explicitly leaves planar complexity unresolved. Its general and restricted-class hardness results do not impose planarity. Directed planar hardness uses different distance semantics. The February preprint, Section 6, asks the same question; the conference version was published on August 25.
- [thesis](https://arxiv.org/html/2602.07927v1): Islam's thesis, Sections 5.2–5.3, defines r-Multipacking by checking only radii 1 through r. Lemma 5.3.2 reduces planar subcubic Independent Set to that truncated problem, with threshold k+|E(H)|(r-1). This is not the full target above.

Fixed from board record `website/questions/planar-multipacking.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.

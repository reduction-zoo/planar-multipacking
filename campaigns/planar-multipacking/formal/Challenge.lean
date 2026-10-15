module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace PlanarMultipacking

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

/-- Relational version for witnesses with quantified real or optimality conditions. -/
def relationalOutput {I W : Type} (legal : I → Bool) (witness : I → W → Prop)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w
  | none => legal x = true ∧ ¬ ∃ w, witness x w

structure Graph where
  n : Nat
  edges : List (Nat × Nat)
  deriving Repr

def adjacent (g : Graph) (u v : Nat) : Bool :=
  g.edges.any (fun e => (e.1 == u && e.2 == v) || (e.1 == v && e.2 == u))

def simple (g : Graph) : Bool :=
  g.edges.all (fun e => e.1 < g.n && e.2 < g.n && e.1 != e.2) &&
  decide ((g.edges.map (fun e => (min e.1 e.2, max e.1 e.2))).Nodup)

/-- Vertices at distance at most the supplied bound, including the starting set. -/
def ballFrom (g : Graph) : Nat → List Nat → List Nat
  | 0, seen => seen
  | k + 1, seen => ballFrom g k ((List.range g.n).filter (fun v =>
      seen.contains v || seen.any (fun u => adjacent g u v)))

def connected (g : Graph) : Bool :=
  g.n > 0 && (ballFrom g g.n [0]).length == g.n

def diameterAtMost (g : Graph) (d : Nat) : Bool :=
  (List.range g.n).all (fun v => (ballFrom g d [v]).length == g.n)

def radiusAtMost (g : Graph) (r : Nat) : Bool :=
  (List.range g.n).any (fun v => (ballFrom g r [v]).length == g.n)

def boolWords : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (boolWords n).flatMap (fun xs => [false :: xs, true :: xs])

def bipartite (g : Graph) : Bool :=
  (boolWords g.n).any (fun side => g.edges.all (fun e => side[e.1]? != side[e.2]?))

def crossingDegree (g : Graph) (side : List Bool) (v : Nat) : Nat :=
  ((List.range g.n).filter (fun u => adjacent g u v && side[u]? != side[v]?)).length

def nontrivialCut (g : Graph) (side : List Bool) : Bool :=
  side.length == g.n && side.contains true && side.contains false

def perfectCut (g : Graph) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v == 1)

def boundedCut (g : Graph) (d : Nat) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v ≤ d)

def encodeGraph (g : Graph) : List Bool :=
  encodeList encodeNat (List.range g.n) ++
  encodeList (fun e => encodeNat e.1 ++ encodeNat e.2) g.edges
def encodeInt (z : Int) : List Bool := [decide (z < 0)] ++ encodeNat z.natAbs
def encodeRat (q : Rat) : List Bool := encodeInt q.num ++ encodeNat q.den
abbrev Point := Rat × Rat

def cross (a b c : Point) : Rat := (b.1-a.1)*(c.2-a.2) - (b.2-a.2)*(c.1-a.1)
def onSegment (p a b : Point) : Bool :=
  cross a b p == 0 && min a.1 b.1 ≤ p.1 && p.1 ≤ max a.1 b.1 &&
  min a.2 b.2 ≤ p.2 && p.2 ≤ max a.2 b.2
def intersectsSegment (a b c d : Point) : Bool :=
  max (min a.1 b.1) (min c.1 d.1) ≤ min (max a.1 b.1) (max c.1 d.1) &&
  max (min a.2 b.2) (min c.2 d.2) ≤ min (max a.2 b.2) (max c.2 d.2) &&
  cross a b c * cross a b d ≤ 0 && cross c d a * cross c d b ≤ 0

def planeDrawing (g : Graph) (points : List Point) : Bool :=
  points.length == g.n && decide points.Nodup &&
  g.edges.all (fun e => (List.range g.n).all (fun v =>
    v == e.1 || v == e.2 || !onSegment (points[v]?.getD (0,0)) (points[e.1]?.getD (0,0)) (points[e.2]?.getD (0,0)))) &&
  g.edges.all (fun e => g.edges.all (fun f =>
    !(decide [e.1,e.2,f.1,f.2].Nodup) ||
    !intersectsSegment (points[e.1]?.getD (0,0)) (points[e.2]?.getD (0,0))
      (points[f.1]?.getD (0,0)) (points[f.2]?.getD (0,0))))
def encodePoints := encodeList (fun p : Point => encodeRat p.1 ++ encodeRat p.2)

def planar (g : Graph) : Prop := ∃ points, planeDrawing g points = true
noncomputable def legalSource (x : Graph × Nat) : Bool := by
  classical
  exact decide (simple x.1 = true ∧ planar x.1 ∧
    ((List.range x.1.n).all (fun v => ((List.range x.1.n).filter (adjacent x.1 v)).length ≤ 3)) = true)
noncomputable def legalTarget (x : Graph × Nat) : Bool := by
  classical
  exact decide (simple x.1 = true ∧ planar x.1)
def sourceWitness (x : Graph × Nat) (w : List Nat) : Bool :=
  decide w.Nodup && w.length ≥ x.2 && w.all (fun v => v < x.1.n) &&
  x.1.edges.all (fun e => !(w.contains e.1 && w.contains e.2))
def targetWitness (x : Graph × Nat) (w : List Nat) : Bool :=
  decide w.Nodup && w.length ≥ x.2 && w.all (fun v => v < x.1.n) &&
  (List.range x.1.n).all (fun v => (List.range x.1.n).all (fun r =>
    (w.filter (ballFrom x.1 (r+1) [v]).contains).length ≤ r+1))
def encodeSource (x : Graph × Nat) := encodeGraph x.1 ++ encodeNat x.2
def encodeTarget := encodeSource
def validSourceOutput := searchOutput legalSource sourceWitness
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : (Graph × Nat) → (Graph × Nat))
    (recover : (Graph × Nat) × Option (List Nat) → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))


def Goal : Prop :=
  ∃ (forward : (Graph × Nat) → (Graph × Nat))
    (recover : (Graph × Nat) × Option (List Nat) → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end PlanarMultipacking

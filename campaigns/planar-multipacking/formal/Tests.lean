import Challenge
open PlanarMultipacking
example : targetWitness (⟨3,[(0,1),(1,2)]⟩,2) [0,2] = false := by native_decide
example : targetWitness (⟨4,[(0,1),(1,2),(2,3)]⟩,2) [0,3] = true := by native_decide
example : planeDrawing ⟨4,[(0,2),(1,3)]⟩ [(0,0),(0,1),(1,1),(1,0)] = false := by native_decide

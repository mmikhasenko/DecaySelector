# README: -lhcb- to state- JSON Conversion

This document describes the logic of the conversion from a `-lhcb-` JSON file (e.g., `lc2ppik-lhcb-2683025.json`) to a `state-` JSON file (e.g., `state_v21-17_24.json`).

## Conversion Logic

1. **Final State Mapping**
   - The initial and final state particles from the `-lhcb-` JSON are mapped to the `finalState.finalStateData` section of the `state-` JSON.
   - Particle properties such as `name` and `spin` are preserved. Spin values like "1/2" are converted to floats (e.g., 0.5).

2. **Main Graph Mapping**
   - does not need to be mapped.

3. **Intermediate State (Resonances/Isobars)**
   - the `-lhcb-` JSON file describes decay chains in terms of propagators and vertexes,
   - each propagator is a resonances in the the `state-` JSON.
   - The `-lhcb-` JSON is more granular and precise in describing how each chain looks like, while the `state-` JSON builds decay chains by iterating over all given propagators.
   - for three-body decays, the name of topology can be taken as a name of the resonance
   - two files use the same convention for propagator / vertices labeling with tuples
   - parity is not given in the `-lhcb-` JSON, so it put it to -1
   - mass and width field for the `state-` JSON can be indicated for these propagators that are parametrized by `BreitWigner` function in the `-lhcb-` JSON.


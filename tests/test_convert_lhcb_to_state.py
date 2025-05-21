import json
import sys
from pathlib import Path

def test_structural_and_conceptual_similarity(lhcb_json_path, state_json_path, converted_json_path):
    # Load files
    with open(lhcb_json_path) as f:
        lhcb = json.load(f)
    with open(state_json_path) as f:
        state_ref = json.load(f)
    with open(converted_json_path) as f:
        state_conv = json.load(f)

    errors = []

    # Test 1: Output is valid JSON and has required top-level keys
    required_keys = ["decay", "graph", "mainGraph", "finalState", "intermediateState"]
    for k in required_keys:
        if k not in state_conv:
            errors.append(f"Missing key in converted: {k}")

    # Test 2: Final state mapping
    n_input_particles = 1 + len(lhcb['distributions'][0]['decay_description']['kinematics']['final_state'])
    n_output_particles = len(state_conv['finalState']['finalStateData'])
    if n_input_particles != n_output_particles:
        errors.append(f"Mismatch in number of particles: input={n_input_particles}, output={n_output_particles}")

    # Test 3: Main graph mapping
    ref_top = lhcb['distributions'][0]['decay_description']['reference_topology']
    if state_conv['mainGraph']['tuple'] != ref_top:
        errors.append("mainGraph.tuple does not match reference_topology from input")

    # Test 4: Particle identity preservation
    input_particles = [lhcb['distributions'][0]['decay_description']['kinematics']['initial_state']] + \
                     lhcb['distributions'][0]['decay_description']['kinematics']['final_state']
    for i, p in enumerate(input_particles):
        out = state_conv['finalState']['finalStateData'].get(str(i))
        if not out:
            errors.append(f"Missing particle {i} in output finalStateData")
            continue
        if out['name'] != p['name']:
            errors.append(f"Particle name mismatch at {i}: {out['name']} != {p['name']}")
        if parse_spin(out['spin']) != parse_spin(p['spin']):
            errors.append(f"Particle spin mismatch at {i}: {out['spin']} != {p['spin']}")

    # Test 5: Topology preservation (mainGraph)
    if state_conv['mainGraph']['tuple'] != ref_top:
        errors.append("mainGraph.tuple does not match input reference_topology")

    # Print results
    if errors:
        print("TEST FAILED:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print("All structural and conceptual tests passed.")

def parse_spin(spin_str):
    if isinstance(spin_str, (int, float)):
        return float(spin_str)
    if '/' in str(spin_str):
        num, denom = spin_str.split('/')
        return float(num) / float(denom)
    return float(spin_str)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python test_convert_lhcb_to_state.py <input_lhcb.json> <reference_state.json> <converted_state.json>")
        sys.exit(1)
    test_structural_and_conceptual_similarity(sys.argv[1], sys.argv[2], sys.argv[3])

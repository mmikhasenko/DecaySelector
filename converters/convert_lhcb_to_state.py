import json
import sys
from pathlib import Path

def convert_lhcb_json_to_state_json(input_path, output_path):
    with open(input_path, 'r') as f:
        lhcb_data = json.load(f)

    # Assume only one distribution for now
    dist = lhcb_data['distributions'][0]
    decay_desc = dist['decay_description']
    kin = decay_desc['kinematics']
    initial = kin['initial_state']
    finals = kin['final_state']

    def parse_spin(spin_str):
        if isinstance(spin_str, (int, float)):
            return float(spin_str)
        if '/' in str(spin_str):
            num, denom = spin_str.split('/')
            return float(num) / float(denom)
        return float(spin_str)

    # Map initial and final states
    finalStateData = {}
    finalStateData["0"] = {
        "spin": parse_spin(initial["spin"]),
        "parity": None,  # Parity not present in lhcb json
        "name": initial["name"]
    }
    for i, p in enumerate(finals, 1):
        finalStateData[str(i)] = {
            "spin": parse_spin(p["spin"]),
            "parity": None,  # Parity not present in lhcb json
            "name": p["name"]
        }

    # Map reference_topology to mainGraph
    mainGraph = {"tuple": decay_desc["reference_topology"]}

    # Build isobars from chains/propagators
    functions = lhcb_data.get("functions", [])
    func_type_map = {f["name"]: f["type"] for f in functions if "name" in f and "type" in f}
    isobars = {}
    for chain in decay_desc.get("chains", []):
        for prop in chain.get("propagators", []):
            tuple_key = str(prop["node"])
            resonance_name = prop.get("parametrization") or prop.get("type") or "resonance"
            spin = parse_spin(prop["spin"])
            # Build resonance entry
            resonance_entry = {
                "name": resonance_name,
                "spin": spin,
                "parity": -1,
                "tuple": prop["node"]
            }
            # Check if the resonance is BreitWigner by looking up its type in functions
            if func_type_map.get(resonance_name) == "BreitWigner":
                # Find the function dict for this resonance
                func = next((f for f in functions if f.get("name") == resonance_name), None)
                if func:
                    if "mass" in func:
                        resonance_entry["mass"] = func["mass"]
                    if "width" in func:
                        resonance_entry["width"] = func["width"]
            # Add to isobars structure
            if tuple_key not in isobars:
                isobars[tuple_key] = {
                    "resonances": {},
                    "label": tuple_key,
                    "tuple": prop["node"]
                }
            isobars[tuple_key]["resonances"][resonance_name] = resonance_entry

    # Compose state json
    state_json = {
        "decay": len(finals) + 1,
        "graph": {
            "topologies": [decay_desc["reference_topology"]]  # Placeholder, real state- json has more
        },
        "mainGraph": mainGraph,
        "finalState": {
            "nodes": list(range(len(finals) + 1)),
            "finalStateData": finalStateData
        },
        "intermediateState": {
            "isobars": isobars
        }
    }

    with open(output_path, 'w') as f:
        json.dump(state_json, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_lhcb_to_state.py <input_lhcb.json> <output_state.json>")
        sys.exit(1)
    convert_lhcb_json_to_state_json(sys.argv[1], sys.argv[2])

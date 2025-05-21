# DecaySelector: State Format Conversion and Testing

This repository is dedicated to the conversion, validation, and testing of the `state-` JSON format for amplitude analysis, as used in the [DecaySelector project](https://kaihabermann.github.io/DecaySelector/).

## Features
- **Conversion Tools:**
  - Convert `-lhcb-` JSON files (e.g., from LHCb amplitude analyses) to the `state-` JSON format.
  - See `converters/convert_lhcb_to_state.py` for the main conversion script.
- **Testing and Validation:**
  - Automated tests to ensure structural and conceptual consistency between input and output formats.
  - See `tests/test_convert_lhcb_to_state.py` and reference files in `tests/`.
- **Documentation:**
  - Detailed mapping logic and conversion notes in `docs/README_lhcb2state.md`.

## Directory Structure
- `converters/` — Conversion scripts
- `data/` — Example input and output JSON files
- `tests/` — Test scripts and reference state- files
- `docs/` — Documentation and mapping logic

## Supported Formats
- **state- JSON:**
  - Used for describing decay chains, topologies, and resonance structures in amplitude analyses.
  - See [DecaySelector documentation](https://kaihabermann.github.io/DecaySelector/) for details.
- **Compatibility:**
  - The repository is designed to be extensible for other serialization standards, such as the [amplitude-serialization format](https://rub-ep1.github.io/amplitude-serialization/).

## Usage
1. Place your `-lhcb-` JSON file in the `data/` directory.
2. Run the conversion script:
   ```sh
   python converters/convert_lhcb_to_state.py data/lc2ppik-lhcb-2683025.json data/converted_lc2ppik-state.json
   ```
3. Run the test script to validate the output:
   ```sh
   python tests/test_convert_lhcb_to_state.py data/lc2ppik-lhcb-2683025.json tests/state_v21-17_24.json data/converted_lc2ppik-state.json
   ```

## Contributing
Contributions for additional converters, tests, or documentation are welcome.

## License
See `decayamplitude/LICENSE.md` for license information.

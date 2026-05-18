from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

TARGET_RUN = ROOT / "data" / "target_run"
INITIAL_RUN = ROOT / "data" / "initial_run"

TARGET_LAYER_PARAMS = {
    0: (346.4101615, 200.0000000, 2000.0, 1000.0, 1000.0),
    1: (389.7114317, 225.0000000, 2000.0, 1000.0, 1000.0),
    2: (433.0127019, 250.0000000, 2000.0, 1000.0, 1000.0),
}

INITIAL_LAYER_PARAMS = {
    0: (346.4101615, 200.0000000, 2000.0, 1000.0, 1000.0),
    1: (346.4101615, 200.0000000, 2000.0, 1000.0, 1000.0),
    2: (346.4101615, 200.0000000, 2000.0, 1000.0, 1000.0),
}


def parse_pml_base_materials(material_input_path):
    lines = material_input_path.read_text().splitlines()

    nmat = int(lines[0].strip())
    material_lines = lines[1:1 + nmat]

    pml_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("# PML properties"):
            pml_start = i
            break

    if pml_start is None:
        raise RuntimeError("Could not find '# PML properties' section.")

    pml_lines = lines[pml_start:]

    base_layer_for_material_id = {
        0: 0,
        1: 1,
        2: 2,
    }

    next_material_id = 3

    for line in pml_lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        parts = stripped.split()

        if len(parts) < 9:
            continue

        if next_material_id >= nmat:
            break

        base_mat = int(float(parts[-1]))

        if base_mat not in [0, 1, 2]:
            raise RuntimeError(
                f"Unexpected base material id {base_mat} in PML line: {line}"
            )

        base_layer_for_material_id[next_material_id] = base_mat
        next_material_id += 1

    if len(base_layer_for_material_id) != nmat:
        raise RuntimeError(
            f"Material mapping is incomplete: nmat={nmat}, "
            f"mapped={len(base_layer_for_material_id)}"
        )

    return nmat, material_lines, pml_lines, base_layer_for_material_id


def generate_material_input(run_dir, layer_params, output_name="material.input"):
    material_path = run_dir / "material.input"
    backup_path = run_dir / "material.input.original_backup"

    if not material_path.exists():
        raise FileNotFoundError(f"Missing material.input in {run_dir}")

    if not backup_path.exists():
        shutil.copy2(material_path, backup_path)

    nmat, original_material_lines, pml_lines, mapping = parse_pml_base_materials(
        material_path
    )

    new_lines = [str(nmat)]

    for material_id in range(nmat):
        original_type = original_material_lines[material_id].split()[0]

        mat_type = original_type
        base_layer = mapping[material_id]

        if base_layer not in layer_params:
            raise RuntimeError(
                f"Unexpected base layer id {base_layer} for material id {material_id}"
            )

        vp, vs, rho, qk, qm = layer_params[base_layer]

        new_lines.append(
            f"{mat_type} {vp:.7f} {vs:.7f} {rho:.7f} {qk:.7f} {qm:.7f}"
        )

    new_lines.extend(pml_lines)

    out_path = run_dir / output_name
    out_path.write_text("\n".join(new_lines) + "\n")

    print()
    print("=" * 80)
    print("Generated:", out_path)
    print("Number of material entries:", nmat)
    print("Material id -> base layer mapping:")

    for mid in range(nmat):
        print(f"  id {mid:2d} -> layer {mapping[mid]}")


def main():
    if not TARGET_RUN.exists():
        raise FileNotFoundError(f"Missing target run directory: {TARGET_RUN}")

    if not INITIAL_RUN.exists():
        shutil.copytree(TARGET_RUN, INITIAL_RUN)

    generate_material_input(TARGET_RUN, TARGET_LAYER_PARAMS)
    generate_material_input(INITIAL_RUN, INITIAL_LAYER_PARAMS)


if __name__ == "__main__":
    main()

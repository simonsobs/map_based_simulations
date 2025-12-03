#!/usr/bin/env python3
"""
Estimate disk space for a map-based simulation release.

This script reads the instrument model and configuration files to estimate
the total disk space required for all maps in a release. It calculates sizes
for both HEALPix and CAR (Cylindrical Equal-Area Rectangular) pixelizations.

Usage
-----
    python estimate_disk_space.py <release_folder> [options]

Arguments
---------
release_folder : str
    Path to the release folder containing common.toml and component files.

Options
-------
--combine-maps PATH
    Path to combine_maps.py script. Default: <release_folder>/combine_maps.py
--n-individual N
    Override the number of individual components instead of counting TOML files.
--n-combined N
    Override the number of combined components instead of parsing combine_maps.py.
-q, --quiet
    Only print the total disk space.

Examples
--------
Basic usage with a release folder:
    python estimate_disk_space.py mbs-s0016-20241111

Override component counts for quick estimates:
    python estimate_disk_space.py mbs-s0016-20241111 --n-individual 10 --n-combined 5

Quiet mode for scripting:
    python estimate_disk_space.py mbs-s0016-20241111 -q

Input Files
-----------
The script reads the following files from the release folder:
- common.toml: Configuration file with pixelization settings (healpix, car flags)
- instrument_model/*.tbl: IPAC table with channel parameters (nside, car_resol)
- *.toml: Individual component configuration files (one per sky component)
- combine_maps.py: Script defining combined component dictionaries

Size Calculations
-----------------
HEALPix maps:
    size = 12 * nside^2 * n_components * dtype_bytes
    where n_components=3 (I,Q,U) and dtype_bytes=4 (float32)

CAR maps:
    size = (360*60/resolution) * (180*60/resolution) * n_components * dtype_bytes
    where n_components=3 (I,Q,U) and dtype_bytes=8 (float64)
"""

import argparse
import ast
import glob
import os
import sys
from typing import Dict, List, Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from astropy.table import QTable


def get_healpix_map_size_bytes(nside: int, n_components: int = 3, dtype_bytes: int = 4) -> int:
    """
    Calculate the size of a HEALPix map in bytes.

    Parameters
    ----------
    nside : int
        HEALPix NSIDE parameter
    n_components : int
        Number of Stokes components (typically 3 for I, Q, U)
    dtype_bytes : int
        Bytes per pixel value (4 for float32, 8 for float64)

    Returns
    -------
    int
        Size in bytes
    """
    npix = 12 * nside * nside
    return npix * n_components * dtype_bytes


def get_car_map_size_bytes(resolution_arcmin: float, n_components: int = 3, dtype_bytes: int = 8) -> int:
    """
    Calculate the size of a CAR (Cylindrical Equal-Area Rectangular) map in bytes.

    CAR maps use a rectangular grid covering the full sky:
    - 360 degrees in longitude (RA)
    - 180 degrees in latitude (Dec)

    Parameters
    ----------
    resolution_arcmin : float
        Pixel resolution in arcminutes
    n_components : int
        Number of Stokes components (typically 3 for I, Q, U)
    dtype_bytes : int
        Bytes per pixel value (4 for float32, 8 for float64)
        Default is 8 (float64) as used by pixell/enmap

    Returns
    -------
    int
        Size in bytes
    """
    # CAR maps use a rectangular grid: nx pixels in longitude, ny in latitude
    nx = int(360 * 60 / resolution_arcmin)  # 360 degrees in arcmin
    ny = int(180 * 60 / resolution_arcmin)  # 180 degrees in arcmin
    npix = nx * ny
    return npix * n_components * dtype_bytes


def format_size(size_bytes: int) -> str:
    """Format size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} EB"


def load_common_config(release_folder: str) -> dict:
    """Load the common.toml configuration file."""
    common_toml_path = os.path.join(release_folder, "common.toml")
    if not os.path.exists(common_toml_path):
        raise FileNotFoundError(f"common.toml not found at {common_toml_path}")

    with open(common_toml_path, "rb") as f:
        return tomllib.load(f)


def load_instrument_model(release_folder: str, common_config: dict) -> QTable:
    """Load the instrument model from the path specified in common.toml."""
    instrument_path = common_config.get("instrument_parameters", "")
    if not instrument_path:
        raise ValueError("instrument_parameters not found in common.toml")

    full_path = os.path.join(release_folder, instrument_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Instrument model not found at {full_path}")

    return QTable.read(full_path, format="ascii.ipac")


def count_component_toml_files(release_folder: str) -> List[str]:
    """Count the component TOML files (excluding common.toml)."""
    toml_files = glob.glob(os.path.join(release_folder, "*.toml"))
    components = []
    for f in toml_files:
        basename = os.path.basename(f)
        if basename != "common.toml":
            # Extract tag from TOML file
            with open(f, "rb") as tf:
                config = tomllib.load(tf)
                tag = config.get("tag", basename.replace(".toml", ""))
                components.append(tag)
    return components


def parse_combined_components(combine_maps_path: str) -> Dict[str, List[str]]:
    """
    Parse the combine_maps.py script to extract combined component definitions.

    This function uses AST parsing to extract the dictionary of combined components
    from the combine_maps.py script. It handles:
    - The main all_combined dictionary definition
    - Variable references (e.g., extragalactic list)
    - Dynamic websky variant generation

    Note: The parser assumes the first all_combined assignment contains the complete
    dictionary definition. Subsequent assignments (e.g., filtering for batch jobs)
    are ignored.

    Returns a dictionary mapping combined component names to lists of individual components.
    """
    if not os.path.exists(combine_maps_path):
        return {}

    with open(combine_maps_path, "r") as f:
        source = f.read()

    # Parse the AST to extract the all_combined dictionary
    tree = ast.parse(source)

    combined = {}  # type: Dict[str, any]
    websky_catalog = []  # type: List[str]
    extragalactic = []  # type: List[str]

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Only take the first all_combined assignment (the full dictionary)
                    # as subsequent assignments may filter or replace it for batch processing
                    if target.id == "all_combined" and isinstance(node.value, ast.Dict) and not combined:
                        for key, value in zip(node.value.keys, node.value.values):
                            if isinstance(key, ast.Constant):
                                name = key.value
                                if isinstance(value, ast.List):
                                    components = [
                                        elt.value for elt in value.elts
                                        if isinstance(elt, ast.Constant)
                                    ]
                                    combined[name] = components
                                elif isinstance(value, ast.Name):
                                    # Handle variable references like extragalactic
                                    combined[name] = value.id  # Store the variable name for now
                    elif target.id == "websky_catalog" and isinstance(node.value, ast.List):
                        websky_catalog = [
                            elt.value for elt in node.value.elts
                            if isinstance(elt, ast.Constant)
                        ]
                    elif target.id == "extragalactic" and isinstance(node.value, ast.List):
                        extragalactic = [
                            elt.value for elt in node.value.elts
                            if isinstance(elt, ast.Constant)
                        ]

    # Resolve variable references
    for name, value in combined.items():
        if value == "extragalactic":
            combined[name] = extragalactic

    # Add the websky variants that are generated dynamically in the script
    for name in list(combined.keys()):
        if name.startswith("galactic") and "d1s1" not in name:
            combined[name + "_websky"] = combined[name] + websky_catalog

    return combined


def estimate_disk_space(
    release_folder: str,
    combine_maps_path: Optional[str] = None,
    n_individual_override: Optional[int] = None,
    n_combined_override: Optional[int] = None,
    verbose: bool = True
) -> dict:
    """
    Estimate the disk space for a release.

    Parameters
    ----------
    release_folder : str
        Path to the release folder containing common.toml and component files
    combine_maps_path : str, optional
        Path to the combine_maps.py script. If not provided, looks for it in release_folder
    n_individual_override : int, optional
        Override the number of individual components (instead of counting TOML files)
    n_combined_override : int, optional
        Override the number of combined components (instead of parsing combine_maps.py)
    verbose : bool
        If True, print detailed information

    Returns
    -------
    dict
        Dictionary with space estimates
    """
    # Load configuration
    common_config = load_common_config(release_folder)
    instrument_model = load_instrument_model(release_folder, common_config)

    # Check what pixelizations are enabled
    do_healpix = common_config.get("healpix", True)
    do_car = common_config.get("car", False)

    # Get components
    if n_individual_override is not None:
        individual_components = [f"component_{i+1}" for i in range(n_individual_override)]
    else:
        individual_components = count_component_toml_files(release_folder)

    # Get combined components
    if n_combined_override is not None:
        combined_components = {f"combined_{i+1}": [] for i in range(n_combined_override)}
    else:
        if combine_maps_path is None:
            combine_maps_path = os.path.join(release_folder, "combine_maps.py")
        combined_components = parse_combined_components(combine_maps_path)

    # Count channels
    n_channels = len(instrument_model)

    if verbose:
        print(f"\n{'='*60}")
        print(f"Disk Space Estimation for: {release_folder}")
        print(f"{'='*60}")
        print(f"\nConfiguration:")
        print(f"  HEALPix maps: {do_healpix}")
        print(f"  CAR maps: {do_car}")
        print(f"  Number of channels: {n_channels}")
        print(f"\nIndividual components ({len(individual_components)}):")
        for comp in sorted(individual_components):
            print(f"  - {comp}")
        print(f"\nCombined components ({len(combined_components)}):")
        for name, components in sorted(combined_components.items()):
            print(f"  - {name}: {components}")

    # Calculate space for each channel
    total_healpix_bytes = 0
    total_car_bytes = 0

    healpix_by_nside = {}
    car_by_resolution = {}

    for row in instrument_model:
        nside = int(row["nside"])

        if do_healpix:
            hp_size = get_healpix_map_size_bytes(nside)
            total_healpix_bytes += hp_size
            healpix_by_nside[nside] = healpix_by_nside.get(nside, 0) + hp_size

        if do_car:
            # Handle astropy Quantity objects and missing columns
            if "car_resol" not in instrument_model.colnames:
                raise ValueError("CAR maps enabled but 'car_resol' column not found in instrument model")
            car_resol_val = row["car_resol"]
            car_resol = float(car_resol_val.value if hasattr(car_resol_val, 'value') else car_resol_val)
            car_size = get_car_map_size_bytes(car_resol)
            total_car_bytes += car_size
            car_by_resolution[car_resol] = car_by_resolution.get(car_resol, 0) + car_size

    # Calculate total for all individual components
    n_individual = len(individual_components)
    total_individual_healpix = total_healpix_bytes * n_individual
    total_individual_car = total_car_bytes * n_individual

    # Calculate total for all combined components
    n_combined = len(combined_components)
    total_combined_healpix = total_healpix_bytes * n_combined
    total_combined_car = total_car_bytes * n_combined

    # Grand totals
    grand_total_healpix = total_individual_healpix + total_combined_healpix
    grand_total_car = total_individual_car + total_combined_car
    grand_total = grand_total_healpix + grand_total_car

    if verbose:
        print(f"\n{'='*60}")
        print("Size per channel per component:")
        print(f"{'='*60}")
        if do_healpix:
            print("\nHEALPix by NSIDE:")
            for nside in sorted(healpix_by_nside.keys()):
                size = get_healpix_map_size_bytes(nside)
                count = healpix_by_nside[nside] // size
                print(f"  NSIDE {nside}: {format_size(size)} x {count} channels")
        if do_car:
            print("\nCAR by resolution:")
            for resol in sorted(car_by_resolution.keys()):
                size = get_car_map_size_bytes(resol)
                count = car_by_resolution[resol] // size
                print(f"  {resol}' resolution: {format_size(size)} x {count} channels")

        print(f"\n{'='*60}")
        print("Summary:")
        print(f"{'='*60}")
        print(f"\nPer component (all {n_channels} channels):")
        if do_healpix:
            print(f"  HEALPix: {format_size(total_healpix_bytes)}")
        if do_car:
            print(f"  CAR: {format_size(total_car_bytes)}")
        if do_healpix and do_car:
            print(f"  Total: {format_size(total_healpix_bytes + total_car_bytes)}")

        print(f"\nIndividual components ({n_individual} components):")
        if do_healpix:
            print(f"  HEALPix: {format_size(total_individual_healpix)}")
        if do_car:
            print(f"  CAR: {format_size(total_individual_car)}")
        print(f"  Total: {format_size(total_individual_healpix + total_individual_car)}")

        print(f"\nCombined components ({n_combined} components):")
        if do_healpix:
            print(f"  HEALPix: {format_size(total_combined_healpix)}")
        if do_car:
            print(f"  CAR: {format_size(total_combined_car)}")
        print(f"  Total: {format_size(total_combined_healpix + total_combined_car)}")

        print(f"\n{'='*60}")
        print(f"GRAND TOTAL: {format_size(grand_total)}")
        if do_healpix:
            print(f"  HEALPix total: {format_size(grand_total_healpix)}")
        if do_car:
            print(f"  CAR total: {format_size(grand_total_car)}")
        print(f"{'='*60}\n")

    return {
        "n_channels": n_channels,
        "n_individual_components": n_individual,
        "n_combined_components": n_combined,
        "healpix_enabled": do_healpix,
        "car_enabled": do_car,
        "per_component_healpix_bytes": total_healpix_bytes if do_healpix else 0,
        "per_component_car_bytes": total_car_bytes if do_car else 0,
        "individual_healpix_bytes": total_individual_healpix if do_healpix else 0,
        "individual_car_bytes": total_individual_car if do_car else 0,
        "combined_healpix_bytes": total_combined_healpix if do_healpix else 0,
        "combined_car_bytes": total_combined_car if do_car else 0,
        "total_bytes": grand_total,
        "individual_components": individual_components,
        "combined_components": combined_components,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Estimate disk space for a map-based simulation release.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python estimate_disk_space.py mbs-s0016-20241111
    python estimate_disk_space.py mbs-s0016-20241111 --n-individual 10 --n-combined 5
    python estimate_disk_space.py mbs-s0016-20241111 -q

Input files read from release folder:
  - common.toml: Configuration (healpix/car flags)
  - instrument_model/*.tbl: Channel parameters (nside, car_resol)
  - *.toml: Individual component configs
  - combine_maps.py: Combined component definitions

Size formulas:
  HEALPix: 12 * nside^2 * 3 components * 4 bytes (float32)
  CAR: (360*60/res) * (180*60/res) * 3 components * 8 bytes (float64)
        """
    )
    parser.add_argument(
        "release_folder",
        nargs="?",
        default=None,
        help="Path to the release folder containing common.toml and component files"
    )
    parser.add_argument(
        "--combine-maps",
        dest="combine_maps_path",
        help="Path to combine_maps.py script (default: <release_folder>/combine_maps.py)"
    )
    parser.add_argument(
        "--n-individual",
        type=int,
        default=None,
        help="Override the number of individual components (instead of counting TOML files)"
    )
    parser.add_argument(
        "--n-combined",
        type=int,
        default=None,
        help="Override the number of combined components (instead of parsing combine_maps.py)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Only print the total disk space"
    )

    args = parser.parse_args()

    # If no release folder provided, print help and exit
    if args.release_folder is None:
        parser.print_help()
        sys.exit(0)

    if not os.path.isdir(args.release_folder):
        print(f"Error: {args.release_folder} is not a directory", file=sys.stderr)
        sys.exit(1)

    try:
        result = estimate_disk_space(
            args.release_folder,
            combine_maps_path=args.combine_maps_path,
            n_individual_override=args.n_individual,
            n_combined_override=args.n_combined,
            verbose=not args.quiet
        )
        if args.quiet:
            print(format_size(result["total_bytes"]))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

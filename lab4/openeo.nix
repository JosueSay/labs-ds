{
  pkgs,
  pyPkgs,
}:
pyPkgs.buildPythonPackage rec {
  pname = "openeo";
  version = "0.43.0";
  # format = "";
  pyproject = true;
  build-system = [pyPkgs.setuptools];
  propagatedBuildInputs = let
    xarray = import ./xarray.nix {
      inherit (pkgs) lib fetchFromGitHub;
      inherit (pyPkgs) buildPythonPackage numpy packaging pandas pytestCheckHook pythonOlder setuptools setuptools-scm;
    };
  in [
    pyPkgs.requests
    pyPkgs.urllib3
    pyPkgs.shapely
    pyPkgs.numpy
    # pkgs.python3."11-xarray-2025.04.0"
    # pkgs.python3."11-xarray-2025.04.0"
    # pkgs.python311Packages.xarray
    pyPkgs.pandas
    pyPkgs.pystac
    pyPkgs.deprecated
    xarray
  ];
  src = pkgs.fetchFromGitHub {
    owner = "Open-EO";
    repo = "openeo-python-client";
    rev = "v${version}";
    sha256 = "sha256-zeUASaj1XbcH8NE2+AalH8Jc0tocwotKwJ5QAtrf0kE=";
  };
}

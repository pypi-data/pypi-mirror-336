{ pkgs ? import <nixpkgs> {} }:
with pkgs.python313Packages;

buildPythonPackage rec {
  pname = "logformat";
  version = "git";
  src = ./.;
  pyproject = true;

  build-system = [
    hatchling
  ];

  disabled = pythonOlder "3.13";

  installCheckPhase = ''
    python ${./test_logformat.py}
  '';
}

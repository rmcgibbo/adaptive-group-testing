{ buildPythonPackage
, pytestCheckHook
}:

buildPythonPackage rec {
  pname = "adaptive-group-testing";
  version = "0.1";

  src = ./.;

  checkInputs = [ pytestCheckHook ];
  pytestFlagsArray = [ "adaptive_group_testing.py" ];

}

{

	description = "Manage your Binance account from cli.";

	inputs.nixpkgs.url = "/Users/ihsan/code/github.com/nixos/nixpkgs/";
	inputs.flake-utils.url = "github:numtide/flake-utils";

	outputs = { self, nixpkgs, flake-utils, }:
	flake-utils.lib.eachDefaultSystem (system: let
		pkgs = nixpkgs.legacyPackages.${system};
	in rec {

		binance-cli = {lib, buildPythonApplication, docopt, python-binance}:
			buildPythonApplication rec {
				pname = "binance-cli";
				version = "0.0.1";
				src = lib.cleanSource ./.;
				doCheck = false;
				propagatedBuildInputs = [
					docopt
					python-binance
				];
			};

		defaultPackage = pkgs.python3Packages.callPackage binance-cli {};

		defaultApp = {
			type = "app";
			program = "${self.defaultPackage.${system}}/bin/binance-cli";
		};

	});

}

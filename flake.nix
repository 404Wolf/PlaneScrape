{
  description = "Plane flight tracker";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      poetry2nix,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        name = "planetrack";
        pkgs = import nixpkgs { inherit system; };
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in
      rec {
        packages = {
          default = mkPoetryApplication {
            projectDir = self;
            buildInputs = [
              pkgs.chromedriver
              pkgs.ungoogled-chromium
            ];
            preferWheels = true;
          };
        };

        devShells = {
          default = pkgs.mkShell {
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc.lib.outPath
              pkgs.stdenv.cc.cc.lib
              pkgs.libstdcxx5
              pkgs.zlib
            ];
            packages = [ pkgs.poetry ];
            inputsFrom = [ packages.default ];
          };
          poetry = pkgs.mkShell {
            packages = [
              pkgs.python313
              pkgs.poetry
            ];
            shellHook = ''poetry install'';
          };
        };
      }
    );
}

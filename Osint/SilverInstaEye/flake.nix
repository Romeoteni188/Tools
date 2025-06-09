{
  description = "herramienta para hacer osint";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    {
      devShells.x86_64-linux.default =
        let
          pkgs = import nixpkgs { system = "x86_64-linux"; };
          pythonEnv = pkgs.python3.withPackages (
            ps: with ps; [
              termcolor
              argparse # Aunque ya viene con Python, puedes dejarlo por claridad
              instagrapi
              requests
              beautifulsoup4
              colorama
              googlesearch-python
              Pillow
            ]
          );
        in
        pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.ffmpeg
            pkgs.tk
          ];
        };
    };
}

# cstags
Python script for generating really basic C# tags for Vim (kind of like ctags)

## Usage

To run it for a specific set of files, do:
```sh
python3 cstags.py file1.cs file2.cs file3.cs
```

To run it for all `.cs` files in your project, go to the root directory, and run it without any arguments:
```sh
python3 cstags.py
```

It'll recursively go through all `.cs` files that aren't in any of the excluded directories.

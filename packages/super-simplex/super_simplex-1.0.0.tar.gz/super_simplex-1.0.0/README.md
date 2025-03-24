# Super Simplex

## Description

This is a library dedicated to a Python port of KurtSpencer's Super Simplex Noise implementation.

## Installation

On window:

```sh
pip install super_simplex
```

On Linux:

```sh
pip3 install super_simplex
```

On Mac:

```sh
pip3 install super_simplex
```

## Usage

Generate 2D noise value for 1 seed:

```py
import super_simplex

noise = super_simplex.noise_2d(
    x = 0.1,
    y = 0.1,
    super_simplex.gen_permu(seed = 384714386)
)

print(noise[0])
```

Generate 2D noise value for 2 seed:

```py
import super_simplex

noises = super_simplex.noise_2d(
    x = 0.1,
    y = 0.1,
    [
        super_simplex.gen_permu(seed = 384714386),
        super_simplex.gen_permu(seed = 983475466)
    ]
)

print(noise[0], noise[1])
```

## Credits

All credit goes to Kurt Spencer for the original C# implementation.

# Super Simplex

## Description

This is a library dedicated to a Python port of KurtSpencer's Super Simplex Noise implementation.

## Installation

```sh
pip install super_simplex
```

## Usage

Generate 2D noise value for 1 seed:

```py
import super_simplex

noise = super_simplex.noise_2d(
    x = 0.1,
    y = 0.1,
    perm = super_simplex.gen_permu(seed = 384714386)[0]
)

print(noise[0])
```

Generate 2D noise value for 2 seed using a generator:

```py
import super_simplex

generator = super_simplex.Gener(
    [384714386, 983475466]
)

print(generator.noise_2d(0.1, 0.1))
```

## Credits

All credit goes to Kurt Spencer for the original C# implementation.

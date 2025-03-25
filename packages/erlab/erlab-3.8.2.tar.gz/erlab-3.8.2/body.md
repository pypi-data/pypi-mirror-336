## v3.8.2 (2025-03-25)

### 🐞 Bug Fixes

- **analysis.transform.symmetrize:** fix compatibility with data including NaN ([ce173ce](https://github.com/kmnhan/erlabpy/commit/ce173ce8fc067ee2d9898f89883f7120b9784f47))

- **formatting:** make float formatting use scientific notation for very small values ([83843a0](https://github.com/kmnhan/erlabpy/commit/83843a047c5b38a6e68d92eb2fb430fa744652f7))

- **plugins.erpes:** promote more attributes to coords ([c2c066a](https://github.com/kmnhan/erlabpy/commit/c2c066ae7bc09af69f393c4cf79e00fc925baaf0))

- **dataloader:** allow datetime and callable objects in `additional_coords` ([732288f](https://github.com/kmnhan/erlabpy/commit/732288f585cef6b2b8cff86cb9c35aa9cbaff2dd))

- **imagetool:** update associated coords on show and reload; ensure float64 type for associated coordinates ([1958b80](https://github.com/kmnhan/erlabpy/commit/1958b80e47bac3bb4424733c18d66a4ebfa09668))

- **qsel:** allow passing arrays to simultaneously select multiple indices ([a5c987b](https://github.com/kmnhan/erlabpy/commit/a5c987bca3bd1fd0d3874129c9bc33226716ed8a))

  `DataArray.qsel` now supports collection arguments. For example, actions like `darr.qsel(x=[1, 2, 3], x_width=2)` now works properly.

- **analysis.fit.functions:** allow passing arrays to any argument ([ffe4914](https://github.com/kmnhan/erlabpy/commit/ffe491459c555e05ecde9015559298375aad7347))

### ⚡️ Performance

- **imagetool.manager:** improve server responsiveness (#117) ([255c04f](https://github.com/kmnhan/erlabpy/commit/255c04f7f1950fa06bfd466f0137d3d616a23b8d))

  Changes the internal detection mechanism for running manager instances to be more reliable, along with some server side micro-optimizations.

### ♻️ Code Refactor

- **kspace:** hide progress messages during momentum conversion ([9eab40c](https://github.com/kmnhan/erlabpy/commit/9eab40ce1fa8c1f921c526ef71e943bc3df26aa2))

  Hides the printed messages during momentum conversion by default. The messages can be enabled by passing `silent=False` to `DataArray.kspace.convert`.

- **imagetool.fastslicing:** fix type signature ordering ([a409322](https://github.com/kmnhan/erlabpy/commit/a4093224e60401d8c144d7a3bbe4429f9fe8e5e1))

[main 94881cc] bump: version 3.8.1 → 3.8.2
 3 files changed, 13 insertions(+), 3 deletions(-)


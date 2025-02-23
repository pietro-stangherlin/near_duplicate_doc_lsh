# Parameters to analyze (not time metrics)

## Efficacy

### Collection

- Noise ratio
- (near) duplicates ratio (duplicates / total)

### Shingling

- shingle length

### MinHash

- signature length
- signature hash function
- signature hash function modulo (bits: 32 vs 64)

### LSH

- number of bands
- number of buckets for each band

## Efficiency

### MinHash

- Btree vs SQL
- occupied memory

### LSH

- List vs SQL
- occupied memory
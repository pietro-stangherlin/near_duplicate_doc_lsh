from mrjob.job import MRJob
from mrjob.step import MRStep
from itertools import combinations

def MyHash(x):
    return (x)

class LSH_MR_SIG(MRJob):
    '''In the version identity hash function
    the input is supposed to be a csv file with a id in the first column
    and the already computed bucket ids for each band in every other column.
    Example of one row with 3 bands: 1222, 45, 78, 32
    1222 = document id
    45 = bucket id in the first band
    78 = bucket id in the second band
    32 = bucket id in the third band
    '''

    def steps(self):
        return[MRStep(mapper = self.mapper_to_bucket,
                   reducer = self.reducer_to_bucket),
            MRStep(mapper = self.mapper_from_bucket,
                   combiner = self.combiner_from_bucket,
                   reducer = self.reducer_from_bucket)]

    def mapper_to_bucket(self, _, line):
        t = line.split(',')
        doc_id = int(t[0])

        bucket_ids = t[1:]

        # for each band
        for i in range(len(bucket_ids)):
            band_id = i + 1
            bucket = bucket_ids[i]

            yield (f"{band_id}_{bucket}", doc_id)
            
    def reducer_to_bucket(self, key, value):
        t = tuple(value)
        yield (key, t)

        # resources wise
        if len(t) > 1:
            yield (key, t)
    
    def mapper_from_bucket(self, band_bucket_key, elements):
        '''
        @param band_bucket_key (string) : f"{band_id}_{bucket}"
        @param elements (tuple): tuple of elements in the same bucket (and band)
        '''
        # for each bucket get all possible pairs
        # each pair is the new key and the value is one
        for id1, id2 in combinations(elements, 2):
            if id1 != id2:
                pair_key = (id1, id2) if (id1 < id2) else (id2, id1)
                yield pair_key, band_bucket_key

    def combiner_from_bucket(self, pair_key, band_bucket_value):
        yield pair_key, sum(1 for _ in band_bucket_value)

    def reducer_from_bucket(self, pair_key, band_bucket_value):
        '''
        @param pair_key (tuple): tuple with (id1, id2) of one document, note: id1 < id2
        @param band_bucket_value (None): useless param

        return the pair with the count of common buckets
        '''
        yield pair_key, sum(1 for _ in band_bucket_value)

if __name__ == '__main__':
    LSH_MR_SIG.run()


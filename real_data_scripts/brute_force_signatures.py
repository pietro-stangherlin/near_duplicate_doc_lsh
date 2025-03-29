# try a brute force many vs many signature search
# just to measure the timing and compare it with that of LSH

# open an arbitratry signature database
# without doing anything
# assume the signature collection has 10^5 elements
# then we need (10^5)^2 = 10^10 comparaisons

# assuming 10^(-5) seconds for each signature compar
# we need 10^5 seconds which is about 28 hours...

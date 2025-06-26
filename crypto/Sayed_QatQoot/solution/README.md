# What the oracle does?

The oracle has 2 functions, it allows us to generate primes of the form

$$
s_iM + s_{i+1} = p

$$

Given enough primes of this form, we are able to recover M by solving the approximate divisor problem. as stated here in this paper. https://eprint.iacr.org/2016/215.pdf

Once M is recovered, we can take a look at the second functionality, which generates 2 primes in the same form as above and multiplies them to generate n

$$
n = (s_iM + s_{i + 1})(s_{i + k}M + s_{i+1+k})

$$

If we expand this and take it mod M we get

$$
n \equiv s_{i+1}s_{i+1+k} \mod{M}

$$

Since we are given a, c and we know the equations used in the generator we can set up a polynomial in terms of s_i and solve it under mod, the only unknown is k, local testing shows its usually below 2000, so we can just brute force it (:

#include <cstdint>


/*Code taken from open access paper:
Mikkel Thorup and Yin Zhang,
"Tabulation Based 5-Universal Hashing and Linear Probing",
2010 Proceedings of the Workshop on Algorithm Engineering and Experiments (ALENEX),
pages 62-76
table A.9 */

/* types used */
typedef unsigned int        INT32;
typedef unsigned long long  INT64;

/*extract lower and upper 32 bits from INT64*/

const INT64 LowOnes = (((INT64)1)<<32)-1;
#define LOW(x)  ((x)&LowOnes)
#define HIGH(x) ((x)>>32)

const INT64 Prime = (((INT64)1)<<61) - 1;

/*Computes ax+b mod Prime,
possibly plus 2*Prime,
exploiting the structure of Prime.*/
INT64 MultAddPrime32(INT32 x,INT64 a, INT64 b)
{
    INT64 a0,a1,c0,c1,c;
    a0 = LOW(a)*x;
    a1 = HIGH(a)*x;
    c0 = a0+(a1<<32);
    c1 = (a0>>32)+a1;
    c  = (c0&Prime)+(c1>>29)+b;
    return c;
}

/*CWtrick for 32-bit key x (Prime = 2ˆ61-1)
x: integer to be hashed
A,B,C,D,E random integers
-> return Unsigned 64 bit */
extern "C" {
INT64 CWtrick32to64(INT32 x, INT64 A,
INT64 B, INT64 C, INT64 D, INT64 E)

{
    INT64 h;
    h = MultAddPrime32(MultAddPrime32(
        MultAddPrime32(
        MultAddPrime32(x,A,B),x,C),x,D),x,E);
    h = (h&Prime)+(h>>61);
    if (h>=Prime) h-=Prime;
    return h;
}

}

/*CWtrick for 32-bit key x (Prime = 2ˆ61-1)
x: integer to be hashed
A,B,C,D,E random integers
-> return Unsigned 32 bit */
extern "C" {
INT32 CWtrick32to32(INT32 x, INT64 A,
INT64 B, INT64 C, INT64 D, INT64 E)

{
    INT64 h;
    h = MultAddPrime32(MultAddPrime32(
        MultAddPrime32(
        MultAddPrime32(x,A,B),x,C),x,D),x,E);
    h = (h&Prime)+(h>>61);
    if (h>=Prime) h-=Prime;
    return h & 0xFFFFFFFF;
}

}

/*table A.2*/
/*2-universal hashing for 32-bit key xA and B are random 64-bit numbers*/
extern "C" {
    INT32 Univ2(INT32 x,INT64 A, INT64 B)
    {return (INT32) ((A*x + B) >> 32);}
}
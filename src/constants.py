WINDOWWIDTH = 960
WINDOWHEIGHT = 630

HEADERHEIGHT = 90

BARWIDTH = 40
BARHEIGHT = 520

BRICKWIDTH = 40
BRICKHEIGHT = 20
BRICKCEILING = 210
# height at which bricks begin appearing
ROWSIZE = 22
# number of bricks per row

FPS = 120

# RGB values for colors
GRAY = (141, 139, 141)
RED = (190, 82, 71)
CYAN = (57, 145, 133)
BLACK = (0, 0, 0)
ORANGE = (206, 112, 55)
DARK_YELLOW = (188, 123, 46)
YELLOW = (168, 158, 38)
GREEN = (69, 150, 69)
BLUE = (64, 80, 213)

BRICKCOLORS = [RED, ORANGE, DARK_YELLOW, YELLOW, GREEN, BLUE]

# used to generate unique integer for each brick configuration
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
          223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
          293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
          383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
          463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
          569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
          647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
          743]
import sys


def print_row(s, m, n):
    sp = ' '*s
    if sp:
        sys.stdout.write(' '*s)
    for i in range(m):
        sys.stdout.write(str((i+n)%10))
    sys.stdout.write('\n')


def diamond(n=3):
    for i in range(-n+1, n):
        s = abs(i)
        m = 2*(n-s) - 1
        print_row(s, m, n)


if __name__ == "__main__":
    diamond()

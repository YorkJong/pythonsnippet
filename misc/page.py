def numPages(n):
    """Return two array of page number for a booklet printing
    Inputs:
        n - total pages
        
    Example:
    >>> numPages(11)
    (array([12,  1, 10,  3,  8,  5]), array([ 2, 11,  4,  9,  6,  7]))
    """
    N = (n+(4-1))/4*4
    h = range(1, N/2+1, 1) # head
    t = range(N, N/2, -1)  # tail

    import numpy as np
    even = np.array(zip(h,t))[np.arange(N/2)%2==1].flatten()
    odd  = np.array(zip(t,h))[np.arange(N/2)%2==0].flatten()
    return odd, even


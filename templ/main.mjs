function fibonachii(n) {
    if (n <= 1) {
        return n;
    }
    return fibonachii(n - 1) + fibonachii(n - 2);
}


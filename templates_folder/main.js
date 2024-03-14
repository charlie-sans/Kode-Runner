function fibonachii(n) {
    if (n <= 1) {
        return n;
    }
    return fibonachii(n - 1) + fibonachii(n - 2);
}

console.log(fibonachii(10));

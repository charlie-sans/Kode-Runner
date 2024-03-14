function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

function main() {
  document.getElementById("fibonacci").innerHTML = fibonacci(10);
  document.getElementById("fibonacci2").innerHTML = fibonacci(20);
  document.getElementById("fibonacci3").innerHTML = fibonacci(30);
  document.getElementById("fibonacci4").innerHTML = fibonacci(40);
  document.getElementById("fibonacci5").innerHTML = fibonacci(50);
}
main();
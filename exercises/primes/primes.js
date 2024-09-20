/* jshint esversion: 8 */
/* jshint node: true */
/* jshint browser: true */
'use strict';


/**
 * Greet user by name
 * 
 * @param {string} name visitor's name
 * @param {string} selector element to use for display
 */
function greet(name, selector) {
  const greetingElement = document.querySelector(selector);
  greetingElement.textContent = `Hello ${name || 'student'}`;
}

/**
 * Check if a number is prime
 * 
 * @param {number} number number to check
 * @return {boolean} result of the check
 */
function isPrime(number) {
  if (number < 2) return false;
  for (let i = 2; i <= Math.sqrt(number); i++) {
      if (number % i === 0) return false;
  }
  return true;}


/**
 * Print whether a number is prime
 * 
 * @param {number} number number to check
 * @param {string} selector element to use for display
 */
function printNumberInfo(number, selector) {
  const numberInfoElement = document.querySelector(selector);
  const primeMessage = isPrime(number) ? `${number} is a prime number` : `${number} is not a prime number`;
  numberInfoElement.textContent = primeMessage;
}

/**
 * Generate an array of prime numbers
 * 
 * @param {number} number number of primes to generate
 * @return {number[]} an array of `number` prime numbers
 */
function getNPrimes(number) {
  const primes = [];
  let candidate = 2;
  
  while (primes.length < number) {
      if (isPrime(candidate)) {
          primes.push(candidate);
      }
      candidate++;
  }
  
  return primes;
}

/**
 * Print a table of prime numbers
 * 
 * @param {number} number number of primes to display
 * @param {string} selector element to use for display
 */
function printNPrimes(number, selector) {
  const primes = getNPrimes(number);
  const tableBody = document.querySelector(`${selector} tbody`);
  tableBody.innerHTML = '';

  primes.forEach(prime => {
      const row = document.createElement('tr');
      const cell = document.createElement('td');
      cell.textContent = prime;
      row.appendChild(cell);
      tableBody.appendChild(row);
  });
}

/**
 * Display warning about missing URL query parameters
 * 
 * @param {Object} urlParams URL parameters
 * @param {string} selector element to use for display
 */
function displayWarnings(urlParams, selector) {
  const warningElement = document.querySelector(selector);
  warningElement.style.display = 'none';

  if (!urlParams.get('name') || !urlParams.get('number')) {
      warningElement.style.display = 'block';
      warningElement.textContent = 'Warning: Missing URL parameters. Default values are used.';
  }
}

window.onload = function () {
    // TODO: Initialize the following variables
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get('name') || 'student';
    const number = parseInt(urlParams.get('number')) || 330;
    
    this.displayWarnings(urlParams, "#warnings");
    greet(name, "#greeting");
    printNumberInfo(number, "#numberInfo");
    printNPrimes(number, "table#nPrimes");
};

document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
      const $notification = $delete.parentNode;
  
      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    });
  });
  
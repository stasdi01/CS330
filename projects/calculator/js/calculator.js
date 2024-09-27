/* jshint esversion: 8 */
/* jshint browser: true */
'use strict';

var outputScreen;
var clearOnEntry;


/**
 * Display a digit on the `outputScreen`
 * 
 * @param {number} digit digit to add or display on the `outputScreen`
 */
function enterDigit(digit) {
    if (clearOnEntry){
        outputScreen.textContent = "";
        clearOnEntry = false;
    }
    if (outputScreen.textContent === "0" && digit !== "."){
        outputScreen.textContent = digit;
    }
    else{
        outputScreen.textContent += digit;
    }
}


/**
 * Clear `outputScreen` and set value to 0
 */
function clear_screen() {
    clearOnEntry = true;
    outputScreen.textContent = "0";
}


/**
 * Evaluate the expression and display its result or *ERROR*
 */
function eval_expr() {
    try{
        outputScreen.textContent = eval(outputScreen.textContent);
    }catch(error){
        outputScreen.textContent = "ERROR"
    }
    clearOnEntry = true;
}


/**
 * Display an operation on the `outputScreen`
 * 
 * @param {string} operation to add to the expression
 */
function enterOp(operation) {
    if (clearOnEntry){
        outputScreen.textContent = ""
        clearOnEntry = false;
    }
    outputScreen.textContent += operation
}


window.onload = function () {
    outputScreen = document.querySelector("#result");
    clearOnEntry = true;
    clear_screen()
};

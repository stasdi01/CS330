'use strict';

/**
 * Retrieve trivia about numbers one-by-one
 * 
 * @param {number} num base number
 * @param {Object} all_numbers DOM element to append to
 */
async function get_individual(num, all_numbers) {
    all_numbers.innerHTML = '';
    try {
        for (let i = num - 1; i <= num + 1; i++) {
            let response = await fetch(`http://numbersapi.com/${i}?json`);
            let data = await response.json();
            displayTrivia(i, data.text, all_numbers);
        }
    } catch (error) {
        console.error("Error fetching individual number trivia:", error);
    }

}

/**
 * Retrieve trivia about all numbers at once
 * 
 * @param {number} num base number
 * @param {Object} all_numbers DOM element to append to
 */
async function get_batch(num, all_numbers) {
    all_numbers.innerHTML = '';
    try {
        let response = await fetch(`http://numbersapi.com/${num-1},${num},${num+1}?json`);
        let data = await response.json();
        for (let i = num - 1; i <= num + 1; i++) {
            displayTrivia(i, data[i], all_numbers);
        }
    } catch (error) {
        console.error("Error fetching batch number trivia:", error);
    }

}

/**
 * Retrieve information about numbers
 */
async function clickedon() {
    let num = parseInt(document.querySelector("#number").value);
    let all_numbers = document.querySelector("#number_info");
    if (document.querySelector("#batch").checked) {
        get_batch(num, all_numbers);
    } else {
        get_individual(num, all_numbers);
    }
}

/* jshint esversion: 8 */
/* jshint browser: true */
"use strict;";

var team = ["Aardvark", "Beaver", "Cheetah", "Dolphin", "Elephant", "Flamingo", "Giraffe", "Hippo"];
var priority = ["Low", "Normal", "Important", "Critical"];

/**
 * Add a new task to the list
 * 
 * Validate form, collect input values, and add call `addRow` to add a new row to the table
 */
function addTask() {
    // TODO: Implement this function
    let title = document.getElementById("title").value;
    let dueDate = document.getElementById("dueDate").value;
    let feebackMessage = document.getElementById("feedbackMessage");

    if ((!title && !dueDate) || (!dueDate) || (!title)){
        feebackMessage.textContent = "Fill out title and due date";
        feebackMessage.style.display = "block";
        return;
    }
    feebackMessage.style.display = "none";

    let assignedTo = document.getElementById("assignedTo").value;
    let priority = document.getElementById("priority").value;

    let taskList = [title, assignedTo, priority, dueDate];
    addRow(taskList, document.getElementById("taskList").querySelector("tbody"));

}

/**
 * Add a new row to the table
 * 
 * @param {string[]} valueList list of task attributes
 * @param {Object} parent DOM node to append to
 */
function addRow(valueList, parent) {
    let row = document.createElement("tr");
    let td = document.createElement("td");
    let cb = document.createElement("input");
    
    cb.type = "checkbox";
    cb.onclick = removeRow;
    td.appendChild(cb);
    row.appendChild(td);

    valueList.forEach(value => {
        let data = document.createElement("td");
        data.textContent = value;
        row.appendChild(data);
    });
    
    // Assign the priority class based on the priority value
    row.classList.add(valueList[2].toLowerCase());

    parent.appendChild(row);
}

/**
 * Remove a table row corresponding to the selected checkbox
 * 
 * https://stackoverflow.com/questions/26512386/remove-current-row-tr-when-checkbox-is-checked
 */
function removeRow() {
    // TODO: Implement this function
    let row = this.closest("tr");
    row.parentNode.removeChild(row);
}

/**
 * Remove all table rows
 * 
 */
function selectAll() {
    let tbody = document.querySelector("#taskList tbody");

    // Clear all rows in the tbody
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }
}

/**
 * Add options to the specified element
 * 
 * @param {string} selectId `select` element to populate
 * @param {string[]} sList array of options
 */
function populateSelect(selectId, sList) {
    // TODO: Implement this function
    let sel = document.getElementById(selectId, sList);
    sList.forEach(function(item) {
        let option = document.createElement("option");
        option.textContent = item;
        option.value = item;
        sel.appendChild(option);
    });
}

window.onload = function () {
    populateSelect("assignedTo", team);
    populateSelect("priority", priority);
};

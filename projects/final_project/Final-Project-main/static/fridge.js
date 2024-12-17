function toggleNumberInputsFridge() {
    const checkbox = document.getElementById("numberCheckbox");
    const numberInputs = document.getElementById("numberInputs");
    if (checkbox.checked) {
        numberInputs.style.display = "block";
    } else {
        numberInputs.style.display = "none";
    }
}


function toggleSizeInputsFridge() {
    const checkbox = document.getElementById("sizeCheckbox");
    const sizeInputs = document.getElementById("sizeInputs");
    if (checkbox.checked) {
        sizeInputs.style.display = "block";
    } else {
        sizeInputs.style.display = "none";
    }
}


function toggleWeightInputsFridge() {
    const checkbox = document.getElementById("weightCheckbox");
    const weightInputs = document.getElementById("weightInputs");
    if (checkbox.checked) {
        weightInputs.style.display = "block";
    } else {
        weightInputs.style.display = "none";
    }
}


function toggleLiquidInputsFridge() {
    const checkbox = document.getElementById("liquidCheckbox");
    const liquidInputs = document.getElementById("liquidInputs");
    if (checkbox.checked) {
        liquidInputs.style.display = "block";
    } else {
        liquidInputs.style.display = "none";
    }
}
function toggleNumberInputsFridge() {
    document.getElementById("numberInputs").style.display =
        document.getElementById("numberCheckbox").checked ? "block" : "none";
}


function convertSizeFridge() {
    const sizeInch = parseFloat(document.getElementById("sizeInch").value) || 0;
    const sizeCm = parseFloat(document.getElementById("sizeCm").value) || 0;

    if (document.activeElement.id === "sizeInch" && sizeInch > 0) {
        const resultCm = (sizeInch * 2.54).toFixed(2);
        document.getElementById("cmOutput").innerText = `${resultCm} cm`;
    } else if (document.activeElement.id === "sizeCm" && sizeCm > 0) {
        const resultInch = (sizeCm / 2.54).toFixed(2);
        document.getElementById("inchOutput").innerText = `${resultInch} inches`; 
    }

    
    if (sizeInch > 0) {
        const resultCm = (sizeInch * 2.54).toFixed(2);
        document.getElementById("inchOutput").innerText = `${sizeInch} inches / ${resultCm} cm`;
        document.getElementById("cmOutput").innerText = "";  
    } else if (sizeCm > 0) {
        const resultInch = (sizeCm / 2.54).toFixed(2);
        document.getElementById("cmOutput").innerText = `${sizeCm} cm / ${resultInch} inches`;
        document.getElementById("inchOutput").innerText = ""; 
    } else {
        document.getElementById("inchOutput").innerText = "";  
        document.getElementById("cmOutput").innerText = "";  
    }
}


function convertWeight() {
    const weightKg = parseFloat(document.getElementById("weightKg").value) || 0;
    const weightLb = parseFloat(document.getElementById("weightLb").value) || 0;

    if (document.activeElement.id === "weightKg" && weightKg > 0) {
        const resultLb = (weightKg * 2.20462).toFixed(2);
        document.getElementById("lbOutput").innerText = `${resultLb} lbs`;  
    } else if (document.activeElement.id === "weightLb" && weightLb > 0) {
        const resultKg = (weightLb / 2.20462).toFixed(2);
        document.getElementById("kgOutput").innerText = `${resultKg} kg`;  
    }

   
    if (weightKg > 0) {
        const resultLb = (weightKg * 2.20462).toFixed(2);
        document.getElementById("kgOutput").innerText = `${weightKg} kg / ${resultLb} lbs`;
        document.getElementById("lbOutput").innerText = ""; 
    } else if (weightLb > 0) {
        const resultKg = (weightLb / 2.20462).toFixed(2);
        document.getElementById("lbOutput").innerText = `${weightLb} lbs / ${resultKg} kg`;
        document.getElementById("kgOutput").innerText = "";  
    } else {
        document.getElementById("kgOutput").innerText = "";  
        document.getElementById("lbOutput").innerText = "";  
    }
}
function convertLiquid() {
    const liquidGallon = parseFloat(document.getElementById("liquidGallon").value) || 0;
    const liquidLiter = parseFloat(document.getElementById("liquidLiter").value) || 0;

   
    if (document.activeElement.id === "liquidGallon" && liquidGallon > 0) {
        const resultLiter = (liquidGallon * 3.78541).toFixed(2);
        document.getElementById("literOutput").innerText = `${resultLiter} liter`; 
    } else if (document.activeElement.id === "liquidLiter" && liquidLiter > 0) {
        const resultGallon = (liquidLiter / 3.78541).toFixed(2);
        document.getElementById("gallonOutput").innerText = `${resultGallon} gallon`;  
    }

    
    if (liquidGallon > 0) {
        const resultLiter = (liquidGallon * 3.78541).toFixed(2);
        document.getElementById("gallonOutput").innerText = `${liquidGallon} gallon / ${resultLiter} liters`;  // Both displayed
        document.getElementById("literOutput").innerText = ""; 
    } else if (liquidLiter > 0) {
        const resultGallon = (liquidLiter / 3.78541).toFixed(2);
        document.getElementById("literOutput").innerText = `${liquidLiter} liters / ${resultGallon} gallon`;  // Both displayed
        document.getElementById("gallonOutput").innerText = ""; 
    } else {
        document.getElementById("gallonOutput").innerText = "";  
        document.getElementById("literOutput").innerText = ""; 
    }
}

function searchItemsFridge() {
    const query = document.getElementById("searchInput").value.trim();
    const resultsDiv = document.getElementById("searchResults");
    const dynamicBox = document.getElementById("dynamicBox");

    if (query.length === 0) {
        resultsDiv.innerHTML = "<p>Please type something to search...</p>";
        dynamicBox.style.transition = "all 1s ease";
        dynamicBox.classList.add("expanded-box");
        dynamicBox.classList.remove("collapsed-box");
        return;
    }

    fetch(`/fridge/search_items_fridge?q=${encodeURIComponent(query)}`)
        .then((response) => {
            console.log("Response Status:", response.status); // Debugging log
            return response.json();
        })
        .then((data) => {
            console.log("Search Results:", data); // Debugging log
            resultsDiv.innerHTML = ""; 
            if (Object.keys(data).length === 0) {
                resultsDiv.innerHTML = `<p>No matching items found for "${query}".</p>`;
            } else {
                for (const [keyword, types] of Object.entries(data)) {
                    if (types.length > 0) {
                        types.forEach((type) => {
                            resultsDiv.innerHTML += `
                                <div class="form-check">
                                    <input type="checkbox" class="form-check-input" name="item_name" value="${keyword} (${type})">
                                    <label class="form-check-label">${keyword} (${type})</label>
                                </div>`;
                        });
                    } else {
                        resultsDiv.innerHTML += `
                            <div class="form-check">
                                <input type="checkbox" class="form-check-input" name="item_name" value="${keyword}">
                                <label class="form-check-label">${keyword}</label>
                            </div>`;
                    }
                }
            }
            dynamicBox.style.transition = "all 1s ease"; 
            dynamicBox.classList.add("expanded-box");
            dynamicBox.classList.remove("collapsed-box");
        })
        .catch((err) => console.error("Error fetching items:", err));
}

document.getElementById("addItemForm").addEventListener("submit", function (e) {
    let hasError = false;

    
    const itemName = document.getElementById("item_name").value.trim();
    const itemNameError = document.getElementById("itemNameError");
    if (!itemName) {
        itemNameError.textContent = "Item name is required.";
        itemNameError.style.display = "block";
        hasError = true;
    } else {
        itemNameError.style.display = "none";
    }

    // Validate quantity type
    const quantityType = document.querySelector('input[name="quantityType"]:checked');
    const quantityTypeError = document.getElementById("quantityTypeError");
    if (!quantityType) {
        quantityTypeError.textContent = "Please select a quantity type.";
        quantityTypeError.style.display = "block";
        hasError = true;
    } else {
        quantityTypeError.style.display = "none";

        
        if (quantityType.value === "number") {
            const number = document.getElementById("number").value.trim();
            const numberError = document.getElementById("numberError");
            if (!number || isNaN(number) || parseInt(number) <= 0) {
                numberError.textContent = "Please enter a valid number of items.";
                numberError.style.display = "block";
                hasError = true;
            } else {
                numberError.style.display = "none";
            }
        }
    }

    
    if (hasError) {
        e.preventDefault();
    }
});
document.getElementById("addItemForm").addEventListener("submit", function (e) {
    let hasError = false;
    let errorMessage = "";


    const selectedItem = document.querySelector('input[name="item_name"]:checked');
    if (!selectedItem) {
        errorMessage += "Please select an item from the search results.\n";
        hasError = true;
    }


    const quantityType = document.querySelector('input[name="quantityType"]:checked');
    if (!quantityType) {
        errorMessage += "Please select a quantity type.\n";
        hasError = true;
    } else {
        
        if (quantityType.value === "number") {
            const number = document.getElementById("number")?.value.trim();
            if (!number || isNaN(number) || parseInt(number) <= 0) {
                errorMessage += "Please enter a valid number of items.\n";
                hasError = true;
            }
        } else if (quantityType.value === "size") {
            const sizeInch = document.getElementById("sizeInch")?.value.trim();
            const sizeCm = document.getElementById("sizeCm")?.value.trim();
            if (!sizeInch && !sizeCm) {
                errorMessage += "Please specify size in inches or centimeters.\n";
                hasError = true;
            }
        } else if (quantityType.value === "weight") {
            const weightKg = document.getElementById("weightKg")?.value.trim();
            const weightLb = document.getElementById("weightLb")?.value.trim();
            if (!weightKg && !weightLb) {
                errorMessage += "Please specify weight in kilograms or pounds.\n";
                hasError = true;
            }
        } else if (quantityType.value === "liquid") {
            const liquidGallon = document.getElementById("liquidGallon")?.value.trim();
            const liquidLiter = document.getElementById("liquidLiter")?.value.trim();
            if (!liquidGallon && !liquidLiter) {
                errorMessage += "Please specify liquid quantity in gallons or liters.\n";
                hasError = true;
            }
        }
    }

    
    if (hasError) {
        alert(errorMessage); 
        e.preventDefault();
    }
});


class CustomSelect {
    constructor(originalSelect) {
        this.originalSelect = originalSelect;
        this.customSelect = document.createElement("div");
        this.customSelect.classList.add("select");
        this.arraySelectedDivs = []
    
        this.originalSelect.querySelectorAll("option").forEach((optionElement) => {
            const itemElement = document.createElement("div");
    
            itemElement.classList.add("select__item");
            itemElement.textContent = optionElement.textContent;
            this.customSelect.appendChild(itemElement);
    
            if (optionElement.selected) {
                this._select(itemElement);
            }
  
            itemElement.addEventListener("click", () => {
            if (
                this.originalSelect.multiple &&
                itemElement.classList.contains("select__item--selected")
            ) {
                this._deselect(itemElement);
            } else {
                this._select(itemElement);
            }

            });
        });
  
        this.originalSelect.insertAdjacentElement("afterend", this.customSelect);
        this.originalSelect.style.display = "none";
    }
  
    _select(itemElement) {
      const index = Array.from(this.customSelect.children).indexOf(itemElement);
  
        if (!this.originalSelect.multiple) {
            this.customSelect.querySelectorAll(".select__item").forEach((el) => {
            el.classList.remove("select__item--selected");
            });
        }
    
        this.originalSelect.querySelectorAll("option")[index].selected = true;
        itemElement.classList.add("select__item--selected");
    }
  
    _deselect(itemElement) {
        const index = Array.from(this.customSelect.children).indexOf(itemElement);
    
        this.originalSelect.querySelectorAll("option")[index].selected = false;
        itemElement.classList.remove("select__item--selected");
    }
}

new CustomSelect(document.querySelector(".custom-select"));

document.querySelector("#ready2").addEventListener("click", () => {
    var selected = []
    var wells = []
    for (var option of document.querySelector(".custom-select").options) {
	wells.push(Number(option.selected))
        if (option.selected) {
            selected.push(option.value);
        }
    }
    alert(selected);
    alert(wells);

    const url = 'http://192.168.1.170:5000/page3'
    fetch(url, {
    	method: "POST",
	body: JSON.stringify(wells)
    })
})

const length = document.querySelector('select').length;
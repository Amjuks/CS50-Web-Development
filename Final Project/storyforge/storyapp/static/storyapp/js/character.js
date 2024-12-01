import { setupImagePreview } from "./image_preview.js";

const elements = {
    traitsContainer: null,
    traitsList: null,
    hiddenTraits: null,
    newTraitInput: null,
    newTraitBtn: null,
};

const data = {"traits": {}};

function traitUpdate(traitInput) {
    let trait = traitInput.getAttribute('data-trait');
    data.traits[trait] = traitInput.value;

    traitInput.addEventListener('input', () => {
        console.log("input");
        console.log(traitInput.value);

        data.traits[trait] = traitInput.value;
        updateTraitInput(elements.hiddenTraits);
    })
}

function updateTraitInput(hiddenInput) {
    hiddenInput.value = JSON.stringify(data);
}

function activateDelete(button) {
    const trait = button.parentElement.parentElement;
    const traitName = trait.children[1].getAttribute('data-trait');

    button.addEventListener('click', () => {
        delete data.traits[traitName];
        updateTraitInput(elements.hiddenTraits);
        trait.remove();
    })
}

function addNewTrait(input, button) {
    button.addEventListener('click', () => {
        const trait = input.value;
        if (!trait) { return; }

        console.log(trait);
        const newElement = `
        <div class="trait">
            <label for="char${trait}">${ trait[0].toUpperCase() + trait.slice(1) }</label>
            <input type="text" value="" name="trait" data-trait="${trait}">
            <button type="button"><i class="fa fa-trash"></i></button>
        </div>`;

        elements.traitsContainer.innerHTML += newElement;
        const traitInput = elements.traitsContainer.querySelector(`input[data-trait="${trait}"]`);
        traitUpdate(traitInput);
        traitInput.dispatchEvent(new Event('input'));
        input.value = null;
    })
}

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('charImage');
    const fileInputButton = document.getElementById('fileInputButton');
    const charPreview = document.getElementById('charPreview');
    
    elements.traitsContainer = document.querySelector('.traits');
    elements.traitsList = document.querySelectorAll('.trait input[name="trait"]');
    elements.hiddenTraits = document.getElementById('hiddenTraits');
    elements.newTraitBtn = document.getElementById('newTraitBtn');
    elements.newTraitInput = document.getElementById('newTraitInput');

    setupImagePreview(fileInput, fileInputButton, charPreview);

    elements.traitsList.forEach(traitEL => {
        traitUpdate(traitEL);
    })

    updateTraitInput(elements.hiddenTraits);
    addNewTrait(elements.newTraitInput, elements.newTraitBtn);

    document.querySelectorAll('.trait .delete-trait').forEach(deleteBtn => activateDelete(deleteBtn));
})
const elements = {
    allRelations: null,
    relationSelect: null,
}

function createNewRelationHTML(relationType, relatedCharacter) {
    const newElement = document.createElement('div');
    newElement.classList.add('relation');
    newElement.innerHTML = `
    <input type="text" name="relation-type" value="${ relationType }">
    <i class="fa-solid fa-right-long"></i>`;
    const newSelect = elements.relationSelect.cloneNode(true);
    const selectedChar = newSelect.querySelector(`option[value="${relatedCharacter.value}"]`);

    newSelect.name = 'relation-character';
    selectedChar.selected = true;
    newElement.appendChild(newSelect);

    elements.allRelations.appendChild(newElement);
}

document.addEventListener('DOMContentLoaded', () => {
    const relationButton = document.getElementById('newRelationBtn');
    const relationTypeInput = document.getElementById('newRelationInput');
    elements.relationSelect = document.getElementById('relationSelect');
    elements.allRelations = document.querySelector('.all-relations');

    relationButton.addEventListener('click', () => {
        const relationType = relationTypeInput.value.trim();
        const relatedCharacter = elements.relationSelect.options[elements.relationSelect.selectedIndex];

        if (!(relationType && relatedCharacter.value !== "-1")) { return; }

        createNewRelationHTML(relationType, relatedCharacter);
        relationTypeInput.value = "";
        relatedCharacter.selected = false;
        elements.relationSelect.firstChild.selected = true;
    })

    document.querySelectorAll('.relation .delete-trait').forEach(deleteBtn => {
        deleteBtn.addEventListener('click', () => {
            deleteBtn.parentNode.parentNode.remove();
        })
    })
})
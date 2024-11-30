import { setupImagePreview } from "./image_preview.js";

const elements = {
    objectivesContainer: null,
    objectivesList: null,
    hiddenObjectives: null,
    newObjectiveInput: null,
    newObjectiveBtn: null,
};

const data = {"objectives": []};

function objectiveUpdate(objectiveInput) {
    let objective = objectiveInput.value;
    data.objectives.push(objective);

    objectiveInput.addEventListener('input', () => {
        updateObjectiveInput(elements.hiddenObjectives);
    })
}

function updateObjectiveInput(hiddenInput) {
    console.log(data);
    hiddenInput.value = JSON.stringify(data.objectives);
}

function activateDelete(button) {
    const objective = button.parentElement.parentElement;
    const objectiveText = objective.children[0].value.trim();

    button.addEventListener('click', () => {
        data.objectives = data.objectives.filter(item => item !== objectiveText);
        console.log("After deleting");
        console.log(data.objectives);
        updateObjectiveInput(elements.hiddenObjectives);
        objective.remove();
    })
}

function addNewObjective(input, button) {
    button.addEventListener('click', () => {
        const objective = input.value;
        if (!objective) { return; }

        const newElement = `
        <div class="objective">
            <input type="text" value="${ objective }" name="objective">
            <button type="button"><i class="fa fa-trash delete-objective"></i></button>
        </div>`;

        elements.objectivesContainer.innerHTML += newElement;
        const newObjective = elements.objectivesContainer.lastChild;
        const objectiveInput = newObjective.querySelector('input');
        const deleteBtn = newObjective.querySelector('.delete-objective');

        objectiveUpdate(objectiveInput);
        objectiveInput.dispatchEvent(new Event('input'));
        input.value = null;
        activateDelete(deleteBtn);
    })
}

document.addEventListener('DOMContentLoaded', () => {
    elements.objectivesContainer = document.querySelector('.objectives');
    elements.objectivesList = document.querySelectorAll('.objective input[name="objective"]');
    elements.hiddenObjectives = document.getElementById('hiddenObjectives');
    elements.newObjectiveBtn = document.getElementById('newObjectiveBtn');
    elements.newObjectiveInput = document.getElementById('newObjectiveInput');

    elements.objectivesList.forEach(objectiveEL => {
        objectiveUpdate(objectiveEL);
    })

    updateObjectiveInput(elements.hiddenObjectives);
    addNewObjective(elements.newObjectiveInput, elements.newObjectiveBtn);

    document.querySelectorAll('.delete-objective').forEach(deleteBtn => activateDelete(deleteBtn));
})
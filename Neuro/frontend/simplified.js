// Ensure these variables are defined somewhere in your code
const rgbButton = document.getElementById("rgb-bt");
const modelDropdown = document.getElementById("fruits");

// Car control buttons
const carControlButtons = {
    up: document.querySelector(".car-control .control.up"),
    down: document.querySelector(".car-control .control.down"),
    left: document.querySelector(".car-control .control.left"),
    right: document.querySelector(".car-control .control.right")
};

// Gimbal control buttons
const gimbalControlButtons = {
    up: document.querySelector(".gimbal-control .control.up"),
    down: document.querySelector(".gimbal-control .control.down"),
    left: document.querySelector(".gimbal-control .control.left"),
    right: document.querySelector(".gimbal-control .control.right")
};

// Check if the RGB button exists
if (rgbButton) {
    rgbButton.addEventListener('click', () => {
        // Send RGB image event logic here
        console.log('Saving picture (RGB)');
        robothubApi.notify("RGB", {});
    });
} else {
    console.error('RGB button is not defined in HTML');
}

// Check if the model dropdown exists
if (modelDropdown) {
    modelDropdown.addEventListener('change', () => {
        const selectedModel = modelDropdown.value;
        console.log(`Model selected: ${selectedModel}`);
        robothubApi.notify("model_change", { model: selectedModel });
    });
} else {
    console.error('Model dropdown is not defined in HTML');
}

// Add event listeners for car control buttons
if (carControlButtons.up) {
    carControlButtons.up.addEventListener('click', () => {
        console.log('Car moving up');
        robothubApi.notify("car_control", { action: "up" });
    });
}
if (carControlButtons.down) {
    carControlButtons.down.addEventListener('click', () => {
        console.log('Car moving down');
        robothubApi.notify("car_control", { action: "down" });
    });
}
if (carControlButtons.left) {
    carControlButtons.left.addEventListener('click', () => {
        console.log('Car moving left');
        robothubApi.notify("car_control", { action: "left" });
    });
}
if (carControlButtons.right) {
    carControlButtons.right.addEventListener('click', () => {
        console.log('Car moving right');
        robothubApi.notify("car_control", { action: "right" });
    });
}

// Add event listeners for gimbal control buttons
if (gimbalControlButtons.up) {
    gimbalControlButtons.up.addEventListener('click', () => {
        console.log('Gimbal moving up');
        robothubApi.notify("gimbal_control", { action: "up" });
    });
}
if (gimbalControlButtons.down) {
    gimbalControlButtons.down.addEventListener('click', () => {
        console.log('Gimbal moving down');
        robothubApi.notify("gimbal_control", { action: "down" });
    });
}
if (gimbalControlButtons.left) {
    gimbalControlButtons.left.addEventListener('click', () => {
        console.log('Gimbal moving left');
        robothubApi.notify("gimbal_control", { action: "left" });
    });
}
if (gimbalControlButtons.right) {
    gimbalControlButtons.right.addEventListener('click', () => {
        console.log('Gimbal moving right');
        robothubApi.notify("gimbal_control", { action: "right" });
    });
}

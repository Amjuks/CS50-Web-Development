// convert normal text "To Title Text"
function toTitle(str) {
    return str.replace(/\b\w/g, char => char.toUpperCase());
}

// check if image url is valid
isImageURL = (url) => {
    return (url.match(/\.(jpeg|jpg|gif|png)$/) != null);
}

// check if image url can load and exists
isValidImage = (url) => {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = url;
    })
}

// map of category and colors
const categoryColors = {
    "Electronics": "#FF6600",
    "Fashion": "#20B2AA",
    "Home": "#0000FF",
    "Garden": "#00FFFF",
    "Health": "#800080",
    "Beauty": "#A7FFFE",
    "Sports": "#CC99FF",
    "Outdoors": "#00FFFF",
    "Books": "#FFA500",
    "Media": "#00FF00",
    "Toys": "#008080",
    "Games": "#A52A2A",
    "Automotive": "#0000FF",
    "Pets": "#808000",
    "Accessories": "#800000"
};

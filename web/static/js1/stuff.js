const b2by3 = document.querySelector('#b2by3');
const b3by4 = document.querySelector('#b3by4');
const b4by6 = document.querySelector('#b4by6');
const ready = document.getElementById('ready');

ready.onclick = function(e) {
    e.preventDefault();

    ready.classList.replace("d-inline", "d-none");
    b2by3.classList.replace("d-none", "d-inline");
    b3by4.classList.replace("d-none", "d-inline");
    b4by6.classList.replace("d-none", "d-inline");
}; 

b2by3.onclick = function(e) {
    //fetch('test')
    //	.then(response => console.log(response.body));
}

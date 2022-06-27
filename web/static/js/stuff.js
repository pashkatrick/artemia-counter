var count = document.getElementById('count');
var save = document.getElementById('save');
var edit = document.getElementById('edit');

const count2 = document.querySelector('#count2');
const save2 = document.querySelector('#save2');
const edit2 = document.querySelector('#edit2');

count2.onclick = function(e) {
    e.preventDefault();

    if (save2.style.visibility == 'visible' && edit2.style.visibility == 'visible') {
        count2.innerHTML = 'Count'
        save2.style.visibility = 'hidden';
	edit2.style.visibility = 'hidden';

    } else {
        count2.innerHTML = 'Home'
        save2.style.visibility = 'visible';
        edit2.style.visibility = 'visible';
    }
}; 

save2.onclick = function(e) {
    fetch('test')
    	.then(response => console.log(response.body));
}

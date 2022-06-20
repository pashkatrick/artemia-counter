var count = document.getElementById('count');
var save = document.getElementById('save');
var edit = document.getElementById('edit');

count.onclick = function(e) {
    e.preventDefault();

    if (save.style.visibility == 'visible' && edit.style.visibility == 'visible') {
        count.innerHTML = 'Count'
        save.style.visibility = 'hidden';
	edit.style.visibility = 'hidden';

    } else {
        count.innerHTML = 'Home'
        save.style.visibility = 'visible';
        edit.style.visibility = 'visible';
    }
}; 

save.onclick = function(e) {
    e.preventDefault();
}

edit.onclick = function(e) {
    e.preventDefault();
}
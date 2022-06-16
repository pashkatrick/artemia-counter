const count = document.getElementById('count');

count.onclick = function() {
    const save = document.getElementById('save');
    const edit = document.getElementById('edit');

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
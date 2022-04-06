const count = document.getElementById('count');

count.onclick = function() {
    const save = document.getElementById('save');
    const edit = document.getElementById('edit');
    console.log(save)

    if (save.style.visibility === 'hidden' && edit.style.visibility === 'hidden') {
        save.style.visibility = 'visible';
	edit.style.visibility = 'visible';
        count.innerHTML = 'Home'
    } else {
        save.style.visibility = 'hidden';
        edit.style.visibility = 'hidden';
        count.innerHTML = 'Count'
    }
}; 
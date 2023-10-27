//Company
document.getElementById('company_box').addEventListener('input', function() {
    const companyBox_input = document.getElementById('companyBox_input');

    if (this.value !== '') {
        companyBox_input.style.display = 'block';
    } else {
        companyBox_input.style.display = 'none';
    }
});

//Journalist
document.getElementById('journalist_box').addEventListener('input', function() {
    const journalistBox_input = document.getElementById('journalistBox_input');

    if (this.value !== '') {
        journalistBox_input.style.display = 'block';
    } else {
        journalistBox_input.style.display = 'none';
    }
});



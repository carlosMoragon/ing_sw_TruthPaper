document.getElementById('company_box').addEventListener('input', function() {
    const companyBox_input = document.getElementById('companyBox_input');

    if (this.value !== '') {
        companyBox_input.style.display = 'block';
    } else {
        companyBox_input.style.display = 'none';
    }
});

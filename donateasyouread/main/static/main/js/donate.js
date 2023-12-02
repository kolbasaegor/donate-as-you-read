const donateForm = document.querySelector('#donateForm');

donateForm.addEventListener("submit", (event) => {
    event.preventDefault();
    donateForm.querySelector('.spinner-border.spinner-border-sm').hidden = false;

    const accountRegex = /(0x[a-fA-F0-9]{40})/g;
    const pkRegex = /([a-f0-9]{64})/g;

    const fromAccount = donateForm.querySelector('#fromAccount').value;
    if ( !accountRegex.test(fromAccount) ) {
        donateForm.querySelector('#errorFromAccount').hidden = false;
        donateForm.querySelector('.spinner-border.spinner-border-sm').hidden = true;
        return;
    }
    donateForm.querySelector('#errorFromAccount').hidden = true;

    const pk = donateForm.querySelector('#privateKey').value;
    if ( !pkRegex.test(pk) ) {
        donateForm.querySelector('#errorPK').hidden = false;
        donateForm.querySelector('.spinner-border.spinner-border-sm').hidden = true;
        return;
    }
    donateForm.querySelector('#errorPK').hidden = true;

    donateForm.submit();
});


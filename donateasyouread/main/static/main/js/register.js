const registerForm = document.querySelector('#registerForm');

registerForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const accountRegex = /(0x[a-fA-F0-9]{40})/g;
    const ethAddress = registerForm.querySelector('#ethAddress');
    const ethWalletErrorMsg = registerForm.querySelector('#ethWalletErrorMsg');

    if ( !accountRegex.test(ethAddress.value) ) {
        ethWalletErrorMsg.textContent = "Invalid Ethereum address";
        ethWalletErrorMsg.hidden = false;
        return;
    }
    ethWalletErrorMsg.hidden = true;

    const password1 = registerForm.querySelector('#password1');
    const password2 = registerForm.querySelector('#password2');
    const passwordErrorMsg = registerForm.querySelector('#passwordErrorMsg');

    if ( password1.value != password2.value ){
        passwordErrorMsg.textContent = "Password mismatch";
        passwordErrorMsg.hidden = false;
        return;
    }
    passwordErrorMsg.hidden = true;

    registerForm.submit();
});
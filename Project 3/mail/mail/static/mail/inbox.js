document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    document.querySelector('#compose-form').addEventListener('submit', event => {
        event.preventDefault();
        
        const recipients = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;

        if (!(subject.trim() !== '' && body.trim() !== '')) {
            alert("Subject and body can not be empty");
            return;
        }

        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(result => {
                    alert(result.error);
                    return Promise.resolve();
                })
            }
        })
        .then(result => {
            alert(result.message);
            setTimeout(() => {
                load_mailbox('inbox');
            }, 3000);
        })
    })
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        const emailFragment = document.createDocumentFragment();

        emails.forEach(email => {
            const emailElement = document.createElement('div');
            emailElement.className = 'email-inline';

            // create email content
            const emailSender = document.createElement('span');
            emailSender.textContent = email.sender.split('@')[0];

            const emailSubject = document.createElement('span');
            emailSubject.textContent = email.subject;

            const emailTimestamp = document.createElement('span');
            emailTimestamp.textContent = email.timestamp;

            emailElement.append(emailSender, emailSubject, emailTimestamp);
            emailFragment.appendChild(emailElement);
        });

        document.querySelector('#emails-view').appendChild(emailFragment);
    })
}
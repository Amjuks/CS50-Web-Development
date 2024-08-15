document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => compose_email());

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(reply_to_mail) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    const emailFields = {
        recipients: '',
        subject: '',
        body: ''
    };

    // Clear out composition fields
    if (reply_to_mail) {
        emailFields.recipients = reply_to_mail.sender;
        emailFields.subject = reply_to_mail.subject;

        if (!emailFields.subject.startsWith('Re: ')) {
            emailFields.subject = 'Re: ' + emailFields.subject;
        }

        const prefix = `On ${reply_to_mail.timestamp} ${reply_to_mail.sender} wrote:\n`;
        emailFields.body = `${prefix}\n${reply_to_mail.body}\n\n`;
    }

    document.querySelector('#compose-recipients').value = emailFields.recipients;
    document.querySelector('#compose-subject').value = emailFields.subject;
    document.querySelector('#compose-body').value = emailFields.body;

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

            return response.json();
        })
        .then(result => {
            load_mailbox('inbox');
        })
    })
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#email-content-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        const emailFragment = document.createDocumentFragment();

        emails.forEach(email => {
            const emailElement = document.createElement('span');
            emailElement.className = 'email-inline';

            if (mailbox !== 'sent') {
                emailElement.classList.toggle('read', email.read);
            }

            // create email content
            const emailSender = document.createElement('span');
            emailSender.textContent = email.sender.split('@')[0];

            const emailSubject = document.createElement('span');
            emailSubject.className = 'email-inline-subject';
            emailSubject.textContent = email.subject;

            const emailTimestamp = document.createElement('span');
            emailTimestamp.className = 'email-inline-timestamp';
            emailTimestamp.textContent = email.timestamp;

            emailElement.append(emailSender, emailSubject, emailTimestamp);
            emailElement.onclick = () => load_email(email.id);
            emailFragment.appendChild(emailElement);
        });

        document.querySelector('#emails-view').appendChild(emailFragment);
    })
}

function load_email(emailId) {
    // Show the mailbox and hide other views
    document.querySelector('#email-content-view').style.display = 'block';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
        
    fetch(`/emails/${emailId}`)
    .then(response => response.json())
    .then(email => {
        // create outline elemenets
        const emailContainer = document.createElement('div');
        const emailHeader = document.createElement('div');
        const emailActions = document.createElement('div');

        //create action buttons
        const actionButtons = [];
        if (email.sender !== username) {
            actionButtons.push(
                createActionButton(email.archived ? 'unarchive':'archive', {emailId: email.id})
            );
        }
        actionButtons.push(createActionButton('reply', {email: email}));
        actionButtons.forEach(button => emailActions.appendChild(button));

        // create the elements
        const sender = document.createElement('span');
        const timestamp = document.createElement('span');

        const recipients = document.createElement('p');
        const subject = document.createElement('h3');
        const body = document.createElement('p');

        // assign classes to elements
        emailContainer.className = 'email-content-container';
        emailHeader.className = 'email-content-header';
        emailActions.className = 'email-content-actions';
        sender.className = 'email-content-sender';
        timestamp.className = 'email-content-timestamp';
        recipients.className = 'email-content-recipients';
        subject.className = 'email-content-subject';
        body.className = 'email-content-body';

        // write into elements
        sender.innerHTML = `From: ${createEmailElement(email.sender)}`;
        timestamp.textContent = email.timestamp;
        recipients.innerHTML = 'To: ' + email.recipients.map(createEmailElement).join('');
        subject.textContent = email.subject;
        body.textContent = email.body;

        // assemble the elements
        emailHeader.append(sender, timestamp);
        emailContainer.append(
            subject,
            emailHeader,
            recipients,
            emailActions,
            body
        );

        document.querySelector('#email-content-view').innerHTML = '';
        document.querySelector('#email-content-view').appendChild(emailContainer);

        if (!email.read) {
            readEmail(email);
        }
    })
}

function readEmail(email) {
    fetch(`emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
}

function createActionButton (name, args) {
    const button = document.createElement('button');
    button.className = 'btn btn-sm btn-outline-info btn-action';
    button.textContent = name[0].toUpperCase() + name.slice(1);

    switch (name){
        case 'archive':
            button.setAttribute('data-email-id', args.emailId);
            onArchiveClicked(button, true);
            break;
        
        case 'unarchive':
            button.setAttribute('data-email-id', args.emailId);
            onArchiveClicked(button, false);
            break;

        case 'reply':
            onEmailReply(button, args.email);

        default:
            break;
    }

    return button
}

function onArchiveClicked (button, archive = true) {
    button.addEventListener('click', event => {
        event.preventDefault();
        const emailId = button.getAttribute('data-email-id');
        console.log('fetch url:');
        console.log(`emails/${emailId}`);

        fetch(`emails/${emailId}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: archive
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Something went wrong");
            }

            load_email(emailId);
        })
        .catch(error => console.error(error));
    })
}

function onEmailReply (button, email) {
    button.addEventListener('click', event => {
        event.preventDefault();
        compose_email(email);
    })
}

function createEmailElement (email) {
    const emailElement = document.createElement('span');
    emailElement.className = 'email-address';
    emailElement.textContent = email;

    return emailElement.outerHTML;
}
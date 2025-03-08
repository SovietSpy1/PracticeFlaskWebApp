document.getElementById('create_button').addEventListener('click', function(event) {
    event.preventDefault();
    const form = document.getElementById(('creation_form'))
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key)=>{
        data[key] = value;
    });
    fetch("/create_user", {method: 'POST',
        headers:{
            "Content-type": "application/json"
        }, body: JSON.stringify(data)
    })
        .then(response=>{
            if (!response.ok){throw new Error("Network response was not ok");}
            return response.json();
        })
        .then(responseData => {
            document.getElementById("creation_status").innerText = JSON.stringify(responseData);
        })
        .catch(error =>{console.error('Error:', error);
        document.getElementById('creation_status').innerText = "Error: ${error.message}";});
})
document.getElementById('login_button').addEventListener('click', function(event) {
    event.preventDefault();
    const form = document.getElementById(('login_form'))
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key)=>{
        data[key] = value;
    });
    fetch("/login", {method: 'POST',
        headers:{
            "Content-type": "application/json"
        }, body: JSON.stringify(data)
    })
        .then(response=>{
            if (!response.ok){throw new Error("Network response was not ok");}
            return response.json();
        })
        .then(responseData => {
            document.getElementById("login_status").innerText = JSON.stringify(responseData);
        })
        .catch(error =>{console.error('Error:', error);
        document.getElementById('login_status').innerText = "Error: ${error.message}";});
})
document.getElementById('user_update_button').addEventListener('click', function(event) {
    event.preventDefault();
    const form = document.getElementById(('user_update_form'))
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key)=>{
        data[key] = value;
    });
    fetch("/update", {method: 'POST',
        headers:{
            "Content-type": "application/json"
        }, body: JSON.stringify(data)
    })
        .then(response=>{
            if (!response.ok){throw new Error("Network response was not ok");}
            return response.json();
        })
        .then(responseData => {
            document.getElementById("user_update_status").innerText = JSON.stringify(responseData);
        })
        .catch(error =>{console.error('Error:', error);
        document.getElementById('user_update_status').innerText = "Error: ${error.message}";});
})
document.getElementById('password_update_button').addEventListener('click', function(event) {
    event.preventDefault();
    const form = document.getElementById(('password_update_form'))
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key)=>{
        data[key] = value;
    });
    fetch("/update", {method: 'POST',
        headers:{
            "Content-type": "application/json"
        }, body: JSON.stringify(data)
    })
        .then(response=>{
            if (!response.ok){throw new Error("Network response was not ok");}
            return response.json();
        })
        .then(responseData => {
            document.getElementById("password_update_status").innerText = JSON.stringify(responseData);
        })
        .catch(error =>{console.error('Error:', error);
        document.getElementById('password_update_status').innerText = "Error: ${error.message}";});
})
document.getElementById('view_button').addEventListener('click', function(event) {
    event.preventDefault();
    const form = document.getElementById(('view_form'))
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key)=>{
        data[key] = value;
    });
    fetch("/view", {method: 'POST',
        headers:{
            "Content-type": "application/json"
        }, body: JSON.stringify(data)
    })
        .then(response=>{
            if (!response.ok){throw new Error("Network response was not ok");}
            return response.json();
        })
        .then(responseData => {
            document.getElementById("view_status").innerText = JSON.stringify(responseData);
        })
        .catch(error =>{console.error('Error:', error);
        document.getElementById('view_status').innerText = "Error: ${error.message}";});
})
document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.input');
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown=>{
        const select = dropdown.querySelector('.select');
        const caret = dropdown.querySelector('.caret');
        const menu = dropdown.querySelector('.menu');
        const options = dropdown.querySelectorAll('.menu li');
        const selected = dropdown.querySelector('.selected');
        select.addEventListener('click', ()=> {
            select.classList.toggle('select-clicked');
            caret.classList.toggle('caret-rotate');
            menu.classList.toggle('menu-open');
        });
        options.forEach(option => {
            option.addEventListener('click', ()=>{
                elements.forEach(element=> element.classList.remove('visible'));
                document.getElementById(option.getAttribute('data-target')).classList.toggle('visible');
                selected.innerText = option.innerText;
                selected.innerText = option.innerText;
                select.classList.remove('select-clicked');
                caret.classList.remove('caret-rotate');
                menu.classList.remove('menu-open');
                options.forEach(option => (option.classList.remove('active')));
                option.classList.toggle('active');
            });
        });
    });
});

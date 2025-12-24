// Add Todo JS
const todoForm = document.getElementById('todoForm');
if (todoForm) {
    todoForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            title: data.title,
            description: data.description,
            priority: parseInt(data.priority.trim()),
            complete: false
        };

        try {
            const response = await fetch('/todos/todo', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                form.reset();
                alert("Todo added successfully!");
            } else {
                const errorData = await response.json();
                console.log(errorData);
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// Edit Todo JS
const editTodoForm = document.getElementById('editTodoForm');
if (editTodoForm) {
    editTodoForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const url = window.location.pathname;
        const todoId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            title: data.title,
            description: data.description,
            priority: parseInt(data.priority),
            complete: data.complete === "on"
        };

        try {
            const response = await fetch(`/todos/${todoId}`, {
                method: 'PUT',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
                return
            }
            alert("Todo updated successfully!");
            window.location.href = '/todos/todo-page'

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    document.getElementById('deleteButton').addEventListener('click', async function () {
        const url = window.location.pathname;
        const todoId = url.substring(url.lastIndexOf('/') + 1);

        try {
            const response = await fetch(`/todos/${todoId}`, {
                method: 'DELETE',
                credentials: 'same-origin'
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
                return
            }
            alert("Todo deleted successfully!");
            window.location.href = '/todos/todo-page'

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}

// Login JS
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(event.target);
        const payload = new URLSearchParams(formData);

        try {
            const response = await fetch('/auth/token', {
                method: 'POST',
                credentials: 'same-origin', // ensures HttpOnly cookie is saved
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload.toString()
            });

            if (!response.ok) {
                const errorData = await response.json();
                alert(errorData.detail);
                return;
            }
            console.log(response);
            window.location.href = '/todos/todo-page'

        } catch (err) {
            console.error(err);
            alert("Login failed");
        }
    });
}

// Register JS
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if (data.input_password !== data.input_confirm_password) {
            alert("Passwords do not match");
            return;
        }

        const payload = {
            email: data.input_email,
            username: data.input_username,
            first_name: data.input_firstname,
            last_name: data.input_lastname,
            role: data.input_role,
            phone_number: data.input_phone_number,
            password: data.input_password
        };

        try {
            const response = await fetch('/auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/auth/login-page';
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.message}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
}
document.getElementById('serviceForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/services/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            Swal.fire({
                title: 'Success!',
                text: 'Service created successfully.',
                icon: 'success',
                confirmButtonText: 'OK'
            }).then(() => {
                window.location.href = '/service_table/';
            });
        } else {
            Swal.fire({
                title: 'Error!',
                text: 'Failed to create service.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: 'Error!',
            text: 'An unexpected error occurred.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
});



// scripts 2

async function submitForm() {
    const form = document.getElementById('service-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const serviceId = form.action.split('/').pop();  // Get the service ID from the form action URL

    try {
        const response = await fetch(`/services/${serviceId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorText = await response.text();
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: `HTTP error! Status: ${response.status}. ${errorText}`,
            });
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Success:', result);

        // Display success message
        Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: 'Service updated successfully.',
            showConfirmButton: false,
            timer: 1500
        }).then(() => {
            // Optionally redirect or refresh the page
            window.location.href = '/service_table/';
        });
    } catch (error) {
        console.error('Error:', error);

        // Display error message
        Swal.fire({
            icon: 'error',
            title: 'Error!',
            text: `An error occurred: ${error.message}`,
        });
    }
}


function delete_test(button) {
    event.preventDefault();
    const serviceId = button.dataset.serviceId;

    bootbox.confirm({
        message: "Are you sure you want to delete this record?",
        buttons: {
            confirm: {
                label: 'Yes',
                className: 'btn-danger'
            },
            cancel: {
                label: 'No',
                className: 'btn-secondary'
            }
        },
        callback: function(result) {
            if (result) {
                fetch(`/services/${serviceId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        id: serviceId
                    })
                })
                .then(response => {
                    if (response.ok) {
                        location.reload(); // Reload the page upon successful deletion
                    } else {
                        console.error('Error deleting record');
                    }
                })
                .catch(error => {
                    console.error('Error deleting record:', error);
                });
            }
        }
    });
}

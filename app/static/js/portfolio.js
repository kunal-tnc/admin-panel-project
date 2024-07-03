

// scripts 2

document.getElementById('updatePortfolioForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const form = event.target;
    const portfolioId = form.getAttribute('data-portfolio-id');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`/portfolios/${portfolioId}`, {
            method: 'PUT',
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
                text: 'Portfolio updated successfully.',
                icon: 'success',
                confirmButtonText: 'OK'
            }).then(() => {
                window.location.href = '/portfolios_table/';
            });
        } else {
            Swal.fire({
                title: 'Error!',
                text: 'Failed to update portfolio.',
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



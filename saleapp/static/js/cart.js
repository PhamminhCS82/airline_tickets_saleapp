function addTicket(ticketId ,name, passport, telephone, ticketClass, price) {
    event.preventDefault()
    console.log(ticketId)
    // promise
    fetch('/api/add-ticket', {
        method: 'post',
        body: JSON.stringify({
            'ticket_id': ticketId,
            'passport': passport,
            'name': name,
            'telephone': telephone,
            'ticket_class': ticketClass,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json()
    }).then(function(data) {
        if(data.code !== null && data.code === 400)
            window.alert('Trùng CMND/Hộ Chiếu')
        else
            location.reload()
    })
}

function pay() {
    if (confirm('Ban chac chan thanh toan khong?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            if (data.code === 200)
                location.reload()
            else
                console.log(data)
        })
    }
}


function checkout() {
    fetch('/stripe_pay', {
        method: 'post'
        })
    .then((result) => { return result.json(); })
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            // Make the id field from the Checkout Session creation API response
            // available to this file, so you can provide it as parameter here
            // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
            sessionId: data.checkout_session_id
        }).then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, display the localized error message to your customer
            // using `result.error.message`.
        });
    })
}